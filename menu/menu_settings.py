import os

# Get the image max size from environment variables, defaulting to 1MB (1048576 bytes) if not set
limit: int = int(os.environ.get("Category_ICON_MAX_SIZE", 1))  # Default to 1MB
Category_ICON_MAX_SIZE = limit * 1024 * 1024  # Convert to bytes
