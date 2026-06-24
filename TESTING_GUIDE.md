# GBLS Literature Reviewer - Multi-Environment Testing Guide

## Testing Environments

You now have three environments to test:

| Environment | URL | Status | Debug Mode |
|-------------|-----|--------|-----------|
| **Local Dev** | http://localhost:8787 | Running (npm start) | ✅ Enabled |
| **Docker Local** | http://localhost:8787 | Running (docker-compose) | ✅ Enabled |
| **Render.com** | https://gamebasedlibraryservicesliterature.onrender.com | Running (auto-deployed) | ✅ Enabled |

---

## Test 1: Quick Login (All Environments)

### Objective
Verify that users can log in with email and auto-generated initials.

### Steps

1. **Navigate to login page**
   - Local Dev: http://localhost:8787/login.html
   - Docker: http://localhost:8787/login.html
   - Render: https://gamebasedlibraryservicesliterature.onrender.com/login.html

2. **Enter test email**
   ```
   admin@gbls.edu
   ```

3. **Click Sign In**

4. **Expected Result**
   - User created with initials: **ADM**
   - Redirected to main dashboard
   - User menu shows: "admin (ADM)"

### Pass/Fail Criteria
- ✅ Login successful
- ✅ Initials generated correctly
- ✅ User menu displays correctly
- ✅ No errors in console

---

## Test 2: Metrics Dashboard

### Objective
Verify that the GBLS Corpus Explorer loads and displays metrics.

### Steps

1. **From login page, log in with**
   ```
   metrics@test.com
   ```

2. **Click "GBLS Lit Explorer" tab**

3. **Verify displayed metrics:**
   - Total Articles: 224
   - Year Range: 1950 - 2025
   - Unique Features: 103
   - Avg Features: 10.6

4. **Test filters:**
   - Change "Service Area" dropdown
   - Articles should update
   - Verify metrics change accordingly

### Pass/Fail Criteria
- ✅ All metrics display correctly
- ✅ Filtering works
- ✅ Articles update on filter change
- ✅ No console errors

---

## Test 3: Submit Article Review

### Objective
Verify that users can submit summary reviews with their initials.

### Steps

1. **Logged in as previous user**

2. **Click "Review Summaries" tab**

3. **Select an article** from dropdown

4. **Rate the summary** (e.g., select quality level)

5. **Add reviewer notes** (optional)

6. **Click Submit**

7. **Expected messages:**
   - "Summary review submitted successfully!"
   - Initials in submission: **MTE** (from metrics@test.com)

### Verify Submission Saved

```bash
# Local/Docker
sqlite3 0_human_sources/users.db \
  "SELECT * FROM users WHERE email = 'metrics@test.com';"

# Check submission file
ls -la 0_human_sources/submitted_summary_reviews.json
```

### Pass/Fail Criteria
- ✅ Submission accepted
- ✅ Success message shown
- ✅ User initials included
- ✅ File saved with correct data

---

## Test 4: Submit Article Classification

### Objective
Verify that users can code articles and submit classifications.

### Steps

1. **Logged in as new user**
   ```
   classifier@test.com
   ```

2. **Click "Review Classifications" tab**

3. **User menu shows:** "classifier (CTE)"

4. **Select an article**

5. **Add some ratings/codes** (select options from form)

6. **Click Submit**

7. **Expected result:**
   - "Classification submitted successfully!"
   - Initials in data: **CTE**

### Verify Database

```bash
# Check user was created
docker exec gbls sqlite3 /app/submissions/../0_human_sources/users.db \
  "SELECT * FROM users WHERE email = 'classifier@test.com';"
```

### Pass/Fail Criteria
- ✅ Can select article
- ✅ Can submit codes
- ✅ User initials included
- ✅ Success message shown
- ✅ Data persisted

---

## Test 5: Multiple Users (Initials Conflict)

### Objective
Verify that system handles duplicate initials correctly.

### Steps

1. **User 1 Login:**
   ```
   john@test.com → Initials: JTE
   ```

