// All configuration comes from config.mjs — no process.env reads for
// structural values (paths, URLs, ports) anywhere in this file.
import {
  DATA_DIR,
  SUBMISSIONS_DIR as CONFIG_SUBMISSIONS_DIR,
  CORPUS_DIR,
  METRICS_DIR,
  PORT,
  APP_URL as appUrl,
  DEBUG_MODE,
  isProduction,
  isRender,
  ensureDataDir,
  getEnv,
} from './config.mjs';
import express from 'express';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import cookieParser from 'cookie-parser';
import session from 'express-session';
import axios from 'axios';
import passport from './passport.mjs';
import {
  initializeDatabase,
  getUserByEmail,
  getUserById,
  getUserByInitials,
  isInitialsTaken,
  createArticleCoding,
  createOrUpdateArticleCoding,
  getArticleCodings,
  createSummaryReview,
  createOrUpdateSummaryReview,
  getSummaryReviews,
  getUserSummaryReview,
  getUserArticleCoding
} from './db.mjs';
import {
  createToken,
  verifyToken,
  handleGithubAuth,
  handleGoogleAuth,
  debugLogin,
  setSessionCookie,
  clearSessionCookie
} from './auth.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

let SUBMISSIONS_DIR = CONFIG_SUBMISSIONS_DIR;

// Allowed origins for CORS
const allowedOrigins = [
  'http://localhost:8787',
  'http://localhost:3000',
  'https://gamebasedlibraryservicesliterature.onrender.com'
];

// Initialize database
initializeDatabase();

// Ensure submissions directory exists. In production this throws if the
// configured directory (e.g. a persistent disk) is unavailable rather than
// silently writing to ephemeral storage; in development it falls back locally.
SUBMISSIONS_DIR = await ensureDataDir(SUBMISSIONS_DIR, { label: 'submissions' });

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Session management for OAuth
// Session middleware: only use secure cookies on Render (which has HTTPS)
const hasRenderEnv = !!process.env.RENDER || !!process.env.RENDER_EXTERNAL_URL;
app.use(
  session({
    secret: getEnv('JWT_SECRET', 'dev-secret'),
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: hasRenderEnv,
      sameSite: 'lax',
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
    },
  })
);

// Passport initialization
app.use(passport.initialize());
app.use(passport.session());

