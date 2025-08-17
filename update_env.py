def update_env_for_deepseek():
    """Update .env file with correct DeepSeek configuration"""
    
    # Read existing API key if it exists
    existing_key = "sk-e941fc978b6144258a388c4c0f6553c4"
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    existing_key = line.split('=', 1)[1].strip()
                    break
    
    new_env_content = f"""# DeepSeek API Configuration (Fixed)
OPENAI_API_KEY={existing_key}
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL_NAME=deepseek/deepseek-chat

# Available DeepSeek Models (with proper LiteLLM format):
# deepseek/deepseek-chat - General purpose conversational model (recommended)
# deepseek/deepseek-coder - Optimized for coding tasks  
# deepseek/deepseek-reasoner - Enhanced reasoning capabilities

# Optional parameters
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_MAX_TOKENS=4000
"""
    
    with open('.env', 'w') as f:
        f.write(new_env_content)
    
    print("✅ Updated .env file with correct DeepSeek configuration")
    print("⚠️  Don't forget to update OPENAI_API_KEY with your actual DeepSeek API key!")

if __name__ == "__main__":
    update_env_for_deepseek()