2. **Logout and User 2 Login:**
   ```
   jane@test.com → Initials: JTE (conflict!)
   ```

3. **Expected behavior:**
   - ✅ System prevents duplicate initials
   - OR ✅ System assigns similar alternative

### Pass/Fail Criteria
- ✅ Handles initials conflict gracefully
- ✅ No database errors
- ✅ User gets unique identifier

---

## Test 6: Logout Functionality

### Objective
Verify that logout clears session and requires re-login.

### Steps

1. **Click user menu** (top-right)

2. **Click "Logout"**

3. **Expected behavior:**
   - Redirected to login page
   - Cookie cleared
   - Session ended

4. **Verify redirect:**
   - URL should be /login.html
   - No user menu visible

5. **Try accessing app directly:**
   ```
   http://localhost:8787
   ```
   - Should redirect to login

### Pass/Fail Criteria
- ✅ Logout works
- ✅ Redirected to login
- ✅ Cookie cleared
- ✅ Cannot access app without login

---

## Test 7: Cross-Environment Consistency

### Objective
Verify that all three environments behave identically.

### Steps

1. **Repeat Test 1-4 on each environment:**
   - Local Dev
   - Docker Local
   - Render.com

2. **Compare results:**
   - All show same metrics (224 articles)
   - All accept logins the same way
   - All generate initials correctly
   - All create submissions

### Expected Results
All three environments should:
- ✅ Display same 224 articles
- ✅ Show same metrics
- ✅ Accept logins identically
- ✅ Generate same initials
- ✅ Save submissions with user info

### Notes
- Render database is ephemeral (resets on rebuild)
- Local databases persist independently
- That's expected and acceptable for testing

---

## Test 8: API Endpoints (Advanced)

### Objective
Verify that API endpoints work correctly.

### Local Testing

```bash
# 1. Test health endpoint
curl http://localhost:8787/health
# Expected: {"ok":true}

# 2. Test login API
RESPONSE=$(curl -s -X POST http://localhost:8787/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"api@test.com"}')

echo $RESPONSE | jq '.user.initials'
# Expected: "ATE"

# 3. Extract token
TOKEN=$(echo $RESPONSE | jq -r '.user.id')

# 4. Test protected endpoint (get current user)
curl -s -H "Cookie: auth_token=$TOKEN" \
  http://localhost:8787/api/user | jq '.initials'
# Expected: "ATE"

# 5. Test metrics endpoint
curl -s -H "Cookie: auth_token=$TOKEN" \
  http://localhost:8787/api/metrics | jq '.summary'
# Expected: {"total_articles": 224, ...}
```

### Render Testing

```bash
# Same commands but replace localhost with Render URL
curl https://gamebasedlibraryservicesliterature.onrender.com/health
```

### Pass/Fail Criteria
- ✅ Health check works
- ✅ Login returns user data
- ✅ Token is valid
- ✅ Protected endpoints require auth
- ✅ Metrics data returns correctly

---

## Test 9: Debug Mode Behavior

### Objective
Verify debug mode works as expected.

### Current State: DEBUG_MODE=true

```bash
# Anyone can login with any email
Email: anything@anywhere.com
Result: User created with auto-generated initials
```

### Expected Behavior

| Email | Full Name | Initials |
|-------|-----------|----------|
| john.smith@test.com | john smith | JOS |
| alice.johnson@company.com | alice johnson | AJO |
| bob@gmail.com | bob | BOB |
| test.user.dev@local.host | test user dev | TUD |

### Pass/Fail Criteria
- ✅ Any email accepted
- ✅ User auto-created
- ✅ Initials auto-generated
- ✅ No registration needed

---

## Test 10: Security & Cookies

### Objective
Verify that authentication cookies work correctly.

### Steps

1. **Open DevTools** (F12)

2. **Go to Application → Cookies**

3. **Login with email**

