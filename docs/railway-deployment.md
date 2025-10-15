# Railway Deployment Guide

This guide explains how to deploy Aegra to Railway, a modern platform for deploying applications with zero configuration.

## Prerequisites

- A [Railway account](https://railway.app)
- Railway CLI (optional, but recommended): `npm install -g @railway/cli`
- Git repository for your Aegra instance

## Quick Deploy

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway configuration"
   git push origin main
   ```

2. **Create a new project on Railway**
   - Go to [railway.app/new](https://railway.app/new)
   - Click "Deploy from GitHub repo"
   - Select your Aegra repository
   - Railway will automatically detect the `railway.json` and `Dockerfile`

3. **Add PostgreSQL database**
   - In your Railway project dashboard, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Configure environment variables**

   Railway automatically provides `DATABASE_URL` and `PORT`. You need to add:

   ```bash
   # Required
   OPENAI_API_KEY=sk-...
   AUTH_TYPE=noop

   # Optional
   DEBUG=false
   LANGFUSE_LOGGING=true
   LANGFUSE_SECRET_KEY=sk-...
   LANGFUSE_PUBLIC_KEY=pk-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

   Add these in the Railway dashboard under "Variables" tab.

5. **Deploy**
   - Railway will automatically build and deploy your application
   - Database migrations run automatically on startup
   - Monitor the deployment in the "Deployments" tab

### Option 2: Deploy with Railway CLI

```bash
# Login to Railway
railway login

# Initialize a new project
railway init

# Link to an existing project (if applicable)
railway link

# Add PostgreSQL
railway add -d postgres

# Set environment variables
railway variables set OPENAI_API_KEY=sk-...
railway variables set AUTH_TYPE=noop

# Deploy
railway up
```

## Environment Variables

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string (from Railway Postgres)
- `PORT` - Port to bind the application (dynamically assigned)
- `RAILWAY_ENVIRONMENT` - Deployment environment (production/staging)

You must configure:
- `OPENAI_API_KEY` - Your OpenAI API key
- `AUTH_TYPE` - Authentication type (use `noop` for no auth, or `custom` for JWT/OAuth)

Optional variables:
- `DEBUG` - Enable debug mode (default: false)
- `LANGFUSE_LOGGING` - Enable Langfuse tracing (default: false)
- `LANGFUSE_SECRET_KEY` - Langfuse secret key
- `LANGFUSE_PUBLIC_KEY` - Langfuse public key
- `LANGFUSE_HOST` - Langfuse host URL

## Database Configuration

Railway PostgreSQL provides a connection string in the format:
```
postgresql://user:password@host:port/database
```

Aegra automatically converts this to the SQLAlchemy format:
```
postgresql+asyncpg://user:password@host:port/database
```

No manual database configuration is needed!

## Health Checks

Railway uses the `/health` endpoint defined in `railway.json`:
- **Path**: `/health`
- **Timeout**: 180 seconds
- **Checks**: Database, LangGraph checkpointer, and LangGraph store connectivity

The health check returns a JSON response:
```json
{
  "status": "healthy",
  "database": "connected",
  "langgraph_checkpointer": "connected",
  "langgraph_store": "connected"
}
```

## Automatic Migrations

The Dockerfile runs migrations automatically on startup:
```bash
alembic upgrade head && uvicorn src.agent_server.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

This ensures your database schema is always up-to-date.

## Custom Domains

1. Go to your Railway project → "Settings" → "Domains"
2. Click "Generate Domain" for a Railway subdomain (`yourapp.railway.app`)
3. Or add a custom domain by clicking "Custom Domain"

## Monitoring and Logs

### View Logs
```bash
# Real-time logs
railway logs

# Or view in the Railway dashboard → "Deployments" → Select deployment → "Logs"
```

### Metrics
- Railway provides built-in metrics for CPU, memory, and network usage
- Access metrics in the "Metrics" tab of your service

## Scaling

Railway automatically handles scaling based on your plan:
- **Hobby Plan**: Single instance with automatic restarts
- **Pro Plan**: Configure replicas and resource limits

To configure resources:
1. Go to "Settings" → "Resources"
2. Adjust CPU and memory limits as needed

## Cost Optimization

Railway pricing is based on usage:
- **Hobby Plan**: $5/month + usage
- **Pro Plan**: $20/month + usage

Tips to reduce costs:
- Use `AUTH_TYPE=noop` for development environments
- Set `DEBUG=false` in production
- Monitor resource usage in the Railway dashboard
- Use Railway's sleep feature for development instances

## Troubleshooting

### Build Failures

**Problem**: Docker build fails during deployment

**Solution**: Check the build logs in Railway dashboard. Common issues:
- Missing dependencies in `pyproject.toml`
- Python version mismatch (ensure Python 3.11+)

### Database Connection Errors

**Problem**: Application can't connect to database

**Solution**:
- Verify `DATABASE_URL` is set automatically by Railway Postgres
- Check that Postgres service is running in Railway dashboard
- Review health check logs for specific connection errors

### Health Check Timeouts

**Problem**: Deployment fails health checks

**Solution**:
- Increase `healthcheckTimeout` in `railway.json` (current: 180s)
- Check application logs for startup errors
- Verify database migrations complete successfully

### Migration Issues

**Problem**: Alembic migrations fail on startup

**Solution**:
```bash
# SSH into Railway container
railway run bash

# Check migration status
alembic current

# Try manual migration
alembic upgrade head
```

## Development Workflow

1. **Develop locally**
   ```bash
   docker compose up aegra
   ```

2. **Test changes**
   ```bash
   uv run pytest
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

4. **Railway auto-deploys** on push to main branch

## Security Best Practices

1. **Never commit secrets**
   - Use Railway environment variables for API keys
   - Add `.env` to `.gitignore`

2. **Enable authentication**
   - Set `AUTH_TYPE=custom` in production
   - Configure JWT/OAuth in `auth.py`

3. **Use HTTPS**
   - Railway provides HTTPS by default
   - All custom domains use Let's Encrypt SSL

4. **Restrict CORS**
   - Update `allow_origins` in `src/agent_server/main.py:87`
   - Replace `["*"]` with your frontend domains

## Support

- **Railway Docs**: https://docs.railway.app
- **Aegra Issues**: https://github.com/ibbybuilds/aegra/issues
- **Railway Discord**: https://discord.gg/railway

## Next Steps

After deployment:
1. Test the health endpoint: `https://your-app.railway.app/health`
2. Access API docs: `https://your-app.railway.app/docs`
3. Connect your frontend or LangGraph Client SDK
4. Set up monitoring with Langfuse (optional)

---

**Need help?** Join our [Discord](https://discord.com/invite/D5M3ZPS25e) or [Reddit](https://www.reddit.com/r/aegra/) community!
