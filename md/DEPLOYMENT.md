# AUREX Deployment Guide

Complete guide for deploying AUREX in various environments.

---

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Backup & Recovery](#backup--recovery)
7. [Scaling & Performance](#scaling--performance)
8. [Security Hardening](#security-hardening)

---

## Local Deployment

### Prerequisites

- Python 3.11 or higher
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space (50GB recommended)
- Ollama with llama3.1:8b model

### Step-by-Step Installation

#### 1. System Preparation

**Windows:**
```powershell
# Check Python version
python --version  # Should be 3.11+

# Check disk space
Get-PSDrive C | Select-Object Used,Free
```

**Linux/Mac:**
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Check disk space
df -h
```

#### 2. Clone Repository

```bash
git clone https://github.com/yourusername/AUREX.git
cd AUREX
```

#### 3. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

#### 5. Install Ollama

**Windows:**
1. Download from https://ollama.ai/download
2. Run installer
3. Open PowerShell and run:
```powershell
ollama pull llama3.1:8b
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b
ollama serve
```

**Mac:**
```bash
brew install ollama
ollama pull llama3.1:8b
ollama serve
```

#### 6. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Minimum .env configuration:**
```env
API_HOST=127.0.0.1
API_PORT=8000
OLLAMA_HOST=127.0.0.1
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.1:8b
LOG_LEVEL=INFO
DEBUG=False
```

#### 7. Initialize Database

```bash
# Create data directories
mkdir -p data/uploads data/chroma_db data/reports logs

# Set permissions (Linux/Mac)
chmod 755 data
chmod 755 logs
```

#### 8. Start Services

**Option A: Using Startup Script**

Windows:
```powershell
.\START_AUREX.bat
```

Linux/Mac:
```bash
chmod +x start_aurex.sh
./start_aurex.sh
```

**Option B: Manual Start**

Terminal 1 (Backend):
```bash
cd AUREX
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2 (Frontend):
```bash
cd AUREX
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run frontend/streamlit_app.py
```

#### 9. Verify Deployment

```bash
# Check backend
curl http://localhost:8000/api/health

# Check frontend
# Open browser: http://localhost:8501

# Check Ollama
curl http://localhost:11434/api/tags
```

#### 10. Test System

```bash
# Run tests
pytest tests -v

# Run quick smoke test
pytest tests/integration/test_api_health.py -v
```

---

## Docker Deployment

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- 8GB RAM available for Docker
- Ollama running on host machine

### Quick Start

1. **Start all services:**
```bash
docker-compose up -d
```

2. **Verify services:**
```bash
docker-compose ps
```

3. **Access application:**
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- ChromaDB: http://localhost:8001

4. **View logs:**
```bash
docker-compose logs -f
```

5. **Stop services:**
```bash
docker-compose down
```

### Production Docker Deployment

Use production compose file with optimizations:

```bash
# Build images
docker-compose -f docker-compose.yml build

# Start services
docker-compose -f docker-compose.yml up -d

# Health check
docker-compose ps
curl http://localhost:8000/api/health
```

### Development Docker Deployment

Use development compose for hot-reload:

```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down
```

See [DOCKER.md](DOCKER.md) for comprehensive Docker guide.

---

## Cloud Deployment

### AWS Deployment

#### EC2 Instance

**1. Launch EC2 Instance:**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.large or larger
- Storage: 50GB EBS volume
- Security Group: Allow ports 22, 8000, 8501

**2. Connect and Setup:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt install docker-compose-plugin

# Clone repository
git clone https://github.com/yourusername/AUREX.git
cd AUREX

# Configure environment
cp .env.example .env
nano .env

# Start services
docker-compose up -d
```

**3. Setup Domain (Optional):**
- Configure Route 53 or use Elastic IP
- Setup SSL with Let's Encrypt
- Configure nginx reverse proxy

#### ECS Deployment

**1. Create Task Definition:**
```json
{
  "family": "aurex-backend",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-registry/aurex-backend:latest",
      "memory": 2048,
      "cpu": 1024,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

**2. Create ECS Service:**
```bash
aws ecs create-service \
  --cluster aurex-cluster \
  --service-name aurex-backend \
  --task-definition aurex-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

### Azure Deployment

#### Azure Container Instances

```bash
# Create resource group
az group create --name aurex-rg --location eastus

# Create container
az container create \
  --resource-group aurex-rg \
  --name aurex-backend \
  --image your-registry/aurex-backend:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables \
    API_HOST=0.0.0.0 \
    OLLAMA_HOST=your-ollama-host
```

#### Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name aurex-plan \
  --resource-group aurex-rg \
  --sku B2 \
  --is-linux

# Create web app
az webapp create \
  --resource-group aurex-rg \
  --plan aurex-plan \
  --name aurex-app \
  --deployment-container-image-name your-registry/aurex:latest
```

### Google Cloud Platform

#### Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/your-project/aurex-backend

# Deploy to Cloud Run
gcloud run deploy aurex-backend \
  --image gcr.io/your-project/aurex-backend \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --allow-unauthenticated
```

#### GKE (Kubernetes)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aurex-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aurex-backend
  template:
    metadata:
      labels:
        app: aurex-backend
    spec:
      containers:
      - name: backend
        image: gcr.io/your-project/aurex-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_HOST
          value: "0.0.0.0"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

Deploy:
```bash
kubectl apply -f deployment.yaml
kubectl expose deployment aurex-backend --type=LoadBalancer --port=8000
```

---

## Production Considerations

### Configuration

**1. Environment Variables:**
```env
# Production settings
DEBUG=False
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Performance
TOP_K=5
SIMILARITY_THRESHOLD=0.3
MAX_UPLOAD_SIZE=104857600  # 100MB

# Database
CHROMA_PERSIST_DIR=/data/chroma_db

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=9090
```

**2. Reverse Proxy (nginx):**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**3. SSL/TLS:**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Database

**1. ChromaDB Persistence:**
```python
# Ensure persistent storage
CHROMA_PERSIST_DIR=/data/chroma_db

# Regular backups
tar -czf chroma-backup-$(date +%Y%m%d).tar.gz data/chroma_db/
```

**2. Document Storage:**
```bash
# Use cloud storage for uploads
# AWS S3, Azure Blob, Google Cloud Storage
# Configure in .env
STORAGE_BACKEND=s3
S3_BUCKET=your-bucket
S3_REGION=us-east-1
```

### Performance Optimization

**1. Application Level:**
```python
# Increase workers
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# Enable caching
ENABLE_CACHE=True
CACHE_TTL=3600
```

**2. Resource Limits:**
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

**3. Load Balancing:**
```yaml
# Use multiple backend instances
docker-compose scale backend=3
```

---

## Monitoring & Maintenance

### Health Checks

**1. Endpoint Monitoring:**
```bash
# Setup monitoring script
#!/bin/bash
while true; do
  if ! curl -f http://localhost:8000/api/health; then
    echo "Backend down!" | mail -s "AUREX Alert" admin@example.com
  fi
  sleep 60
done
```

**2. Log Monitoring:**
```bash
# Use log aggregation
# ELK Stack, Splunk, CloudWatch, etc.

# Example: CloudWatch Logs
aws logs create-log-group --log-group-name /aurex/backend
```

**3. Performance Metrics:**
```python
# Prometheus integration
from prometheus_client import Counter, Histogram

query_duration = Histogram('query_duration_seconds', 'Query duration')
query_counter = Counter('queries_total', 'Total queries')
```

### Backup Strategy

**1. Automated Backups:**
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR=/backups/aurex
DATE=$(date +%Y%m%d_%H%M%S)

# Backup ChromaDB
tar -czf $BACKUP_DIR/chroma_$DATE.tar.gz data/chroma_db/

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz data/uploads/

# Backup reports
tar -czf $BACKUP_DIR/reports_$DATE.tar.gz data/reports/

# Remove old backups (keep 30 days)
find $BACKUP_DIR -mtime +30 -delete
```

**2. Schedule Backups:**
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### Updates & Patches

**1. Update Procedure:**
```bash
# Stop services
docker-compose down

# Backup data
./backup.sh

# Pull latest code
git pull origin main

# Rebuild images
docker-compose build

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations (if any)
# python manage.py migrate

# Start services
docker-compose up -d

# Verify
curl http://localhost:8000/api/health
```

**2. Rolling Updates (Zero Downtime):**
```bash
# Update one instance at a time
docker-compose up -d --scale backend=3 --no-recreate
docker-compose restart backend-1
# Wait for health check
docker-compose restart backend-2
# Wait for health check
docker-compose restart backend-3
```

---

## Scaling & Performance

### Horizontal Scaling

**1. Multiple Backend Instances:**
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
  
  load-balancer:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - backend
```

**2. Load Balancer Configuration:**
```nginx
upstream backend {
    least_conn;
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

### Vertical Scaling

**1. Increase Resources:**
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

**2. Optimize Ollama:**
```env
# Use GPU if available
OLLAMA_NUM_GPU=1
OLLAMA_NUM_THREAD=8
```

### Caching Strategy

**1. Redis Cache:**
```python
# Add Redis for caching
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_BACKEND=redis
```

**2. CDN for Static Assets:**
- Use CloudFront, Cloudflare, or similar
- Cache images, CSS, JavaScript

---

## Security Hardening

### Application Security

**1. Authentication:**
```python
# Add API key authentication
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    return api_key
```

**2. Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/query")
@limiter.limit("60/minute")
async def query_endpoint():
    pass
```

**3. Input Validation:**
```python
# Already handled by Pydantic
# Add additional validation as needed
from pydantic import validator, constr

class QueryRequest(BaseModel):
    question: constr(min_length=1, max_length=1000)
    
    @validator('question')
    def question_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('question cannot be empty')
        return v
```

### Infrastructure Security

**1. Firewall Rules:**
```bash
# Only allow necessary ports
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw enable
```

**2. SSL/TLS:**
```bash
# Force HTTPS redirect
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

**3. Secrets Management:**
```bash
# Use environment variables, not hardcoded
# Use AWS Secrets Manager, Azure Key Vault, etc.
aws secretsmanager get-secret-value --secret-id aurex/prod
```

### Container Security

**1. Non-root User:**
```dockerfile
# Dockerfile
RUN useradd -m -u 1000 aurex
USER aurex
```

**2. Security Scanning:**
```bash
# Scan Docker images
docker scan aurex-backend:latest

# Use Trivy
trivy image aurex-backend:latest
```

**3. Network Isolation:**
```yaml
# docker-compose.yml
networks:
  frontend:
    internal: false
  backend:
    internal: true
```

---

## Troubleshooting Deployment

### Common Issues

**1. Port Conflicts:**
```bash
# Find process using port
netstat -ano | findstr "8000"  # Windows
lsof -i :8000                   # Linux/Mac

# Kill process
kill -9 <PID>
```

**2. Permission Errors:**
```bash
# Fix permissions
chmod -R 755 data logs
chown -R $USER:$USER data logs
```

**3. Database Connection:**
```bash
# Check ChromaDB
docker-compose logs chromadb

# Restart ChromaDB
docker-compose restart chromadb
```

**4. Memory Issues:**
```bash
# Check memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources
```

### Deployment Checklist

- [ ] System requirements met
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Database initialized
- [ ] Ollama running
- [ ] Services started
- [ ] Health checks passing
- [ ] Tests passing
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Security hardened
- [ ] Documentation updated

---

## Support & Resources

- **Documentation**: [README.md](README.md)
- **API Docs**: http://your-domain.com/docs
- **Docker Guide**: [DOCKER.md](DOCKER.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **GitHub Issues**: Report deployment issues
- **Email**: your.email@example.com

---

**Last Updated**: September 2026  
**Version**: 1.0.0
