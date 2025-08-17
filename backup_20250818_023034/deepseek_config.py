import os
from dotenv import load_dotenv

class DeepSeekConfig:
    """Configuration for DeepSeek API integration with proper LiteLLM format"""
    
    @staticmethod
    def setup_environment():
        """Setup environment variables for DeepSeek"""
        load_dotenv()
        
        # Set the base URL for DeepSeek
        os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"
        
        # Default model with proper provider prefix for LiteLLM
        model_name = os.getenv("OPENAI_MODEL_NAME", "deepseek-chat")
        
        # Ensure model has the deepseek/ prefix for LiteLLM
        if not model_name.startswith("deepseek/"):
            if model_name == "deepseek-chat":
                model_name = "deepseek/deepseek-chat"
            elif model_name == "deepseek-coder":
                model_name = "deepseek/deepseek-coder"
            elif model_name == "deepseek-reasoner":
                model_name = "deepseek/deepseek-reasoner"
            else:
                model_name = f"deepseek/{model_name}"
        
        os.environ["OPENAI_MODEL_NAME"] = model_name
        
        # Validate API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        return {
            "api_key": api_key,
            "base_url": os.getenv("OPENAI_API_BASE", "https://api.deepseek.com"),
            "model": model_name,
            "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "4000"))
        }
    
    @staticmethod
    def get_model_config():
        """Get model configuration for CrewAI"""
        config = DeepSeekConfig.setup_environment()
        
        return {
            "model": config["model"],
            "base_url": config["base_url"],
            "api_key": config["api_key"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"]
        }
    
    @staticmethod
    def print_config():
        """Print current configuration for debugging"""
        try:
            config = DeepSeekConfig.setup_environment()
            print("🔍 DeepSeek Configuration:")
            print(f"   Model: {config['model']}")
            print(f"   Base URL: {config['base_url']}")
            print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "   API Key: Not set")
            print(f"   Temperature: {config['temperature']}")
            print(f"   Max Tokens: {config['max_tokens']}")
        except Exception as e:
            print(f"❌ Configuration error: {e}")