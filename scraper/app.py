from flask import Flask
from scraper.blueprints.scrape import scrape_bp

def create_app():
    """
    App factory pattern - instead of creating the Flask app at module level,
    we wrap it in a function. This makes it easier to test and configure
    for different environments (dev, prod, test).
    """
    app = Flask(__name__)

    #register the scrape blueprint
    #url_prefix means all routes in this blueprint start with /api
    app.register_blueprint(scrape_bp, url_prefix="/api")

    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "scraper"}
    return app


#only runs when this file is executed directly
#not when imported by another module
if __name__ == "__main__":
    app = create_app()
    #port 5001 - FastAPI is on 8000, so we use a different port
    app.run(port=5001, debug=True)