"""
Configuration settings for Neo4j Aura connection
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Neo4j Aura connection settings
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate required environment variables
required_vars = ['NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD', 'OPENAI_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 