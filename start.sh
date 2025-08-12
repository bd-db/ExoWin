#!/bin/bash

# ExoWin Startup Script
# This script sets up the database, launches the web app for games/mini apps,
# and starts the Telegram bot.

set -e  # Exit on error

echo "🚀 Starting ExoWin Platform..."

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ No .env file found. Make sure to create one before running this script."
    exit 1
fi

# Create necessary directories
mkdir -p logs
mkdir -p data

# Setup the database
echo "🗄️ Setting up database..."
python -m src.database.setup

# Check if SSL certificates exist
if [ -f "$SSL_CERT_PATH" ] && [ -f "$SSL_KEY_PATH" ]; then
    echo "🔒 SSL certificates found, enabling HTTPS for web app"
    SSL_ENABLED="true"
else
    echo "⚠️ SSL certificates not found, using HTTP for web app"
    SSL_ENABLED="false"
fi

# Start the web app in the background
echo "🌐 Starting web app for games and mini apps..."
if [ "$SSL_ENABLED" = "true" ]; then
    python -m src.webapp.app --ssl_cert="$SSL_CERT_PATH" --ssl_key="$SSL_KEY_PATH" > logs/webapp.log 2>&1 &
else
    python -m src.webapp.app > logs/webapp.log 2>&1 &
fi
WEBAPP_PID=$!
echo "📝 Web app started with PID: $WEBAPP_PID"

# Give the web app a moment to start
sleep 2

# Start the Telegram bot
echo "🤖 Starting Telegram bot..."
python -m src.bot > logs/bot.log 2>&1 &
BOT_PID=$!
echo "📝 Telegram bot started with PID: $BOT_PID"

echo "✅ ExoWin platform is now running!"
echo "📊 Web app logs: logs/webapp.log"
echo "🤖 Bot logs: logs/bot.log"
echo ""
echo "To stop the services, run: kill $WEBAPP_PID $BOT_PID"

# Save PIDs to file for easy shutdown
echo "$WEBAPP_PID $BOT_PID" > .running_pids

# Keep the script running to maintain the background processes
echo "Press Ctrl+C to stop all services"
wait