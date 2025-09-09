from pyfinn.api import app

# Expose the Flask WSGI application for Vercel's Python builder.
__all__ = ["app"]
