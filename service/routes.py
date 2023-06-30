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
# Place your REST API code here ...


######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route("/wishlist", methods=["POST"])
def create_wishlist():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create a Wishlist")
    check_content_type("application/json")

    # Create the account
    wishlist = Wishlist()
    data = request.get_json()
    if wishlist.find_by_name(data["wishlist_name"]).count() > 0:
        abort(
            status.HTTP_409_CONFLICT
        )
    else:
        wishlist.deserialize(data)
        wishlist.create()
        return make_response(
            "", status.HTTP_201_CREATED,
        )


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
