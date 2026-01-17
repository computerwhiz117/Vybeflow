"""
WSGI entry point for VybeFlow application
"""

try:
    from .app import app  # When imported as package
except ImportError:  # Fallback when run as a top-level module
    from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
