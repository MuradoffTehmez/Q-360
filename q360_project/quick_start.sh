#!/bin/bash

# Q360 Quick Start Script
# This script helps you quickly set up and run the Q360 Evaluation System

echo "========================================="
echo "Q360 - 360° Qiymətləndirmə Sistemi Tahmaz Mueadov"
echo "Quick Start Script v1.0 by Claude Code"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env file and update the following:"
    echo "   - SECRET_KEY"
    echo "   - DB_PASSWORD"
    echo "   - EMAIL_HOST_USER"
    echo "   - EMAIL_HOST_PASSWORD"
    echo ""
    read -p "Press Enter after updating .env file..."
else
    echo "✅ .env file exists"
fi

echo ""
echo "🚀 Starting Docker containers..."
docker-compose up -d --build

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 10

echo ""
echo "📦 Running database migrations..."
docker-compose exec web python manage.py migrate

echo ""
echo "👤 Creating superuser..."
docker-compose exec web python manage.py createsuperuser

echo ""
echo "📁 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "✅ Q360 System is ready!"
echo "========================================="
echo ""
echo "Access the application:"
echo "  🌐 Application: http://localhost"
echo "  🔐 Admin Panel: http://localhost/admin"
echo "  🔌 API: http://localhost/api"
echo ""
echo "Useful commands:"
echo "  docker-compose ps           # View running containers"
echo "  docker-compose logs -f      # View logs"
echo "  docker-compose down         # Stop containers"
echo "  docker-compose restart      # Restart containers"
echo ""
echo "Happy evaluating! 🎉"
