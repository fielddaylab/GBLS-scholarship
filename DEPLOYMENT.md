# GBLS Literature Reviewer - Deployment Guide

## Overview

The GBLS Literature Reviewer can run in multiple environments:
- **Local Development**: `http://localhost:8787`
- **Docker Local**: `http://localhost:8787`
- **Render.com Production**: `https://gamebasedlibraryservicesliterature.onrender.com`

All environments share the same codebase with environment-specific configuration.

## Quick Start

### Development (Localhost)

```bash
# Install dependencies
cd site
npm install

# Run development server
npm start
# or
node server.mjs

# Access at http://localhost:8787
```

### Docker Local

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8787

# View logs
docker logs gbls -f

# Stop
docker-compose down
```

### Render.com Production

```bash
# Deploy to Render
git push origin main

# Render automatically:
# 1. Pulls latest code
# 2. Installs dependencies
# 3. Starts application
# 4. Available at https://gamebasedlibraryservicesliterature.onrender.com
```

---

## Environment Configuration

### Development (.env)

```bash
NODE_ENV=development
PORT=8787
DEBUG_MODE=true
APP_URL=http://localhost:8787
SUBMISSIONS_DIR=./0_human_sources
CORPUS_DIR=../1_coded_gbls_corpus_articles
METRICS_DIR=../2_calculated_metrics
JWT_SECRET=dev-secret-key-not-secure
```

### Docker (.env or docker-compose.yml)

```yaml
environment:
  NODE_ENV: production
  PORT: 8787
  DEBUG_MODE: "true"  # Keep true for testing
  SUBMISSIONS_DIR: /app/submissions
  CORPUS_DIR: ../1_coded_gbls_corpus_articles
  METRICS_DIR: ../2_calculated_metrics
  JWT_SECRET: your-secure-random-key
```

### Render.com (render.yaml + Render Dashboard)

**render.yaml:**
```yaml
services:
  - type: web
    name: gbls-literature-reviewer
    runtime: node
    buildCommand: cd site && npm install
    startCommand: cd site && node server.mjs
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 8080
      - key: DEBUG_MODE
        value: "false"
```

**Render Dashboard Environment Variables:**
Set in Render dashboard (Settings → Environment):
- `JWT_SECRET` = random secure value
- `APP_URL` = (auto-set from RENDER_EXTERNAL_URL)

---

## Deployment Steps

### Deploy to Render.com

#### Initial Setup (One Time)

1. **Create Render Account**
   - Go to https://render.com
   - Connect GitHub account

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select repository: `gameBasedLibraryServicesLiterature`
   - Name: `gbls-literature-reviewer`
   - Runtime: `Node`
   - Build Command: `cd site && npm install`
   - Start Command: `cd site && node server.mjs`
   - Plan: Free (or Paid for production)
   - Click "Create Web Service"

3. **Set Environment Variables** (in Render Dashboard)
   - Go to Settings → Environment Variables
   - Add:
     ```
     NODE_ENV = production
     DEBUG_MODE = false
     JWT_SECRET = [generate random string]
     PORT = 8080
     ```

4. **Deploy**
   - Render auto-deploys when you push to main branch
   - Watch deployment logs in Render dashboard

#### Subsequent Deployments

Just push to main branch:
```bash
git add .
git commit -m "your message"
git push origin main
```

Render automatically:
1. Detects changes
2. Rebuilds application
3. Restarts service
4. Available at https://gamebasedlibraryservicesliterature.onrender.com

### Monitor Deployment

**In Render Dashboard:**
- Click "Logs" to see build & runtime logs
- Click "Metrics" to see CPU/Memory usage
- Check "Health" status

**From Command Line:**
```bash
# Check health
curl https://gamebasedlibraryservicesliterature.onrender.com/health

# Check logs (if using render CLI)
render logs --service=gbls-literature-reviewer
```

---

## Testing Both Environments

### Test Local Development

```bash
# Start app
cd site && npm start

# In browser
http://localhost:8787

# Test login
Email: dev@test.com
Expected: Auto-creates user with initials "DTE"
```

### Test Docker Local

```bash
# Start
docker-compose up -d

# In browser
http://localhost:8787

# Test login
Email: docker@test.com
Expected: Auto-creates user with initials "DOT"

# View database
docker exec gbls sqlite3 0_human_sources/users.db \
  "SELECT email, initials FROM users;"
```

### Test Render Production

```bash
# In browser
https://gamebasedlibraryservicesliterature.onrender.com

# Test login
Email: render@test.com
Expected: Auto-creates user with initials "RTE"

# Check health
curl https://gamebasedlibraryservicesliterature.onrender.com/health
```

---

## Disable Debug Mode (Before Production)

### Local Development
Edit `.env`:
```bash
DEBUG_MODE=false
```
Restart: `npm start`

### Docker
Edit `docker-compose.yml`:
```yaml
DEBUG_MODE: "false"
```
Restart: `docker-compose restart`

### Render.com
In Render Dashboard → Environment Variables:
- Change `DEBUG_MODE` from `true` to `false`
- Application auto-restarts
- Users now must register via `/register.html`

---

## Environment-Specific Behavior

### CORS Settings

All environments allow requests from:
- `http://localhost:8787`
- `http://localhost:3000`
- `https://gamebasedlibraryservicesliterature.onrender.com`

