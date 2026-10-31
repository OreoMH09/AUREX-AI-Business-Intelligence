# AUREX Docker Quick Start Guide

Get AUREX running with Docker in 5 minutes!

---

## Prerequisites

1. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Minimum: 8GB RAM allocated to Docker
   - 10GB free disk space

2. **Ollama** running on your host machine
   - Must be running on `localhost:11434`
   - Start with: `ollama serve`
   - Model: `llama3.1:8b` must be pulled

---

## Quick Start (3 Steps)

### Step 1: Verify Docker Setup

Run the pre-flight check:
```bash
CHECK_DOCKER.bat
```

This will verify:
- ✅ Docker installed
- ✅ Docker running
- ✅ Docker Compose available
- ✅ Ollama accessible
- ✅ Sufficient disk space

### Step 2: Deploy AUREX

Run the deployment script:
```bash
DEPLOY_DOCKER.bat
```

Choose deployment type:
- **Option 1**: Production (optimized, production-ready)
- **Option 2**: Development (hot-reload for code changes)

### Step 3: Access AUREX

Once deployed, access:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ChromaDB**: http://localhost:8001

---

## Manual Deployment

If you prefer manual commands:

### Production Deployment
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development Deployment
```bash
# Start with hot-reload
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

---

## What Gets Deployed?

### Services Started

1. **aurex-backend**
   - FastAPI application
   - Port: 8000
   - Container: Python 3.11

2. **aurex-frontend**
   - Streamlit UI
   - Port: 8501
   - Container: Python 3.11

3. **aurex-chromadb**
   - Vector database
   - Port: 8001
   - Persistent storage

### Volumes

- `aurex-chroma-data`: Vector database storage (persistent)
- `./data`: Host directory mounted for documents and reports
- `./logs`: Application logs

### Network

- `aurex-network`: Internal bridge network for service communication

---

## Common Tasks

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f chromadb
```

### Restart Service
```bash
# Restart specific service
docker-compose restart backend

# Restart all
docker-compose restart
```

### Stop Everything
```bash
# Stop and keep data
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Rebuild Images
```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build backend

# Force rebuild (no cache)
docker-compose build --no-cache
```

### Check Health
```bash
# Check service status
docker-compose ps

# Check backend health
curl http://localhost:8000/api/health

# Check frontend
curl http://localhost:8501
```

---

## Troubleshooting

### Issue: Docker is not running
**Solution**: Start Docker Desktop from Start Menu

### Issue: Port already in use
**Solution**: Stop conflicting service or change ports in docker-compose.yml
```bash
# Check what's using port 8000
netstat -ano | findstr "8000"

# Kill process (use PID from above)
taskkill /PID <PID> /F
```

### Issue: Cannot connect to Ollama
**Solution**: Ensure Ollama is running on host
```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

### Issue: Out of memory
**Solution**: Increase Docker memory
1. Docker Desktop → Settings → Resources
2. Increase Memory to 8GB+
3. Click "Apply & Restart"

### Issue: Build fails
**Solution**: Clean rebuild
```bash
# Remove everything
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Service won't start
**Solution**: Check logs
```bash
docker-compose logs backend
docker-compose logs frontend
```

---

## Performance Tips

### Optimize Docker
1. **Allocate more resources**:
   - Docker Desktop → Settings → Resources
   - CPU: 4+ cores
   - Memory: 8GB+
   - Swap: 2GB

2. **Use WSL 2** (Windows):
   - Docker Desktop → Settings → General
   - Enable "Use WSL 2 based engine"

3. **Prune regularly**:
```bash
# Remove unused images and containers
docker system prune -a
```

### Production Optimization
1. **Use production compose**:
   - Always use `docker-compose.yml` for production
   - Sets resource limits
   - Optimized for performance

2. **Monitor resources**:
```bash
# Real-time resource usage
docker stats
```

3. **Scale services**:
```bash
# Run multiple backend instances
docker-compose up -d --scale backend=3
```

---

## Data Persistence

### Where is data stored?

**Documents**: `./data/uploads/` (mounted from host)
**ChromaDB**: Docker volume `aurex-chroma-data`
**Reports**: `./data/reports/` (mounted from host)
**Logs**: `./logs/` (mounted from host)

### Backup data
```bash
# Backup ChromaDB volume
docker run --rm -v aurex-chroma-data:/data -v %cd%:/backup ubuntu tar czf /backup/chroma-backup.tar.gz /data

# Backup documents (already on host)
tar czf documents-backup.tar.gz data/uploads/
```

### Restore data
```bash
# Restore ChromaDB
docker run --rm -v aurex-chroma-data:/data -v %cd%:/backup ubuntu tar xzf /backup/chroma-backup.tar.gz -C /
```

---

## Development Workflow

### For Active Development
1. Use development compose for hot-reload:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. Make code changes in `app/` or `frontend/`
3. Changes auto-reload (no restart needed)

### Run Tests
```bash
# Run tests in container
docker-compose exec backend pytest tests -v

# Run specific test
docker-compose exec backend pytest tests/unit/test_analytics.py -v
```

### Access Container Shell
```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend bash
```

---

## Deployment Checklist

Before deploying, verify:

- [ ] Docker Desktop installed and running
- [ ] 8GB+ RAM allocated to Docker
- [ ] 10GB+ free disk space
- [ ] Ollama running (`ollama serve`)
- [ ] Model pulled (`ollama pull llama3.1:8b`)
- [ ] Ports 8000, 8501, 8001 available
- [ ] `.env` file configured (optional)

---

## Next Steps

After deployment:

1. **Test the system**:
   - Upload a document at http://localhost:8501
   - Ask questions in AI Analyst page
   - Check Dashboard for analytics
   - Generate a report

2. **Monitor health**:
   ```bash
   # Check all services
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

3. **Production deployment**:
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment
   - Configure SSL/TLS for security
   - Setup monitoring and backups

---

## Support

**Issues?**
- Check logs: `docker-compose logs -f`
- View documentation: [DOCKER.md](DOCKER.md)
- GitHub issues: [Report issues]

**Need help?**
- Full Docker guide: [DOCKER.md](DOCKER.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- User guide: [USER_GUIDE.md](USER_GUIDE.md)

---

## Summary

**Start**: `DEPLOY_DOCKER.bat` → Choose option → Done!  
**Access**: http://localhost:8501  
**Stop**: `docker-compose down`  
**Logs**: `docker-compose logs -f`  

That's it! Your AUREX system is now running in Docker containers. 🎉
