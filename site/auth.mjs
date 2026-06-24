import { JWT_SECRET, DEBUG_MODE, isProduction, getEnv } from './config.mjs';
import jwt from 'jsonwebtoken';
import axios from 'axios';
import {
  createUser,
  getUserByEmail,
  getUserByGithubId,
  getUserByGoogleId,
  updateUserLastLogin,
  createSession,
  getSession,
  deleteSession,
  isInitialsTaken
} from './db.mjs';

// JWT_SECRET, DEBUG_MODE, isProduction imported from config.mjs
const SESSION_DURATION = 24 * 60 * 60 * 1000; // 24 hours

export function createToken(userId) {
  return jwt.sign(
    { userId, iat: Math.floor(Date.now() / 1000) },
    JWT_SECRET,
    { expiresIn: '24h' }
  );
}

export function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

export async function handleGithubAuth(githubProfile) {
  const { id: githubId, emails, name } = githubProfile;
  const email = emails?.[0]?.value;

  if (!email) {
    throw new Error('Could not retrieve email from GitHub');
  }

  // Check if user exists
  let user = getUserByGithubId(githubId);

  if (!user) {
    // Check if email exists
    user = getUserByEmail(email);

    if (user) {
      // User exists with same email, link GitHub
      // Note: In a real app, you'd update the user record to link GitHub
      // For now, just use existing user
    } else {
      // Create new user from GitHub profile
      const initials = generateInitialsFromName(name);
      user = createUser(email, name, initials, null, githubId);
    }
  }

  updateUserLastLogin(user.id);
  const token = createToken(user.id);

  return { user, token };
}

export async function handleGoogleAuth(googleProfile) {
  const { sub: googleId, email, name } = googleProfile;

  if (!email) {
    throw new Error('Could not retrieve email from Google');
  }

  // Check if user exists
  let user = getUserByGoogleId(googleId);

  if (!user) {
    // Check if email exists
    user = getUserByEmail(email);

    if (user) {
      // User exists with same email, link Google
      // Note: In a real app, you'd update the user record
    } else {
      // Create new user from Google profile
      const initials = generateInitialsFromName(name);
      user = createUser(email, name, initials, null, null, googleId);
    }
  }

  updateUserLastLogin(user.id);
  const token = createToken(user.id);

  return { user, token };
}

export async function debugLogin(testEmail = 'debug@localhost') {
  if (!DEBUG_MODE) {
    throw new Error('Debug login only available in debug mode');
  }

  let user = getUserByEmail(testEmail);

  if (!user) {
    // Auto-create debug test user
    const fullName = 'Debug Tester';
    const initials = 'DBG';
    user = createUser(testEmail, fullName, initials, 'Debug');
  }

  updateUserLastLogin(user.id);
  const token = createToken(user.id);

  return { user, token };
}

function generateInitialsFromName(name) {
  if (!name) return 'XXX';

  const parts = name.split(/\s+/).filter(p => p.length > 0);
  if (parts.length === 0) return 'XXX';

  if (parts.length === 1) {
    // Single name: use first 3 letters
    return parts[0].substring(0, 3).toUpperCase();
  }

  if (parts.length === 2) {
    // Two names: first letter + first letter of last + middle
    return (parts[0][0] + parts[1][0] + parts[0][1]).toUpperCase();
  }

  // Three or more names: first letter of each
  return parts.slice(0, 3).map(p => p[0]).join('').toUpperCase();
}

export function setSessionCookie(res, token) {
  res.cookie('auth_token', token, {
    httpOnly: true,
    secure: isProduction,
    sameSite: 'lax',
    maxAge: SESSION_DURATION,
    path: '/'
  });
}

export function clearSessionCookie(res) {
  res.clearCookie('auth_token', { path: '/' });
}
