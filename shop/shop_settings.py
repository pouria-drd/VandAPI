import os
from dotenv import load_dotenv

load_dotenv()  # Loads the variables from the .env file into the environment

# Get the image max size from environment variables, defaulting to 1MB (1048576 bytes) if not set
limit: int = int(os.getenv("Category_ICON_MAX_SIZE", 1))  # Default to 1MB
Category_ICON_MAX_SIZE = limit * 1024 * 1024  # Convert to bytes
