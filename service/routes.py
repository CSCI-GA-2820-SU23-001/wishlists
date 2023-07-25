"""
Wishlist Service

This microservice handles the management of wishlists and their contents
"""

from flask import jsonify, request, url_for, make_response, abort
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
        jsonify(
            name="Wishlist REST API Service",
            version="1.0"
        ),
        status.HTTP_200_OK
    )


######################################################################
# R E S T   A P I   E N D P O I N T S
######################################################################


# ---------------------------------------------------------------------
#                W I S H L I S T   M E T H O D S
# ---------------------------------------------------------------------


######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_all_wishlists():
    """
    Return all wishlists

    This endpoint will return all Wishlists in the database
    """
    app.logger.info("Request for a list of Wishlists")

    # Filtering by wishlist name, if needed
    wishlist_name = request.args.get("wishlist_name")
    if wishlist_name:
        wishlists = Wishlist.find_by_name(wishlist_name)
        if len(wishlists) == 0:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"wishlist with '{wishlist_name}' doesn't exist.")
        wishlists = [wishlists[0].serialize()]
    else:
        # Return as an array of JSON
        wishlists = [wishlist.serialize() for wishlist in Wishlist.all()]

    # Filtering by product id, if needed
    product_id = request.args.get("product_id")
    if product_id:
        filtered_wishlists = []
        for wishlist in wishlists:
            for product in wishlist["wishlist_products"]:
                if int(product_id) == product["product_id"]:
                    filtered_wishlists.append(wishlist)
    else:
        filtered_wishlists = wishlists

    return make_response(jsonify(filtered_wishlists), status.HTTP_200_OK)


######################################################################
# RETRIEVE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single wishlist

    This endpoint will return a Wishlist based on the id specified in the path
    """
    app.logger.info("Request for Wishlist with id: %s", wishlist_id)

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found."
        )

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlist():
    """
    Create a wishlist

    This endpoint will create a Wishlist based on the data in the body that is posted
    """
    app.logger.info("Request to create a Wishlist")
    check_content_type("application/json")

    # Create the wishlist
    wishlist = Wishlist()
    data = request.get_json()
    wishlist.deserialize(data)
    if len(Wishlist.find_by_name(data["wishlist_name"])) > 0:
        abort(
            status.HTTP_409_CONFLICT,
            f"Name: {data['wishlist_name']} has been taken."
        )
    else:
        wishlist.create()

    res = wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)

    return make_response(jsonify(res), status.HTTP_201_CREATED, {"Location": location_url})


######################################################################
# UPDATE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlist(wishlist_id):
    """
    Update a wishlist

    This endpoint will update a Wishlist based on the data in the body
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # Retrieve the wishlist if it exists
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found."
        )

    # Update the wishlist with the data posted
    body = request.get_json()

    # Checking for conflicts when renaming
    update_wl = Wishlist.find_by_name(body['wishlist_name'])
    if len(update_wl) > 0:
        abort(
            status.HTTP_409_CONFLICT,
            f"Wishlist with '{body['wishlist_name']}' already exists."
        )

    wishlist.deserialize(body)
    wishlist.update()

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlist(wishlist_id):
    """
    Delete a wishlist

    This endpoint will delete a Wishlist based on the id specified in the path
    """
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)

    # Retrieve the wishlist to delete, and delete it if it exists
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------
#                P R O D U C T   M E T H O D S
# ---------------------------------------------------------------------


######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/wishlists/<int:wishlist_id>/products", methods=["GET"])
def list_products(wishlist_id):
    """
    Return all products in a wishlist

    This endpoint will return all products in the given wishlist
    """
    app.logger.info("Request for all Products in Wishlist with id: %s", wishlist_id)

    # See if the wishlist exists, and abort if it does not
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' cannot be found."
        )

    res = [product.serialize() for product in wishlist.wishlist_products]

    # Filtering, if needed
    product_id = request.args.get("product_id")
    if product_id:
        res = [product for product in res if product["product_id"] == int(product_id)]
        if len(res) == 0:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' cannot be found."
            )

    return make_response(jsonify(res), status.HTTP_200_OK)


######################################################################
# ADD A PRODUCT TO A WISHLIST
######################################################################
@app.route('/wishlists/<int:wishlist_id>/products', methods=['POST'])
def create_product(wishlist_id):
    """
    Add a product to a wishlist

    This endpoint will add a product to a wishlist.
    """
    app.logger.info("Request to add a Product to Wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the wishlist exists, and abort if it does not
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found."
        )

    # Create a product from the JSON data
    product = Product()
    product.deserialize(request.get_json())

    # Adding the product to the wishlist
    wishlist.wishlist_products.append(product)
    wishlist.update()

    message = product.serialize()
    location_url = url_for("get_products", wishlist_id=wishlist.id, product_id=product.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})


######################################################################
# RETRIEVE A PRODUCT FROM A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/products/<int:product_id>", methods=["GET"])
def get_products(wishlist_id, product_id):
    """
    Get a product

    This endpoint returns the requested product from the specified wishlist
    """
    app.logger.info("Request to retrieve a Product with id %s from Wishlist %s", product_id, wishlist_id)

    # See if the product exists, and abort if it does not
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route('/wishlists/<int:wishlist_id>/products/<int:product_id>', methods=['PUT'])
def update_product(wishlist_id, product_id):
    """
    Update a product

    This endpoint updates the specified product from the given wishlist
    """
    app.logger.info("Request to update product %s in Wishlist %s", product_id, wishlist_id)

    # See if the product exists, and abort if it does not
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found")

    original_wishlist_id = product.wishlist_id
    product.deserialize(request.get_json())
    product.id = product_id
    product.wishlist_id = original_wishlist_id
    product.update()

    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route('/wishlists/<int:wishlist_id>/products/<int:product_id>', methods=['DELETE'])
def remove_product(wishlist_id, product_id):
    """
    Remove a product from a wishlist

    This endpoint will remove the given product from the specified wishlist
    """
    app.logger.info("Request to delete product %s for Wishlist id: %s", product_id, wishlist_id)

    # See if the product exists, and delete it if it does
    product = Product.find(product_id)
    if product:
        product.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# HEALTH CHECK FOR KUBERNETES
######################################################################
@app.route('/health')
def check_kubernetes():
    """
    Health check for kubernetes
    """
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK

######################################################################
# U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}"
    )
