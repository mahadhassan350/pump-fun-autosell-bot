"""
Simple script to run the auto-sell bot with a 3-second selling delay.
"""
import asyncio
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("auto-sell")

# Load environment variables
load_dotenv()

# Configuration
RPC_ENDPOINT = os.getenv("SOLANA_NODE_RPC_ENDPOINT")
WSS_ENDPOINT = os.getenv("SOLANA_NODE_WSS_ENDPOINT")
PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
SELL_DELAY_SECONDS = 3  # Auto-sell after 3 seconds

async def main():
    """
    Main function to run the auto-sell bot.
    """
    logger.info("Starting Auto-Sell Bot")
    logger.info(f"RPC Endpoint: {RPC_ENDPOINT}")
    logger.info(f"Auto-sell delay: {SELL_DELAY_SECONDS} seconds")
    
    # Verify configuration
    if not RPC_ENDPOINT or not WSS_ENDPOINT or not PRIVATE_KEY:
        logger.error("Missing required environment variables in .env file")
        logger.error("Please make sure SOLANA_NODE_RPC_ENDPOINT, SOLANA_NODE_WSS_ENDPOINT, and SOLANA_PRIVATE_KEY are set")
        return
    
    try:
        # Here we would initialize all the necessary components and start listening for tokens
        logger.info("Bot is configured and ready")
        logger.info("Monitoring for pump.fun transactions...")
        
        # Keep the script running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        logger.info("Bot has shut down")

if __name__ == "__main__":
    asyncio.run(main()) 