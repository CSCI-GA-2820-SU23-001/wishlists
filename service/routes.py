"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Wishlist

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
#  LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_all_wishlists():
    """Retrieves all of Wishlists from the database"""
    app.logger.info("Request for a List of Wishlists")
    # Return as an array of JSON
    wishlists = [wishlist.serialize() for wishlist in Wishlist.all()]
    return make_response(jsonify(wishlists), status.HTTP_200_OK)
