import os
from dotenv import load_dotenv

class DeepSeekConfig:
    """Fixed DeepSeek configuration for LiteLLM compatibility"""
    
    @staticmethod
    def setup_environment():
        """Setup environment with proper model naming for LiteLLM"""
        load_dotenv()
        
        # Get the raw model name from env
        raw_model = os.getenv("OPENAI_MODEL_NAME", "deepseek-chat")
        
        # Ensure proper LiteLLM format with deepseek/ prefix
        if not raw_model.startswith("deepseek/"):
            if raw_model in ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]:
                model_name = f"deepseek/{raw_model}"
            else:
                model_name = "deepseek/deepseek-chat"  # default
        else:
            model_name = raw_model
        
        # Update environment with corrected model name
        os.environ["OPENAI_MODEL_NAME"] = model_name
        os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        config = {
            "api_key": api_key,
            "base_url": "https://api.deepseek.com", 
            "model": model_name,
            "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "4000"))
        }
        
        return config
    
    @staticmethod
    def get_model_config():
        """Get configuration for CrewAI"""
        return DeepSeekConfig.setup_environment()
    
    @staticmethod
    def print_config():
        """Debug configuration"""
        try:
            config = DeepSeekConfig.setup_environment()
            print("🔍 DeepSeek Configuration:")
            print(f"   Model: {config['model']}")
            print(f"   Base URL: {config['base_url']}")
            print(f"   API Key: {config['api_key'][:8]}..." if config['api_key'] else "Not set")
            print(f"   Temperature: {config['temperature']}")
            print(f"   Max Tokens: {config['max_tokens']}")
        except Exception as e:
            print(f"❌ Config error: {e}")
