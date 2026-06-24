import Database from 'better-sqlite3';
import path from 'path';
import { mkdirSync } from 'fs';
import { DB_PATH, isProduction } from './config.mjs';

const dbPath = DB_PATH;

let db;

export function initializeDatabase() {
  // Ensure the directory holding the database exists (e.g. the data root on
  // a fresh persistent disk) before opening the connection. In production we
  // refuse to fall back to ephemeral storage so a misconfigured/unmounted
  // persistent disk fails loudly instead of silently losing user data.
  const dbDir = path.dirname(dbPath);
  try {
    mkdirSync(dbDir, { recursive: true });
  } catch (error) {
    if ((error.code === 'EACCES' || error.code === 'ENOENT') && isProduction) {
      throw new Error(
        `FATAL: database directory "${dbDir}" is not usable (${error.code}). ` +
        `Refusing to use ephemeral storage in production. ` +
        `Verify the persistent disk is mounted and DATA_DIR points at it.`
      );
    }
    throw error;
  }
  db = new Database(dbPath);
  db.pragma('journal_mode = WAL');

  // Create users table if it doesn't exist
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      full_name TEXT NOT NULL,
      initials TEXT UNIQUE NOT NULL,
      organizational_affiliation TEXT,
      github_id TEXT UNIQUE,
      google_id TEXT UNIQUE,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      last_login DATETIME,
      is_active BOOLEAN DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      user_id INTEGER NOT NULL,
      token TEXT UNIQUE NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      expires_at DATETIME NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS article_codings (
      id TEXT PRIMARY KEY,
      article_id TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      codes TEXT NOT NULL,
      rubric_id TEXT,
      rubric_version TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS summary_reviews (
      id TEXT PRIMARY KEY,
      article_id TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      ratings TEXT NOT NULL,
      quality_rating TEXT,
      notes TEXT,
      rubric_id TEXT,
      rubric_version TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );
  `);

  return db;
}

export function getDatabase() {
  if (!db) initializeDatabase();
  return db;
}

// User functions
export function createUser(email, fullName, initials, organizationalAffiliation = null, githubId = null, googleId = null) {
  const db = getDatabase();
  try {
    const stmt = db.prepare(`
      INSERT INTO users (email, full_name, initials, organizational_affiliation, github_id, google_id, last_login)
      VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    `);
    const result = stmt.run(email, fullName, initials, organizationalAffiliation, githubId, googleId);
    return getUserById(result.lastInsertRowid);
  } catch (error) {
    if (error.message.includes('UNIQUE constraint failed')) {
      throw new Error('Email or initials already registered');
    }
    throw error;
  }
}

export function getUserByEmail(email) {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE email = ? AND is_active = 1').get(email);
}

export function getUserById(id) {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE id = ? AND is_active = 1').get(id);
}

export function getUserByGithubId(githubId) {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE github_id = ? AND is_active = 1').get(githubId);
}

export function getUserByGoogleId(googleId) {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE google_id = ? AND is_active = 1').get(googleId);
}

export function updateUserLastLogin(userId) {
  const db = getDatabase();
  db.prepare('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?').run(userId);
}

export function getUserByInitials(initials) {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE initials = ? AND is_active = 1').get(initials);
}

export function isInitialsTaken(initials) {
  const db = getDatabase();
  return db.prepare('SELECT COUNT(*) as count FROM users WHERE initials = ?').get(initials).count > 0;
}

// Session functions
export function createSession(userId, token, expiresInHours = 24) {
  const db = getDatabase();
  const sessionId = `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  const expiresAt = new Date(Date.now() + expiresInHours * 60 * 60 * 1000);
  
  db.prepare(`
    INSERT INTO sessions (id, user_id, token, expires_at)
    VALUES (?, ?, ?, ?)
  `).run(sessionId, userId, token, expiresAt.toISOString());
  
  return sessionId;
}

export function getSession(sessionId) {
  const db = getDatabase();
  const session = db.prepare(`
    SELECT s.*, u.* FROM sessions s
    JOIN users u ON s.user_id = u.id
    WHERE s.id = ? AND s.expires_at > CURRENT_TIMESTAMP
  `).get(sessionId);
  return session;
}

export function deleteSession(sessionId) {
  const db = getDatabase();
  db.prepare('DELETE FROM sessions WHERE id = ?').run(sessionId);
}

export function cleanupExpiredSessions() {
  const db = getDatabase();
  db.prepare('DELETE FROM sessions WHERE expires_at <= CURRENT_TIMESTAMP').run();
}

// Submission functions - Article Codings
export function createArticleCoding(codingId, articleId, userId, codes, rubricId = null, rubricVersion = null) {
  const db = getDatabase();
  const stmt = db.prepare(`
    INSERT INTO article_codings (id, article_id, user_id, codes, rubric_id, rubric_version)
    VALUES (?, ?, ?, ?, ?, ?)
  `);
  stmt.run(codingId, articleId, userId, JSON.stringify(codes), rubricId, rubricVersion);
  return { id: codingId, article_id: articleId, user_id: userId };
}

export function getArticleCodings() {
  const db = getDatabase();
  const rows = db.prepare(`
    SELECT ac.*, u.initials
    FROM article_codings ac
    LEFT JOIN users u ON ac.user_id = u.id
    ORDER BY ac.created_at DESC
  `).all();
  return rows.map(row => ({
    id: row.id,
    articleId: row.article_id,
    userId: row.user_id,
    usercode: row.initials,
    codes: JSON.parse(row.codes),
    rubricId: row.rubric_id,
    rubricVersion: row.rubric_version,
    timestamp: row.created_at
  }));
}

export function getArticleCodingsByArticle(articleId) {
  const db = getDatabase();
  const rows = db.prepare(`
    SELECT ac.*, u.initials
    FROM article_codings ac
    LEFT JOIN users u ON ac.user_id = u.id
    WHERE ac.article_id = ?
    ORDER BY ac.created_at DESC
  `).all(articleId);
  return rows.map(row => ({
    id: row.id,
    articleId: row.article_id,
    userId: row.user_id,
    usercode: row.initials,
    codes: JSON.parse(row.codes),
    rubricId: row.rubric_id,
    rubricVersion: row.rubric_version,
    timestamp: row.created_at
  }));
}

// Submission functions - Summary Reviews
export function createSummaryReview(reviewId, articleId, userId, ratings, qualityRating = null, notes = null, rubricId = null, rubricVersion = null) {
  const db = getDatabase();
  const stmt = db.prepare(`
    INSERT INTO summary_reviews (id, article_id, user_id, ratings, quality_rating, notes, rubric_id, rubric_version)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);
  stmt.run(reviewId, articleId, userId, JSON.stringify(ratings), qualityRating, notes, rubricId, rubricVersion);
  return { id: reviewId, article_id: articleId, user_id: userId };
}

export function getSummaryReviews() {
  const db = getDatabase();
  const rows = db.prepare(`
    SELECT sr.*, u.initials
    FROM summary_reviews sr
    LEFT JOIN users u ON sr.user_id = u.id
    ORDER BY sr.created_at DESC
  `).all();
  return rows.map(row => ({
    id: row.id,
    articleId: row.article_id,
    userId: row.user_id,
    userInitials: row.initials,
    ratings: JSON.parse(row.ratings),
    qualityRating: row.quality_rating,
    notes: row.notes,
    rubricId: row.rubric_id,
    rubricVersion: row.rubric_version,
    timestamp: row.created_at
  }));
}

export function getSummaryReviewsByArticle(articleId) {
  const db = getDatabase();
  const rows = db.prepare(`
    SELECT sr.*, u.initials
    FROM summary_reviews sr
    LEFT JOIN users u ON sr.user_id = u.id
    WHERE sr.article_id = ?
    ORDER BY sr.created_at DESC
  `).all(articleId);
  return rows.map(row => ({
    id: row.id,
    articleId: row.article_id,
    userId: row.user_id,
    userInitials: row.initials,
    ratings: JSON.parse(row.ratings),
    qualityRating: row.quality_rating,
    notes: row.notes,
    rubricId: row.rubric_id,
    rubricVersion: row.rubric_version,
    timestamp: row.created_at
  }));
}
