from app import create_app
from dotenv import load_dotenv
import os

def main():
    """Main application entry point."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Create Flask application with the specified environment
    env = os.getenv('FLASK_ENV', 'development').lower()
    if env not in ['development', 'testing', 'production']:
        env = 'development'
    
    # Map environment to configuration name
    config_map = {
        'development': 'development',
        'testing': 'testing',
        'production': 'production'
    }
    config_name = config_map.get(env, 'development')
    
    app = create_app(config_name)
    
    # Run the application
    app.run(
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=env == 'development'
    )

if __name__ == '__main__':
    main()