// CORS headers - allow localhost and Render domains
app.use((req, res, next) => {
  const origin = req.headers.origin;
  
  // Allow if origin matches allowed list or if no origin (same-domain requests)
  if (!origin || allowedOrigins.includes(origin)) {
    res.set('Access-Control-Allow-Origin', origin || '*');
  }
  
  res.set('Cache-Control', 'no-store');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  res.set('Access-Control-Allow-Credentials', 'true');
  
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Auth middleware to extract user from token or Passport session.
// Passport.session() already set req.user if the session is valid,
// so only check the JWT cookie if Passport didn't authenticate.
app.use((req, res, next) => {
  if (req.user) {
    // Passport session already authenticated this user
    return next();
  }

  // No Passport session — try JWT cookie
  const token = req.cookies.auth_token;
  if (token && typeof token === 'string') {
    const decoded = verifyToken(token);
    if (decoded && decoded.userId) {
      try {
        req.user = getUserById(decoded.userId);
        if (!req.user) {
          // User doesn't exist, clear the cookie
          clearSessionCookie(res);
        }
      } catch (error) {
        console.error('Error loading user from JWT:', error.message);
        clearSessionCookie(res);
      }
    } else {
      // Invalid or malformed token
      clearSessionCookie(res);
    }
  }
  next();
});

// Protected route middleware
function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  next();
}

// Public auth routes (no authentication required)
const authRoutes = ['/auth/', '/api/debug-status', '/api/debug-login', '/health'];

// Middleware to redirect unauthenticated users
app.use((req, res, next) => {
  // Allow auth routes, health check, and static files
  if (authRoutes.some(route => req.path.startsWith(route)) || 
      req.path === '/register.html' || 
      req.path === '/login.html' ||
      req.path.endsWith('.css') || 
      req.path.endsWith('.js')) {
    return next();
  }

  // Redirect to login if not authenticated and trying to access app
  if (!req.user && (req.path === '/' || req.path.startsWith('/api/'))) {
    if (req.path.startsWith('/api/')) {
      return res.status(401).json({ error: 'Please log in to access this resource' });
    }
    return res.redirect('/login.html');
  }

  next();
});

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// ==================== UTILITY FUNCTIONS ====================

function cleanUsercode(value) {
  return String(value || '').trim().replace(/\s+/g, ' ');
}

function safeKeyPart(value) {
  return encodeURIComponent(String(value).toLowerCase());
}

function parseRubric(markdown) {
  const match = markdown.match(/```json rubric\s*([\s\S]*?)```/);
  if (!match) throw new Error('Summary quality rubric definition is missing.');
  const rubric = JSON.parse(match[1]);
  if (!rubric.id || !rubric.version || !Array.isArray(rubric.dimensions) || !rubric.dimensions.length) {
    throw new Error('Summary quality rubric definition is invalid.');
  }
  return rubric;
}

async function loadRubric() {
  const rubricPath = path.join(__dirname, 'public', 'summary_quality_rubric.md');
  const content = await fs.readFile(rubricPath, 'utf-8');
  return parseRubric(content);
}

async function readJSONFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

// ==================== AUTHENTICATION ROUTES ====================

// Health check (public)
app.get('/health', (req, res) => {
  res.json({ ok: true });
});

// Debug login endpoint (debug mode only)
// Check if debug mode is available
app.get('/api/debug-status', (req, res) => {
  res.json({ debugMode: DEBUG_MODE });
});

app.post('/api/debug-login', async (req, res) => {
  try {
    if (!DEBUG_MODE) {
      return res.status(403).json({ error: 'Debug login is not available in production' });
    }

    const { user, token } = await debugLogin();

    console.log('[DEBUG-LOGIN] Setting session cookie');
    console.log('[DEBUG-LOGIN] Token:', token.substring(0, 20) + '...');
    console.log('[DEBUG-LOGIN] isProduction:', isProduction);
    console.log('[DEBUG-LOGIN] process.env.NODE_ENV:', process.env.NODE_ENV);
    
    setSessionCookie(res, token);
    
    console.log('[DEBUG-LOGIN] Response headers:', res.getHeaders());
    
    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        initials: user.initials,
        organizationalAffiliation: user.organizational_affiliation
      },
      debug: 'Debug mode enabled - test user created/loaded'
    });
  } catch (error) {
    console.error('[DEBUG-LOGIN] Error:', error);
    res.status(400).json({ error: error.message });
  }
});

// Logout endpoint
app.post('/api/logout', (req, res) => {
  clearSessionCookie(res);
  res.json({ success: true });
});

// Get current user
app.get('/api/user', (req, res) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  res.json({
    id: req.user.id,
    email: req.user.email,
    fullName: req.user.full_name,
    initials: req.user.initials,
    organizationalAffiliation: req.user.organizational_affiliation
  });
});

// GitHub OAuth login initiation
app.get('/auth/github', passport.authenticate('github', { scope: ['user:email'] }));

// GitHub OAuth callback
app.get(
  '/auth/github/callback',
  passport.authenticate('github', { failureRedirect: '/login.html?error=GitHub login failed' }),
  (req, res) => {
    // Passport authenticated the user and set req.user.
    // Create a JWT token and set it as a cookie for persistence.
    if (!req.user) {
      return res.redirect('/login.html?error=Authentication failed');
    }
    const token = createToken(req.user.id);
    setSessionCookie(res, token);
    res.redirect('/');
  }
);

// Google OAuth login initiation
app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

// Google OAuth callback
app.get(
  '/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login.html?error=Google login failed' }),
  (req, res) => {
    // Passport authenticated the user and set req.user.
    // Create a JWT token and set it as a cookie for persistence.
    if (!req.user) {
      return res.redirect('/login.html?error=Authentication failed');
    }
    const token = createToken(req.user.id);
    setSessionCookie(res, token);
    res.redirect('/');
  }
);

