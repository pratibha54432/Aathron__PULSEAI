.PHONY: help install setup run test clean deploy

help:
	@echo "PULSEAI AGENT - Makefile Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make setup       - Full setup (install + env)"
	@echo ""
	@echo "Development:"
	@echo "  make run         - Start FastAPI backend server"
	@echo "  make test        - Run test suite"
	@echo "  make dev         - Run with auto-reload"
	@echo ""
	@echo "Database:"
	@echo "  make db-init     - Initialize database"
	@echo "  make db-clean    - Reset database"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove cache files"
	@echo "  make clean-all   - Remove cache + venv"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

setup: install
	@echo "🔧 Setting up project..."
	@test -f backend/.env || cp .env.example backend/.env
	@echo "✅ Setup complete. Edit backend/.env with your API key"
	@echo "Get API key from: https://makersuite.google.com/app/apikey"

run:
	@echo "🚀 Starting FastAPI server..."
	cd backend && uvicorn main:app --reload --port 8000

dev: run

test:
	@echo "🧪 Running test suite..."
	@test -f backend/.env || (echo "❌ Create backend/.env first"; exit 1)
	python test_api.py

db-init:
	@echo "🗄️  Initializing database..."
	@echo "Not yet implemented - run with SQLite or configure Firebase"

db-clean:
	@echo "🗑️  Cleaning database..."
	rm -f backend/fitness.db
	@echo "✅ Database reset"

clean:
	@echo "🧹 Cleaning cache..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	@echo "✅ Cache cleaned"

clean-all: clean
	@echo "🗑️  Removing virtual environment..."
	rm -rf venv
	@echo "✅ All cleaned"

# Frontend commands
frontend-setup:
	@echo "⚛️  Setting up React frontend..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

frontend-dev:
	@echo "⚛️  Starting React dev server..."
	cd frontend && npm start

frontend-build:
	@echo "🏗️  Building React frontend..."
	cd frontend && npm run build
	@echo "✅ Frontend build complete"

# Deployment shortcuts
deploy-backend:
	@echo "🚀 Deploying backend..."
	@echo "Assuming your code is on GitHub:"
	@echo "1. Go to https://render.com"
	@echo "2. Connect your GitHub repo"
	@echo "3. Set GEMINI_API_KEY in environment variables"
	@echo "4. Deploy!"

deploy-frontend:
	@echo "🚀 Deploying frontend..."
	@echo "Assuming your code is on GitHub:"
	@echo "1. Go to https://vercel.com"
	@echo "2. Import your GitHub repo"
	@echo "3. Deploy!"

# API and docs
docs:
	@echo "📚 Opening API documentation..."
	@echo "Visit: http://localhost:8000/docs"

check:
	@echo "✅ Checking setup..."
	@command -v python3 >/dev/null 2>&1 && echo "✅ Python installed" || echo "❌ Python not found"
	@test -f requirements.txt && echo "✅ requirements.txt exists" || echo "❌ requirements.txt missing"
	@test -d backend && echo "✅ backend/ directory exists" || echo "❌ backend/ missing"
	@echo ""
	@echo "Next steps:"
	@echo "  1. make install"
	@echo "  2. Create backend/.env with GEMINI_API_KEY"
	@echo "  3. make run"
	@echo "  4. make test"
