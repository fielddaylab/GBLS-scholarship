# GBLS Literature Reviewer - Authentication System

## Overview

The GBLS Literature Reviewer now includes a comprehensive user authentication and registration system. All users must register and log in to access the application. User 3-letter initials serve as the contribution code for all submissions.

## Features

### User Registration
- **Full Name**: Required
- **Email**: Required (used as username for login)
- **3-Letter Initials**: Required unique identifier (becomes contribution code)
- **Organizational Affiliation**: Optional
- **reCAPTCHA**: Optional verification
- **Email Validation**: Built-in validation

### Authentication Methods
1. **Email-based**: Direct login with email address
2. **GitHub OAuth**: Sign in with GitHub account (structure ready, requires configuration)
3. **Google OAuth**: Sign in with Google account (structure ready, requires configuration)

### Session Management
- **JWT Tokens**: Secure token-based authentication
- **HTTP-Only Cookies**: Tokens stored securely in cookies
- **24-hour Sessions**: Automatic expiration after 24 hours
- **Persistent Login**: Sessions persist across page reloads

## Database

### SQLite Storage
- Stored at: `0_human_sources/users.db`
- Tables:
  - `users`: Stores user profiles with OAuth integration
  - `sessions`: Manages active sessions

### User Fields
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE,
  full_name TEXT,
  initials TEXT UNIQUE,
  organizational_affiliation TEXT,
  github_id TEXT UNIQUE,
  google_id TEXT UNIQUE,
  created_at DATETIME,
  last_login DATETIME,
  is_active BOOLEAN
);
```

## Setup Instructions

### Local Development

1. **Install Dependencies**
   ```bash
   cd site
   npm install
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run Application**
   ```bash
   npm start
   # or
   node server.mjs
   ```

4. **Access Application**
   - Navigate to http://localhost:8787
   - You'll be redirected to login page
   - Register new account or log in

### Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

2. **Access Application**
   - Navigate to http://localhost:8787
   - Same login/registration flow

## Configuring OAuth Providers

### GitHub OAuth Setup

1. **Create OAuth Application**
   - Go to https://github.com/settings/developers
   - Click "New OAuth App"
   - Fill in application details:
     - **Application name**: GBLS Literature Reviewer
     - **Homepage URL**: http://localhost:8787 (or your domain)
     - **Authorization callback URL**: http://localhost:8787/auth/github/callback

2. **Get Credentials**
   - Client ID and Client Secret will be generated
   - Add to `.env` file:
     ```
     GITHUB_CLIENT_ID=your_client_id
     GITHUB_CLIENT_SECRET=your_client_secret
     ```

3. **Implementation** (when ready)
   - Update `auth.mjs` handleGithubAuth function
   - Implement OAuth flow in server routes
   - Test GitHub login

### Google OAuth Setup

1. **Create OAuth Credentials**
   - Go to https://console.cloud.google.com/
   - Create new project or select existing
   - Enable OAuth 2.0
   - Create OAuth 2.0 credentials:
     - Type: Web application
     - Authorized redirect URIs: http://localhost:8787/auth/google/callback

2. **Get Credentials**
   - Client ID and Client Secret will be generated
   - Add to `.env` file:
     ```
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```

3. **Frontend Integration**
   - Replace `{{ GOOGLE_CLIENT_ID }}` in `register.html`
   - Add Google Sign-In library (already included)

### reCAPTCHA Setup (Optional)

1. **Register Site**
   - Go to https://www.google.com/recaptcha/admin
   - Add new site
   - Choose reCAPTCHA v3
   - Add domains

2. **Get Keys**
   - Site Key: Add to registration form
   - Secret Key: Add to environment:
     ```
     RECAPTCHA_SITE_KEY=your_site_key
     RECAPTCHA_SECRET_KEY=your_secret_key
     ```

## Debug Mode (Development Only)

### Enabling Debug Mode
Set environment variable:
```bash
DEBUG_MODE=true
```