// ==================== METRICS ENDPOINTS ====================

app.get('/api/metrics', requireAuth, async (req, res) => {
  try {
    const metricsPath = path.join(METRICS_DIR, 'gbls_corpus_metrics');
    const datasetPath = path.join(metricsPath, 'dataset_summary.json');
    
    let summary;
    try {
      const content = await fs.readFile(datasetPath, 'utf-8');
      summary = JSON.parse(content);
    } catch (error) {
      console.error('Error loading dataset summary:', error.message);
      return res.status(500).json({ error: 'Metrics data not found' });
    }
    
    const articlesPath = path.join(metricsPath, 'articles_core.csv');
    let articles = [];
    
    try {
      const csv = await fs.readFile(articlesPath, 'utf-8');
      const lines = csv.trim().split('\n');
      const headers = lines[0].split(',').map(h => h.trim());
      
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const article = {};
        headers.forEach((header, idx) => {
          article[header.toLowerCase()] = values[idx]?.trim() || null;
        });
        if (article.article_id) articles.push(article);
      }
    } catch (error) {
      console.warn('Could not load articles from CSV:', error.message);
    }
    
    const featureGroups = [
      { key: 'source_type', label: 'Source Type' },
      { key: 'peer_review', label: 'Peer Review' },
      { key: 'evidence_type', label: 'Evidence Type' },
      { key: 'primary_methodology', label: 'Primary Methodology' },
      { key: 'library_context', label: 'Library Context' },
      { key: 'game_format', label: 'Game Format' },
      { key: 'service_area', label: 'Service Area' },
      { key: 'audience', label: 'Audience' },
      { key: 'intended_outcome', label: 'Intended Outcome' },
      { key: 'evidence_confidence', label: 'Evidence Confidence' },
      { key: 'coding_confidence', label: 'Coding Confidence' },
      { key: 'conceptual_theme', label: 'Conceptual Theme' }
    ];
    
    res.json({
      summary,
      featureGroups,
      articles
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/reference-metrics', requireAuth, async (req, res) => {
  try {
    const metricsPath = path.join(METRICS_DIR, 'reference_corpus_metrics');
    const datasetPath = path.join(metricsPath, 'dataset_summary.json');
    const data = await readJSONFile(datasetPath);
    res.json(data || { error: 'Reference metrics data not found' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== ARTICLES ENDPOINTS ====================

app.get('/api/articles', requireAuth, async (req, res) => {
  try {
    const articles = [];
    
    const publicDataPath = path.join(__dirname, 'public', 'data', 'articles');
    try {
      const files = await fs.readdir(publicDataPath);
      for (const file of files) {
        if (file.endsWith('.json') && !file.startsWith('.')) {
          const filePath = path.join(publicDataPath, file);
          const data = await readJSONFile(filePath);
          if (data && data.id) {
            articles.push({
              id: data.id,
              citation: data.citation || file,
              summary: data.summary || '',
              sourceText: data.sourceText || '',
              evidence: data.evidence || {}
            });
          }
        }
      }
    } catch (error) {
      const corpusPath = CORPUS_DIR;
      try {
        const files = await fs.readdir(corpusPath);
        for (const file of files) {
          if (file.endsWith('.json') && !file.startsWith('.')) {
            const filePath = path.join(corpusPath, file);
            const data = await readJSONFile(filePath);
            if (data && data.id) {
              articles.push({
                id: data.id,
                citation: data.citation || file,
                summary: data.summary || '',
                sourceText: data.sourceText || '',
                evidence: data.evidence || {}
              });
            }
          }
        }
      } catch (err) {
        // Corpus directory also unavailable
      }
    }
    
    res.json(articles);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/article/:id', requireAuth, async (req, res) => {
  try {
    let data = null;
    const publicFilePath = path.join(__dirname, 'public', 'data', 'articles', `${req.params.id}.json`);
    data = await readJSONFile(publicFilePath);
    
    if (!data) {
      const corpusPath = CORPUS_DIR;
      const corpusFilePath = path.join(corpusPath, `${req.params.id}.json`);
      data = await readJSONFile(corpusFilePath);
    }

    if (!data) {
      return res.status(404).json({ error: 'Article not found' });
    }

    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== CODINGS ENDPOINTS ====================

app.get('/api/codings', requireAuth, async (req, res) => {
  try {
    const codings = getArticleCodings();
    res.json(codings);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user's existing coding for an article
app.get('/api/codings/:articleId', requireAuth, async (req, res) => {
  try {
    const { articleId } = req.params;
    const coding = getUserArticleCoding(req.user.id, articleId);
    
    if (!coding) {
      return res.status(404).json({ error: 'No coding found' });
    }
    
    res.json(coding);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/codings', requireAuth, async (req, res) => {
  try {
    const { articleId, codes, rubricId, rubricVersion, hadClassificationIssues, classificationNotes } = req.body;
    console.log('[POST /api/codings] Received:', { articleId, codes, hadClassificationIssues, classificationNotes });
    
    if (!articleId || !codes) {
      console.log('[POST /api/codings] Missing required fields');
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const codingId = `coding_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    console.log('[POST /api/codings] Creating/updating with codingId:', codingId, 'userId:', req.user.id);
    
    const result = createOrUpdateArticleCoding(
      codingId,
      articleId,
      req.user.id,
      codes,
      rubricId,
      rubricVersion,
      hadClassificationIssues || false,
      classificationNotes || null
    );

    console.log('[POST /api/codings] Result:', result);
    res.json({ success: true, id: result.id, updated: result.updated });
  } catch (error) {
    console.error('[POST /api/codings] Error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ==================== SUMMARIES ENDPOINTS ====================

app.get('/api/summaries', requireAuth, async (req, res) => {
  try {
    const summaries = getSummaryReviews();
    res.json(summaries);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user's existing review for an article
app.get('/api/summaries/:articleId', requireAuth, async (req, res) => {
  try {
    const { articleId } = req.params;
    const review = getUserSummaryReview(req.user.id, articleId);
    
    if (!review) {
      return res.status(404).json({ error: 'No review found' });
    }
    
    res.json(review);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/summaries', requireAuth, async (req, res) => {
  try {
    const rubric = await loadRubric();
    const { articleId, ratings, qualityRating, notes } = req.body;
    
    if (!articleId || !ratings) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const reviewId = `review_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const result = createOrUpdateSummaryReview(
      reviewId,
      articleId,
      req.user.id,
      ratings,
      qualityRating,
      notes,
      rubric.id,
      rubric.version
    );

    res.json({ success: true, id: result.id, updated: result.updated });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== ERROR HANDLING ====================

app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

// ==================== START SERVER ====================

app.listen(PORT, () => {
  console.log('\n' + '='.repeat(70));
  console.log('GBLS Literature Reviewer API Server');
  console.log('='.repeat(70));
  console.log(`🚀 Environment: ${isRender ? 'Render.com' : isProduction ? 'Docker' : 'Development'}`);
  console.log(`🌐 URL: ${appUrl}`);
  console.log(`🔌 Port: ${PORT}`);
  console.log(`🔓 Debug Mode: ${DEBUG_MODE ? 'ENABLED' : 'disabled'}`);
  console.log(`💾 Data dir: ${DATA_DIR}`);
  console.log(`📁 Submissions: ${SUBMISSIONS_DIR}`);
  console.log(`📚 Corpus: ${CORPUS_DIR}`);
  console.log(`📊 Metrics: ${METRICS_DIR}`);
  console.log('='.repeat(70) + '\n');

  if (DEBUG_MODE) {
    console.log('⚠️  DEBUG MODE ENABLED - Users can login with any email');
    console.log('   To disable, remove DEBUG_MODE from .env and restart\n');
  }
});
