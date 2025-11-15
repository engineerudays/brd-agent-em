# Docker Setup Guide for n8n

This guide helps you run n8n with Docker and mount your projects folder for easy file access.

## 🚀 Quick Start

### 1. Start n8n with Docker Compose

```bash
cd /Users/udayammanagi/Udays-Folder/IK/brd_agent_em
docker-compose up -d
```

### 2. Access n8n

Open your browser and go to: **http://localhost:5678**

**Default credentials:**
- Username: `admin`
- Password: `change-this-password`

⚠️ **Important:** Change these in `docker-compose.yml` before using in production!

### 3. Import Workflows

1. In n8n, go to **Workflows** → **Import from File**
2. Import these files:
   - `n8n_flows/planning_agent/engineering_plan/structured_plan_generator.json`
   - `n8n_flows/planning_agent/project_schedule/project_schedule_generator.json`
3. Configure Anthropic API credentials (see [ANTHROPIC_SETUP.md](n8n_flows/planning_agent/ANTHROPIC_SETUP.md))
4. Activate the workflows

## 📁 Volume Mounts

The Docker setup mounts these directories:

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `~/.n8n` | `/home/node/.n8n` | n8n data, credentials, settings |
| `/Users/udayammanagi/Udays-Folder` | `/data/projects` | All your projects (read/write) |

### File Path Mapping

**Your local path:**
```
/Users/udayammanagi/Udays-Folder/IK/brd_agent_em/sample_inputs/outputs/
```

**Inside n8n container:**
```
/data/projects/IK/brd_agent_em/sample_inputs/outputs/
```

**This means:**
- Files saved by n8n workflows appear in your local project instantly!
- You can access any project under `/Users/udayammanagi/Udays-Folder/` from n8n

## 🔧 Docker Commands

### Start n8n
```bash
docker-compose up -d
```

### Stop n8n
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f n8n
```

### Restart n8n
```bash
docker-compose restart
```

### Check status
```bash
docker-compose ps
```

### Update n8n to latest version
```bash
docker-compose pull
docker-compose up -d
```

## 🐛 Troubleshooting

### Port already in use
If port 5678 is already taken, change it in `docker-compose.yml`:
```yaml
ports:
  - "5679:5678"  # Use 5679 instead
```

### Permission denied errors
If n8n can't write files:

```bash
# Check directory permissions
ls -la sample_inputs/outputs/

# Fix permissions if needed
chmod -R 755 sample_inputs/outputs/
```

### Can't access mounted files
Check that the volume is mounted:
```bash
docker exec -it n8n-brd-agent ls /data/projects/IK/brd_agent_em
```

Should show your project files.

### n8n won't start
Check logs for errors:
```bash
docker-compose logs n8n
```

## 🔐 Security Best Practices

### 1. Change Default Password

Edit `docker-compose.yml`:
```yaml
environment:
  - N8N_BASIC_AUTH_USER=your-username
  - N8N_BASIC_AUTH_PASSWORD=your-strong-password
```

### 2. Use Environment File

Create `.env` file (safer than hardcoding):
```bash
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-strong-password
ANTHROPIC_API_KEY=sk-ant-...
```

Update `docker-compose.yml`:
```yaml
environment:
  - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
  - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
```

Add `.env` to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

### 3. Network Security

For production, use HTTPS with reverse proxy (nginx, Caddy, Traefik).

## 📊 Monitoring

### Check n8n health
```bash
curl http://localhost:5678/healthz
```

### Monitor resource usage
```bash
docker stats n8n-brd-agent
```

## 🔄 Backup & Restore

### Backup n8n data
```bash
# Backup workflows, credentials, settings
tar -czf n8n-backup-$(date +%Y%m%d).tar.gz ~/.n8n
```

### Restore n8n data
```bash
# Stop n8n
docker-compose down

# Restore backup
tar -xzf n8n-backup-20250115.tar.gz -C ~/

# Start n8n
docker-compose up -d
```

## 🌐 Access from Other Machines

To access n8n from other devices on your network:

1. Edit `docker-compose.yml`:
```yaml
environment:
  - WEBHOOK_URL=http://your-machine-ip:5678/
```

2. Update ports to bind to all interfaces:
```yaml
ports:
  - "0.0.0.0:5678:5678"
```

3. Find your IP:
```bash
ipconfig getifaddr en0  # macOS
```

4. Access from other device: `http://your-machine-ip:5678`

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Docker Setup](https://docs.n8n.io/hosting/installation/docker/)
- [n8n Community Forum](https://community.n8n.io/)
- [Project Setup Guide](ANTHROPIC_SETUP.md)

---

**Need help?** Check the logs with `docker-compose logs -f n8n`

