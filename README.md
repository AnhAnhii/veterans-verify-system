# 🎖️ Veterans Verification System

A comprehensive system for verifying U.S. military veteran status, featuring a Web Application, REST API, and Command-Line Interface.

![Veterans Verify](https://img.shields.io/badge/Veterans-Verify-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## 📋 Overview

This system allows organizations and individuals to verify military veteran status through:

- **SheerID Integration**: Official verification against DoD/DEERS database
- **VA Public Data**: Search through Grave Locator, Veterans Legacy Memorial, and Army Explorer
- **Multiple Interfaces**: Web App, REST API, and CLI

## 🏗️ Architecture

```
veterans-verify-system/
├── web/          # Next.js Web Application
├── api/          # Python FastAPI Backend
├── cli/          # Python CLI Tool
└── database/     # Supabase SQL Migrations
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.8+
- Supabase Account
- Vercel Account (for deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/veterans-verify-system.git
cd veterans-verify-system
```

### 2. Set Up Supabase

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the migration:

```bash
# Copy contents of database/migrations/001_initial_schema.sql
# Paste and run in Supabase SQL Editor
```

### 3. Configure API Backend

```bash
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Supabase credentials

# Run locally
uvicorn app.main:app --reload
```

### 4. Configure Web Application

```bash
cd web

# Install dependencies
npm install

# Create .env.local file
cp env.example .env.local
# Edit .env.local with your credentials

# Run locally
npm run dev
```

### 5. Install CLI (Optional)

```bash
cd cli
pip install -e .

# Configure
veterans-cli configure --api-key YOUR_API_KEY --api-url http://localhost:8000
```

## 📱 Web Application

The web application provides:

- **Dashboard**: Overview of verification activities
- **Verify**: Multi-step form for new verifications
- **VA Lookup**: Search public VA databases
- **History**: Track all verification requests

### Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/auth` | Login/Register |
| `/dashboard` | Main dashboard |
| `/verify` | New verification |
| `/lookup` | VA record search |
| `/history` | Verification history |

## 🔧 API Endpoints

### Verification

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/verify/create` | Create verification |
| `POST` | `/api/verify/submit` | Submit veteran info |
| `GET` | `/api/verify/{id}/status` | Check status |
| `POST` | `/api/verify/{id}/document` | Upload document |

### VA Lookup

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/lookup/grave` | Search Grave Locator |
| `GET` | `/api/lookup/vlm` | Search VLM |
| `GET` | `/api/lookup/army` | Search Army Explorer |
| `GET` | `/api/lookup/aggregate` | Search all sources |

### History

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/history` | Get verification history |

## ⌨️ CLI Usage

```bash
# Configure
veterans-cli configure --api-key YOUR_KEY

# Verify veteran status
veterans-cli verify \
  --first-name "John" \
  --last-name "Smith" \
  --birth "1985-03-15" \
  --branch "Army" \
  --email "john@example.com"

# Search VA records
veterans-cli lookup --first-name "John" --last-name "Smith"

# View history
veterans-cli history

# Check status
veterans-cli status <verification_id>
```

## 🚀 Deployment

### Deploy API to Vercel

```bash
cd api
vercel
```

### Deploy Web to Vercel

```bash
cd web
vercel
```

### Environment Variables

#### API (.env)
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx
SHEERID_API_KEY=xxx
SECRET_KEY=xxx
```

#### Web (.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## 🔐 Security

- All API endpoints require authentication (Bearer token or API key)
- Row Level Security (RLS) enabled on all Supabase tables
- CORS configured for allowed origins only
- Sensitive data encrypted at rest

## 📊 Supported Services

- ✅ ChatGPT Plus
- ✅ Spotify Premium
- ✅ YouTube Premium
- ✅ Google One
- ✅ Custom integrations

## 🎖️ Military Branches

All U.S. military branches are supported:

- Army, Navy, Air Force, Marine Corps, Coast Guard, Space Force
- Army/Air National Guard
- All Reserve components

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📞 Support

- 📧 Email: support@veteransverify.com
- 📖 Documentation: [docs.veteransverify.com](https://docs.veteransverify.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/veterans-verify-system/issues)
