#!/usr/bin/env python3
"""
ExoWin 👑 - A Telegram bot for gambling without KYC

This is the main entry point for the ExoWin platform.
For a more comprehensive startup that includes the web app,
use the start.sh script instead.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check required environment variables
required_vars = ['BOT_TOKEN', 'MONGODB_URI']
missing_vars = []

for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\nPlease check your .env file and ensure all required variables are set.")
    sys.exit(1)

# Import and run the bot
from src.bot import main

if __name__ == "__main__":
    print("🤖 Starting ExoWin Telegram Bot...")
    asyncio.run(main())