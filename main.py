"""
LinkedIn Profile Query Bot - Main Application

This script provides a unified entry point to run the LinkedIn Profile Query Bot.
It can start the API server, Wati integration, or both.
"""

import os
import argparse
import logging
import json
import time
import threading
import uvicorn
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from .env file or environment variables."""
    # Load from .env file if it exists
    load_dotenv()
    
    # Configuration dictionary
    config = {
        "wati_api_key": os.environ.get("WATI_API_KEY"),
        "bot_api_url": os.environ.get("BOT_API_URL", "http://localhost:8000"),
        "profiles_dir": os.environ.get("PROFILES_DIR", "profiles"),
        "wati_api_url": os.environ.get("WATI_API_URL", "https://api.wati.io/api/v1"),
        "host": os.environ.get("HOST", "0.0.0.0"),
        "port": int(os.environ.get("PORT", "8000"))
    }
    
    # Try to load from config.json if it exists
    try:
        with open("config.json", "r") as f:
            file_config = json.load(f)
        # Update config with values from file
        for key, value in file_config.items():
            if key not in config or not config[key]:
                config[key] = value
    except (FileNotFoundError, json.JSONDecodeError):
        logger.info("No config.json found or invalid, using environment variables")
    
    # Validate required configuration
    if not config["wati_api_key"] and not os.environ.get("SKIP_WATI"):
        logger.warning("Wati API key not found. Set WATI_API_KEY or SKIP_WATI=1")
    
    # Create profiles directory if it doesn't exist
    os.makedirs(config["profiles_dir"], exist_ok=True)
    
    return config

def run_api_server(config):
    """Run the FastAPI server."""
    from api_server import app
    
    logger.info(f"Starting API server on {config['host']}:{config['port']}")
    uvicorn.run(app, host=config["host"], port=config["port"])

def run_wati_integration(config):
    """Run the Wati integration."""
    from wati_integration import LinkedInBotWatiIntegration
    
    if not config["wati_api_key"]:
        logger.error("Wati API key is required for Wati integration")
        return
    
    logger.info("Starting Wati integration")
    integration = LinkedInBotWatiIntegration(
        config["wati_api_key"],
        config["bot_api_url"],
        config["wati_api_url"]
    )
    
    # Set up webhook
    webhook_result = integration.setup_webhook()
    logger.info(f"Webhook setup result: {webhook_result}")
    
    # Keep the script running
    logger.info("Wati integration running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Wati integration...")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="LinkedIn Profile Query Bot")
    parser.add_argument(
        "--mode", 
        choices=["api", "wati", "all"], 
        default="all",
        help="Run mode: api (API server only), wati (Wati integration only), all (both)"
    )
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    if args.mode == "api":
        # Run API server only
        run_api_server(config)
    elif args.mode == "wati":
        # Run Wati integration only
        run_wati_integration(config)
    else:
        # Run both in separate threads
        api_thread = threading.Thread(target=run_api_server, args=(config,))
        api_thread.daemon = True
        api_thread.start()
        
        # Give the API server time to start
        time.sleep(2)
        
        # Run Wati integration in the main thread
        run_wati_integration(config)

if __name__ == "__main__":
    main()
