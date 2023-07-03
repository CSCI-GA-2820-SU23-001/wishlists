"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Wishlist, Product

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
# RETRIEVE AN ACCOUNT
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single wishlist

    This endpoint will return an Wishlist based on it's id
    """
    app.logger.info("Request for Wishlist with id: %s", wishlist_id)

    # See if the account exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{wishlist_id}' could not be found.",
        )

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)

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
@app.route("/wishlists", methods=["POST"])
def create_wishlist():
    # TODO Location for read/lookup wishlist
    """
    Creates a Wishlist
    This endpoint will create a wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create a Wishlist")
    check_content_type("application/json")

    # Create the account
    # wishlist = Wishlist()
    # data = request.get_json()
    # if wishlist.find_by_name(data["wishlist_name"]).count() > 0:
    #     abort(
    #         status.HTTP_409_CONFLICT, f"Name: {data['wishlist_name']} has been taken.",
    #     )
    # else:
    wishlist = Wishlist()
    data = request.get_json()
    wishlist.deserialize(data)
    wishlist.create()

    app.logger.info("New wishlist %s created!", wishlist.wishlist_name)
    res=wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id = wishlist.id, _external=True)
    return jsonify(res), status.HTTP_201_CREATED,{"Location": location_url}


@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    "Delete a wishlist"
    app.logger.info(f"Request to delete wishlist with id: {wishlist_id}")
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------
#                P R O D U C T   M E T H O D S
# ---------------------------------------------------------------------
######################################################################
# ADD A PRODUCT TO A WISHLIST
######################################################################

@app.route('/wishlists/<int:wishlist_id>/products', methods=['POST'])
def create_product(wishlist_id):
    """
    Add a product to a wishlist
    This endpoint will add a product to a wishlist.
    """
    app.logger.info("Request to add a Product for Wishlist with id: %s", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)

    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found.",
        )

    product = Product()
    product.deserialize(request.get_json())

    # adding to wishlist
    wishlist.wishlist_products.append(product)
    wishlist.update()

    message = product.serialize()

    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# LIST ALL PRODUCTS
######################################################################

@app.route("/wishlists/<int:wishlist_id>/products", methods=["GET"])
def list_product(wishlist_id):
    app.logger.info("Request to list all Products for a wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' cannot be found.",
        )
    res = [wishlist.serialize() for product in wishlist.wishlist_products]
    return make_response(jsonify(res), status.HTTP_200_OK)

######################################################################
# RETRIEVE A PRODUCT FROM WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/products/<int:product_id>", methods = ["GET"])
def get_products(wishlist_id, product_id):
    """
    this endpoint returns a product in the wishlist
    """
    app.logger.info("Request to retrieve a product with id %s for Wishlist %s", product_id, wishlist_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.id)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route('/wishlists/<int:wishlist_id>/products/<int:product_id>', methods=['DELETE'])
def remove_product(wishlist_id, product_id):
    """
    Remove a product from a wishlist
    This endpoint will remove a product from a wishlist.
    """
    app.logger.info("Request to delete product %s for Wishlist id: %s", wishlist_id, product_id)
    product = Product.find(product_id)

    if product:
        product.delete()

    app.logger.info("Product with ID [%s] is deleted from wishlist [%s]", product_id, wishlist_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

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