4. **Check cookie:**
   - Name: `auth_token`
   - HttpOnly: ✅ Yes (can't access from JS)
   - Secure: ✅ Yes (only HTTPS in production)
   - SameSite: `Lax`
   - MaxAge: 24 hours

5. **Clear cookie manually**
   - Delete `auth_token`
   - Refresh page
   - Should redirect to login

### Pass/Fail Criteria
- ✅ Cookie is HttpOnly
- ✅ Cookie has proper flags
- ✅ Clearing cookie requires re-login
- ✅ Session properly invalidated

---

## Test Checklist

### Basic Functionality
- [ ] Local Dev: Login works
- [ ] Docker: Login works
- [ ] Render: Login works
- [ ] Initials generated correctly
- [ ] User menu displays
- [ ] Logout works

### Features
- [ ] Metrics display (224 articles)
- [ ] Can filter by category
- [ ] Can submit reviews
- [ ] Can submit classifications
- [ ] Submissions include user initials
- [ ] Database persists data

### Security
- [ ] Session requires login
- [ ] Logout clears session
- [ ] Protected routes work
- [ ] Cookies are secure
- [ ] CORS allows correct domains

### Cross-Environment
- [ ] Local, Docker, Render all match
- [ ] Same metrics in all environments
- [ ] Same login behavior
- [ ] Same submission tracking

---

## Troubleshooting Test Failures

### Login Not Working

```bash
# Check server is running
curl http://localhost:8787/health

# Check logs
# Local: npm start (look at console)
# Docker: docker logs gbls -f
# Render: Render Dashboard → Logs

# Check debug mode
docker exec gbls env | grep DEBUG_MODE
```

### Metrics Not Loading

```bash
# Check API endpoint
curl http://localhost:8787/api/metrics \
  -H "Cookie: auth_token=YOUR_TOKEN"

# Check files exist
ls -la 2_calculated_metrics/gbls_corpus_metrics/
```

### Submission Not Saving

```bash
# Check submissions directory exists
docker exec gbls ls -la /app/submissions/

# Check database
docker exec gbls sqlite3 /app/submissions/../0_human_sources/users.db \
  "SELECT * FROM users;"
```

### Cookie Issues

```bash
# Check browser dev tools:
# DevTools → Application → Cookies
# Should see auth_token
# Should be HttpOnly=Yes

# If missing, browser may be blocking cookies
# Try incognito window
# Or check browser cookie settings
```

---

## Performance Testing

### Load Time

Test with DevTools Network tab:

| Environment | Load Time | Time to Interactive |
|-------------|-----------|-------------------|
| Local Dev | <200ms | <500ms |
| Docker | <200ms | <500ms |
| Render | <500ms | <1000ms |

### Database Performance

```bash
# Check database size
ls -lh 0_human_sources/users.db

# Should be small (<1MB)
# If large, users table has lots of test data

# Clean for testing
rm 0_human_sources/users.db
docker-compose restart
```

---

## Automated Testing (Optional)

```bash
#!/bin/bash
# test.sh - Simple test script

BASE_URL=${1:-http://localhost:8787}

echo "Testing: $BASE_URL"

# Test health
echo -n "Health: "
curl -s $BASE_URL/health | jq '.ok'

# Test login
echo -n "Login: "
curl -s -X POST $BASE_URL/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com"}' | jq '.user.email'

echo "✓ Basic tests passed"
```

Usage:
```bash
bash test.sh http://localhost:8787          # Local
bash test.sh http://localhost:8787          # Docker
bash test.sh https://gamebasedlibraryservicesliterature.onrender.com  # Render
```

---

## Summary

You now have a comprehensive testing strategy for three environments. Use this guide to:

1. ✅ **Verify functionality** works across all environments
2. ✅ **Identify environment-specific issues** (if any)
3. ✅ **Ensure consistency** between deployments
4. ✅ **Test security** and authentication
5. ✅ **Validate submissions** are tracked correctly

All environments should behave identically with debug mode enabled. When you're ready for production, disable debug mode and users will need to register.
