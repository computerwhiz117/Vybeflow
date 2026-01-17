try:
    from . import create_app  # When running as part of the Vybeflow package
except ImportError:  # Fallback when executed as a top-level module
    from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)