Add more origins in `site/server.mjs` if needed:
```javascript
const allowedOrigins = [
  'http://localhost:8787',
  'http://localhost:3000',
  'https://gamebasedlibraryservicesliterature.onrender.com',
  'https://yourdomain.com'  // Add here
];
```

### Database Location

| Environment | Database | Notes |
|-------------|----------|-------|
| Development | `./0_human_sources/users.db` | Local file |
| Docker | `/app/submissions/../0_human_sources/users.db` | Container volume |
| Render | `/tmp/submissions/../users.db` | Ephemeral (resets on rebuild) |

**Important:** Render's `/tmp` is ephemeral. For persistent database on Render, consider:
- Using PostgreSQL add-on
- Or external database service

### Session Cookies

| Environment | Secure | SameSite | Domain |
|-------------|--------|----------|--------|
| Development | false | lax | localhost |
| Docker | false | lax | localhost |
| Render | true | lax | .onrender.com |

---

## Troubleshooting

### App Won't Start Locally

```bash
# Check Node version
node --version  # Should be 20+

# Check dependencies
cd site && npm install

# Try running directly
node server.mjs

# Check for port conflicts
lsof -i :8787
```

### Docker Build Fails

```bash
# Clean build
docker-compose down
docker system prune -a
docker-compose build --no-cache

# Check logs
docker logs gbls
```

### Render Deployment Fails

1. Check Render Dashboard → Logs
2. Common issues:
   - Missing `render.yaml`
   - Wrong build command
   - Port not set to 8080
   - Node version incompatible

3. Common fixes:
   ```yaml
   # render.yaml
   services:
     - type: web
       runtime: node
       buildCommand: cd site && npm install
       startCommand: cd site && node server.mjs
   ```

### Database Issues

**Local/Docker:**
```bash
# Reset database
rm 0_human_sources/users.db
docker-compose restart  # for Docker
npm start               # for local
```

**Render:**
Database resets on rebuild. If needed, use external database:
1. Add PostgreSQL to Render
2. Set `DATABASE_URL` in environment
3. Update `db.mjs` to use PostgreSQL

### CORS Errors

Check that your origin is in `allowedOrigins` list in `server.mjs`.

Add domain in `allowedOrigins`:
```javascript
const allowedOrigins = [
  'http://localhost:8787',
  'https://gamebasedlibraryservicesliterature.onrender.com',
  'https://yourdomain.com'  // Add custom domains here
];
```

---

## Production Checklist

Before deploying to production:

### Security
- [ ] `DEBUG_MODE=false`
- [ ] `JWT_SECRET` = random secure value
- [ ] `NODE_ENV=production`
- [ ] HTTPS enabled (Render does this automatically)
- [ ] Database backed up

### Configuration
- [ ] All OAuth secrets set (if using)
- [ ] reCAPTCHA keys set (if using)
- [ ] Custom domain configured (if needed)
- [ ] CORS origins updated

### Testing
- [ ] Login/register works
- [ ] Users can submit articles
- [ ] Database persists data
- [ ] Logs look clean
- [ ] No security warnings

### Monitoring
- [ ] Logs checked
- [ ] Health endpoint working
- [ ] Error tracking set up
- [ ] Auto-restart configured

---

## Useful Commands

### Local Development
```bash
# Start
npm start

# Debug mode
DEBUG=* npm start

# Kill process on port 8787
lsof -i :8787
kill -9 <PID>
```

### Docker
```bash
# Build and start
docker-compose up -d

# View logs (live)
docker logs gbls -f

# Access container
docker exec -it gbls bash

# Check database
docker exec gbls sqlite3 /path/to/users.db ".tables"

# Stop
docker-compose down

# Clean everything
docker-compose down && rm -rf 0_human_sources/users.db
```

### Render
```bash
# View logs (requires Render CLI)
render logs --service=gbls-literature-reviewer

# Trigger manual deploy
# (Push to main branch, or use Render dashboard)

# Check health
curl https://gamebasedlibraryservicesliterature.onrender.com/health
```

---

## Multi-Environment Summary

| Feature | Local | Docker | Render |
|---------|-------|--------|--------|
| Database | File | Docker Volume | Ephemeral |
| Port | 8787 | 8787 | 8080 |
| Debug Mode | Yes | Yes | No |
| Auto-deploys | Manual | Manual | Git push |
| Scalability | Limited | Limited | Auto-scaling |
| Cost | Free | Free | Free (with limits) |
| Uptime | Dev only | Test | 24/7 |

---

## Getting Help

### Check Logs
```bash
# Local
npm start

# Docker
docker logs gbls -f

# Render
View in Render Dashboard → Logs
```

### Common Issues

**Port already in use:**
```bash
lsof -i :8787
kill -9 <PID>
```

**Module not found:**
```bash
cd site && npm install
```

**Database locked:**
```bash
docker-compose restart
```

**Out of disk space (Render):**
- Clear build cache in Render dashboard
- Or delete and recreate service

---

## Next Steps

1. **Test Locally**: Run on localhost, verify functionality
2. **Test Docker**: Deploy locally with Docker Compose
3. **Deploy to Render**: Push to main, watch auto-deploy
4. **Disable Debug**: Set `DEBUG_MODE=false` on Render
5. **Configure OAuth**: Add GitHub/Google credentials
6. **Monitor Production**: Watch logs and metrics
