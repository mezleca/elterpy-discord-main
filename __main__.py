import os
import asyncio

from src.bot import main
from src.envs import BOT_TOKEN

# run the bot
if __name__ == "__main__":
    asyncio.run(main(BOT_TOKEN))