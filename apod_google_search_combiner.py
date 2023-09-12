from dotenv import load_dotenv

# Load environment variables from .env into the script's environment
load_dotenv()

# check if required environment variables are set
required_env_vars = ['nasa_api_key', 'google_api_key', 'search_engine_id']
for var_name in required_env_vars:
    if var_name not in os.environ:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
