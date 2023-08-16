"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from flask_restx import Api
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

app.url_map.strict_slashes = False

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Wishlist Demo REST API Service",
    description="This is a sample server Wishlist service.",
    default="wishlists",
    default_label="Wishlist operations",
    doc="/apidocs",  # default also could use doc='/apidocs/'
    prefix="/api",
)

# Dependencies require we import the routes AFTER the Flask app is created
# pylint: disable=wrong-import-position, wrong-import-order, cyclic-import
from service import routes, models  # noqa: E402, E261
# pylint: disable=wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401, E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our SQLAlchemy tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
