# AUREX Docker Deployment Guide

Complete guide for deploying AUREX using Docker containers.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- At least 4GB RAM available for Docker
- Ollama installed locally (for LLM access) or use remote Ollama instance

## Quick Start

### Production Deployment

1. **Build and start all services:**
```bash
docker-compose up -d
```

2. **Access the application:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ChromaDB: http://localhost:8001

3. **View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f chromadb
```

4. **Stop services:**
```bash
docker-compose down
```

### Development Deployment

For development with hot-reload:

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

## Architecture

```
┌─────────────────────────────────────────┐
│           Docker Network                │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │ Frontend │  │ Backend  │  │Chroma│ │
│  │Streamlit │◄─┤ FastAPI  │◄─┤  DB  │ │
│  │  :8501   │  │  :8000   │  │:8001 │ │
│  └──────────┘  └──────────┘  └──────┘ │
│       │             │                   │
└───────┼─────────────┼───────────────────┘
        │             │
        ▼             ▼
   localhost      localhost
    :8501          :8000
                      │
                      ▼
              Ollama (Host)
                 :11434
```

## Services

### Backend (FastAPI)
- **Port:** 8000
- **Container:** aurex-backend
- **Endpoints:** 
  - `/api/health` - Health check
  - `/api/docs` - API documentation
  - `/api/query` - RAG queries
  - `/api/analytics` - Analytics endpoints
  - `/api/visualization` - Chart generation
  - `/api/reports` - Report generation

### Frontend (Streamlit)
- **Port:** 8501
- **Container:** aurex-frontend
- **Pages:**
  - Upload - Document ingestion
  - AI Business Analyst - Query interface
  - Dashboard - Analytics & visualizations
  - Reports - Report generation

### ChromaDB (Vector Database)
- **Port:** 8001
- **Container:** aurex-chromadb
- **Purpose:** Vector storage for document embeddings
- **Persistent:** Data stored in named volume

## Volume Management

### Persistent Volumes

```bash
# List volumes
docker volume ls | grep aurex

# Inspect volume
docker volume inspect aurex-chroma-data

# Backup volume
docker run --rm -v aurex-chroma-data:/data -v $(pwd):/backup ubuntu tar czf /backup/chroma-backup.tar.gz /data

# Restore volume
docker run --rm -v aurex-chroma-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/chroma-backup.tar.gz -C /
```

### Bind Mounts

Development mode uses bind mounts for hot-reload:
- `./app` → `/app/app` (Backend code)
- `./frontend` → `/app/frontend` (Frontend code)
- `./data` → `/app/data` (Documents, reports, DB)

## Environment Configuration

### Production (.env)
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Ollama Configuration
OLLAMA_HOST=host.docker.internal
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b

# Storage
CHROMA_PERSIST_DIR=/app/data/chroma_db
UPLOAD_DIR=/app/data/uploads
REPORTS_DIR=/app/data/reports

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

### Development
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Docker Commands

### Build
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend

# Build without cache
docker-compose build --no-cache
```

### Start/Stop
```bash
# Start in background
docker-compose up -d

# Start with logs
docker-compose up

# Stop services
docker-compose stop

# Stop and remove
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Maintenance
```bash
# Restart service
docker-compose restart backend

# View service status
docker-compose ps

# Execute command in container
docker-compose exec backend python -m pytest

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend bash
```

### Logs
```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f backend
```

## Health Checks

All services include health checks:

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check ChromaDB health
curl http://localhost:8001/api/v1/heartbeat

# Docker health status
docker-compose ps
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Check Docker resources
docker system df

# Clean up
docker system prune -a
```

### Database connection issues
```bash
# Verify ChromaDB is running
docker-compose ps chromadb

# Check ChromaDB logs
docker-compose logs chromadb

# Restart ChromaDB
docker-compose restart chromadb
```

### Ollama connection issues
```bash
# Verify Ollama is running on host
curl http://localhost:11434/api/tags

# Check backend environment
docker-compose exec backend env | grep OLLAMA

# Test from container
docker-compose exec backend curl http://host.docker.internal:11434/api/tags
```

### Port conflicts
```bash
# Check ports in use
netstat -ano | findstr "8000"
netstat -ano | findstr "8501"
netstat -ano | findstr "8001"

# Change ports in docker-compose.yml
ports:
  - "8002:8000"  # Use different host port
```

### Out of disk space
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Complete cleanup
docker system prune -a --volumes
```

## Production Deployment

### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml aurex

# Check services
docker stack services aurex

# Remove stack
docker stack rm aurex
```

### Using Kubernetes
```bash
# Generate Kubernetes manifests
kompose convert -f docker-compose.yml

# Apply to cluster
kubectl apply -f .
```

## Security Considerations

1. **Environment Variables:** Use Docker secrets for sensitive data
2. **Network Isolation:** Services communicate via internal network
3. **Volume Permissions:** Set appropriate file permissions
4. **Image Security:** Regularly update base images
5. **Resource Limits:** Set memory and CPU limits in production

### Resource Limits Example
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Performance Optimization

1. **Multi-stage builds:** Reduce image size
2. **Layer caching:** Order Dockerfile for better caching
3. **Volume mounts:** Use volumes for better I/O performance
4. **Resource allocation:** Allocate sufficient Docker resources

## Backup and Restore

### Backup
```bash
# Backup ChromaDB data
docker-compose exec chromadb tar czf /tmp/backup.tar.gz /chroma/chroma
docker cp aurex-chromadb:/tmp/backup.tar.gz ./backups/

# Backup uploaded documents
tar czf documents-backup.tar.gz data/uploads/

# Backup reports
tar czf reports-backup.tar.gz data/reports/
```

### Restore
```bash
# Restore ChromaDB data
docker cp ./backups/backup.tar.gz aurex-chromadb:/tmp/
docker-compose exec chromadb tar xzf /tmp/backup.tar.gz -C /

# Restore documents
tar xzf documents-backup.tar.gz
```

## Monitoring

### Container Stats
```bash
# Real-time stats
docker stats

# Specific container
docker stats aurex-backend
```

### Health Monitoring
```bash
# Check all health statuses
docker-compose ps

# Automated health check script
while true; do
  curl -f http://localhost:8000/api/health || echo "Backend unhealthy"
  sleep 30
done
```

## Upgrade Procedure

1. **Backup data:**
```bash
./backup.sh
```

2. **Pull latest changes:**
```bash
git pull origin main
```

3. **Rebuild images:**
```bash
docker-compose build --no-cache
```

4. **Update services:**
```bash
docker-compose up -d
```

5. **Verify deployment:**
```bash
docker-compose ps
curl http://localhost:8000/api/health
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review documentation: `README.md`
- Check health endpoints
- Verify Ollama is running on host
