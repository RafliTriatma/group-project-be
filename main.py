from flask import Flask
import os
from config.setting import create_app

def main():
    # Create the Flask application using the factory function
    app = create_app()
    
    # Run the application
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV', 'development') == 'development'
    )

if __name__ == "__main__":
    main()
