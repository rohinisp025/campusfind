import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.item_routes import item_bp
from routes.claim_routes import claim_bp
from routes.admin_routes import admin_bp
from routes.notification_routes import notification_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all routes under /api and /uploads
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notification_bp)

    # Serve uploaded images statically
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # API Health Check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'app': 'CampusFind Lost and Found Portal API',
            'version': '1.0.0'
        }), 200

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource or endpoint not found.'}), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return jsonify({'error': 'File size exceeds maximum allowed limit (16MB).'}), 413

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error occurred.'}), 500

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print(" CampusFind Flask Backend is starting on http://127.0.0.1:5000 ")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