### How It Works
When debug mode is enabled:
1. User can log in with **any email address**
2. If user doesn't exist, they're created automatically
3. 3-letter initials auto-generated from email
4. Full name auto-generated from email prefix

### Auto-Generated Initials
- `john.smith@example.com` → Full Name: "john smith" → Initials: "JSM"
- `alice.johnson.dev@company.com` → Full Name: "alice johnson dev" → Initials: "AJD"
- `test@example.com` → Full Name: "test" → Initials: "TES"

### Disabling Debug Mode
When configuration is complete:
```bash
DEBUG_MODE=false
```

Users will then need to:
- Use registration form at `/register.html`
- Or use configured OAuth providers

**⚠️ Important:** Always disable debug mode before production deployment!

## User Flow

### Registration
1. User navigates to `/register.html`
2. Fills in form with:
   - Full name
   - Email
   - 3-letter initials (checked for availability)
   - Optional organization
   - reCAPTCHA (if enabled)
3. System creates user account
4. User is logged in automatically
5. Redirected to main application

### Login
1. User navigates to `/login.html`
2. Enters email address
3. System finds user and creates session
4. Logged in, redirected to main application

### Logout
1. User clicks "Logout" button in header
2. Session cookie is cleared
3. Redirected to login page

## Contribution Tracking

### Initials as Contribution Code
- User's 3-letter initials automatically used in all submissions
- Visible in:
  - User menu (top right)
  - All submitted codings
  - All submitted summary reviews
- No manual entry needed

### Submission Data
All submissions include:
- `userId`: User's database ID
- `userInitials`: User's 3-letter code
- `timestamp`: When submission was made
- Automatically tracked in submission files

## Security Considerations

### Password Security
- No passwords stored (OAuth-based or email verification)
- JWT tokens use secure signing
- Tokens expire after 24 hours

### Session Security
- HTTP-only cookies prevent XSS attacks
- Secure flag on cookies (production)
- SameSite protection enabled
- CSRF tokens available if needed

### Database
- SQLite with WAL mode for consistency
- User data encrypted at rest (recommended in production)
- Database file: `0_human_sources/users.db`

## Troubleshooting

### Database Issues
```bash
# Database location
ls -la 0_human_sources/users.db

# Check permissions
chmod 666 0_human_sources/users.db
```

### Session Problems
- Clear browser cookies
- Check JWT_SECRET is consistent
- Verify cookie settings in browser

### OAuth Login Fails
1. Verify callback URLs match exactly
2. Check Client ID/Secret are correct
3. Look for errors in server logs
4. Ensure environment variables are loaded

### reCAPTCHA Issues
- Verify domain is registered
- Check site key matches in HTML
- Ensure secret key is in environment

## API Endpoints

### Authentication Endpoints (Public)
- `POST /api/register` - Create new account
- `POST /api/login` - Log in with email
- `POST /api/logout` - Log out
- `GET /api/check-initials` - Check if initials available
- `GET /auth/github/callback` - GitHub OAuth callback
- `GET /auth/google/callback` - Google OAuth callback

### Protected Endpoints (Require Auth)
- `GET /api/user` - Get current user info
- `GET /api/metrics` - Access metrics
- `GET /api/articles` - Access articles
- `POST /api/summaries` - Submit summary review
- `POST /api/codings` - Submit article coding

## Future Enhancements

1. **OAuth Completion**
   - Finish GitHub OAuth implementation
   - Finish Google OAuth implementation
   - Link existing accounts to OAuth

2. **Account Management**
   - User profile page
   - Change email
   - Update organizational affiliation
   - Password reset (if adding passwords)

3. **Admin Features**
   - User management dashboard
   - Analytics on contributions
   - Bulk user import

4. **Advanced Security**
   - Two-factor authentication
   - Email verification on registration
   - Audit logging
   - IP-based restrictions

## Support

For issues or questions:
1. Check logs: `docker logs gbls`
2. Verify environment variables: `echo $JWT_SECRET`
3. Test database: `sqlite3 0_human_sources/users.db ".tables"`
4. Review auth.mjs for authentication logic
5. Check server.mjs for route implementations
