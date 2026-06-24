# GBLS Literature Reviewer - Quick Start Guide

## For End Users

### Access the Application
1. Open browser and go to: **http://localhost:8787**
2. You'll be redirected to the login page

### First Time Login (Debug Mode)
1. Enter any email address (e.g., `yourname@example.com`)
2. Click "Sign In"
3. Account is created automatically
4. You'll be logged in and see the dashboard

### Your 3-Letter Code
Your unique contribution code is automatically generated from your email:
- `john.smith@test.com` → Code: **JOS**
- `alice.dev@company.com` → Code: **ADE**

This code automatically appears in all your submissions.

### Main Features

#### Tab 1: GBLS Lit Explorer
- Browse and filter the 224-article corpus
- View metrics by different categories
- Search articles by features
- No submissions here (read-only)

#### Tab 2: Review Summaries
- Review existing article summaries
- Rate summary quality
- Add reviewer notes
- Submit feedback

#### Tab 3: Review Classifications
- Code articles with quality ratings
- Select metadata classifications
- Submit article codings
- All tracked with your code

#### Tab 4: View Classifications
- See all submitted classifications
- Filter by contributor code
- Browse historical submissions

### Logging Out
Click your name in the top-right corner and click "Logout"

---

## For Administrators

### Initial Setup
```bash
# Already done! Just start:
docker-compose up -d

# Verify it's running:
curl http://localhost:8787/health
```

### Disable Debug Mode (Before Production)
1. Edit `docker-compose.yml`
2. Change: `DEBUG_MODE: "false"`
3. Restart:
   ```bash
   docker-compose restart
   ```

### Reset User Database
```bash
# Stop containers
docker-compose down

# Delete database
rm 0_human_sources/users.db

# Restart
docker-compose up -d
```

### View User Database
```bash
# List all users
docker exec gbls sqlite3 /app/submissions/../0_human_sources/users.db \
  "SELECT id, email, full_name, initials FROM users;"

# Or on local:
sqlite3 0_human_sources/users.db \
  "SELECT id, email, full_name, initials FROM users;"
```

### Check Logs
```bash
docker logs gbls -f
```

---

## Common Test Scenarios

### Test 1: Quick Login
1. Go to http://localhost:8787
2. Enter: `demo@test.com`
3. Click Sign In
4. Should see dashboard with "demo" user and "DTE" initials

### Test 2: Submit Article Coding
1. Login with any email
2. Go to "Review Classifications" tab
3. Select an article
4. Add some ratings/codes
5. Click Submit
6. See success message
7. Data saved with your initials

### Test 3: Multiple Users
1. Login with `user1@test.com` → Code: UTT
2. Logout
3. Login with `user2@test.com` → Code: UTT (same - they'll fail!)
4. Try `alice.bob@test.com` → Code: ABO (works!)
5. Logout
6. Login with `user1@test.com` again (same user)

### Test 4: Protected Routes
1. Open DevTools (F12)
2. Go to Console
3. Clear all cookies (dev tools → Application → Cookies → Delete)
4. Refresh page
5. Should redirect to login page
6. Proves routes are protected ✓

---

## API Testing (Advanced)

### Quick Login API
```bash
curl -X POST http://localhost:8787/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}' \
  | jq '.user'
```

### Get Current User
```bash
# After login, get the auth_token cookie, then:
curl http://localhost:8787/api/user \
  -H "Cookie: auth_token=YOUR_TOKEN_HERE" \
  | jq '.'
```

### Access Protected Metrics
```bash
curl http://localhost:8787/api/metrics \
  -H "Cookie: auth_token=YOUR_TOKEN_HERE" \
  | jq '.summary'
```

---

## Troubleshooting

### "User not found" Error
- **Cause**: Debug mode disabled
- **Solution**: Enable DEBUG_MODE in docker-compose.yml

### Can't Access Application
- **Cause**: Not logged in
- **Solution**: Go to http://localhost:8787/login.html

### Initials Conflict
- **Cause**: Auto-generated initials already taken
- **Solution**: Use different email with different initials

### Database Locked Error
- **Cause**: Multiple processes accessing database
- **Solution**: Restart Docker: `docker-compose restart`

### Forgot Your Code
- **Cause**: Need to know your 3-letter initials
- **Solution**: Look at user menu in top-right (shows initials)

---

## Features by Role

### Researcher (End User)
- ✅ Login with email
- ✅ Browse GBLS corpus
- ✅ Submit article reviews
- ✅ Submit article codes
- ✅ View your submissions
- ❌ Can't see other users' data (just summaries)
- ❌ Can't manage accounts

### Administrator
- ✅ All researcher features
- ✅ View all user accounts
- ✅ Reset database
- ✅ Check logs
- ✅ Enable/disable debug mode
- ✅ Configure environment
- ✅ Backup database

---

## What Happens Behind the Scenes

### When You Login
1. Browser sends email to server
2. Server checks if user exists
3. If not (in debug mode), creates user with auto-generated name & initials
4. Creates JWT token (24-hour expiration)
5. Sends token in HTTP-only cookie
6. Browser stores cookie
7. You're logged in!

### When You Submit
1. Data sent with your user ID
2. Your 3-letter initials included automatically
3. Saved to `0_human_sources/submitted_*.json`
4. Timestamp recorded
5. Tracked in database

### When You Logout
1. Session cookie deleted
2. You're redirected to login page
3. Next request requires new login
4. Token is invalidated

---

## Production Checklist

Before going live:
- [ ] Set `DEBUG_MODE=false`
- [ ] Change `JWT_SECRET` to random value
- [ ] Enable HTTPS
- [ ] Review security settings
- [ ] Test with real email validation
- [ ] Set up automated backups
- [ ] Create admin account
- [ ] Test OAuth providers (optional)
- [ ] Configure reCAPTCHA (optional)
- [ ] Review logs for security
- [ ] Document user procedures
- [ ] Create user accounts for all researchers

---

## Questions?

See full documentation:
- **AUTH.md** - Authentication details
- **IMPLEMENTATION_SUMMARY.md** - Technical summary
- **README.md** - Project overview

Or check logs:
```bash
docker logs gbls -f
```
