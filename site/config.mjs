// Centralized application configuration.
//
// Design goals:
//   - Secrets only in .env (local) or Render secret env vars (production).
//   - All paths and structural defaults are hardcoded here — no need to set
//     CORPUS_DIR, METRICS_DIR, PORT, APP_URL, etc. in any config file.
//   - DATA_DIR auto-detects the Render persistent disk mount; falls back to
//     a local ./data directory for development.
//
// .env loading strategy:
//   1. Look for a .env file (project root → site/ → cwd) and load it.
//   2. dotenv does NOT override variables already in process.env, so on
//      Render (no .env file, secrets injected by platform) this is a no-op.

import { existsSync, mkdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Absolute path to the repo root (one level above site/).
export const REPO_ROOT = path.resolve(__dirname, '..');

// ---------------------------------------------------------------------------
// .env loading
// ---------------------------------------------------------------------------
const envCandidates = [
  path.join(REPO_ROOT, '.env'),   // project root  ← preferred
  path.join(__dirname, '.env'),   // site/
  path.join(process.cwd(), '.env')
];
const loadedEnvPath = envCandidates.find((p) => existsSync(p));

if (loadedEnvPath) {
  dotenv.config({ path: loadedEnvPath });
  console.log(`🔧 Loaded environment from ${loadedEnvPath}`);
} else {
  console.log('🔧 No .env file found — using platform environment (Render secrets)');
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Return env var value, or fallback if unset/empty. */
export function getEnv(key, fallback) {
  const v = process.env[key];
  return v === undefined || v === '' ? fallback : v;
}

/** True when the env var is set to a non-empty value. */
export function hasEnv(key) {
  return process.env[key] !== undefined && process.env[key] !== '';
}

// ---------------------------------------------------------------------------
// Environment detection
// ---------------------------------------------------------------------------

/** True on Render.com — platform sets RENDER=true automatically. */
export const isRender = !!process.env.RENDER || !!process.env.RENDER_EXTERNAL_URL;

/** True in any production context (Render or Docker with NODE_ENV=production). */
export const isProduction = process.env.NODE_ENV === 'production' || isRender;

// ---------------------------------------------------------------------------
// Hardcoded structural paths (same in every environment — no config needed)
// ---------------------------------------------------------------------------

/** Read-only corpus that ships with the repo. */
export const CORPUS_DIR = path.join(REPO_ROOT, '1_coded_gbls_corpus_articles');

/** Read-only pre-calculated metrics that ship with the repo. */
export const METRICS_DIR = path.join(REPO_ROOT, '2_calculated_metrics');

// ---------------------------------------------------------------------------
// Data root (user-created data: database + submissions)
// ---------------------------------------------------------------------------
// Default resolution:
//   1. DATA_DIR env var (set as a Render secret or in local .env)
//   2. /mnt/persistent  when running on Render (disk is mounted there)
//   3. <repo>/data      for local development / Docker
//
// DB_PATH and SUBMISSIONS_DIR can be overridden individually, but in normal
// use they always live under DATA_DIR.

const defaultDataDir = isRender ? '/mnt/persistent' : path.join(REPO_ROOT, 'data');

/** Absolute path to the persistent data root. */
export const DATA_DIR = path.resolve(getEnv('DATA_DIR', defaultDataDir));

/** Absolute path to the SQLite database file. */
export const DB_PATH = path.resolve(getEnv('DB_PATH', path.join(DATA_DIR, 'database.sqlite')));

/** Absolute path to the submissions directory. */
export const SUBMISSIONS_DIR = path.resolve(
  getEnv('SUBMISSIONS_DIR', path.join(DATA_DIR, 'submissions'))
);

// ---------------------------------------------------------------------------
// Server
// ---------------------------------------------------------------------------

export const PORT = parseInt(getEnv('PORT', '8787'), 10);

export const APP_URL =
  getEnv('APP_URL') ||
  process.env.RENDER_EXTERNAL_URL ||
  (isProduction
    ? 'https://gamebasedlibraryservicesliterature.onrender.com'
    : `http://localhost:${PORT}`);

/** Debug mode lets any email log in without registration. DEFAULT: false. */
export const DEBUG_MODE = getEnv('DEBUG_MODE', 'false') === 'true';

// ---------------------------------------------------------------------------
// Secrets (must be provided via .env or Render secret env vars)
// ---------------------------------------------------------------------------

export const JWT_SECRET = getEnv('JWT_SECRET', 'change-me-in-production');

// ---------------------------------------------------------------------------
// Utility: ensure a data directory exists
// ---------------------------------------------------------------------------

/**
 * Create a directory if it does not exist.  In production, refuses to fall
 * back silently if the target is unavailable — a missing persistent disk
 * should fail loudly, not write to ephemeral storage.
 *
 * @param {string} dir     Target directory path.
 * @param {object} opts
 * @param {string} opts.label    Human-readable label for log messages.
 * @param {string} [opts.fallback]  Dev-only fallback directory.
 * @returns {Promise<string>}  The directory actually used.
 */
export async function ensureDataDir(dir, { label = 'data', fallback } = {}) {
  const { mkdir } = await import('fs/promises');
  try {
    await mkdir(dir, { recursive: true });
    return dir;
  } catch (error) {
    if (error.code !== 'EACCES' && error.code !== 'ENOENT') throw error;

    if (isProduction) {
      throw new Error(
        `FATAL: ${label} directory "${dir}" is not usable (${error.code}). ` +
        `Refusing to fall back to ephemeral storage in production. ` +
        `Verify the persistent disk is mounted and DATA_DIR is set correctly.`
      );
    }

    const target = fallback || path.join(REPO_ROOT, 'data', label);
    console.warn(`Cannot use ${label} dir ${dir} (${error.code}); falling back to ${target}`);
    await mkdir(target, { recursive: true });
    return target;
  }
}

export const loadedFrom = loadedEnvPath ?? null;
