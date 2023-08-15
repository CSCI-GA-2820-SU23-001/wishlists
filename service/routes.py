"""
Wishlist Service

This microservice handles the management of wishlists and their contents
"""

from flask import jsonify, request, make_response, abort
from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Wishlist, Product

# Import Flask application
from . import app, api


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Base URL for Wishlists service """
    return app.send_static_file("index.html")


######################################################################
# R E S T   A P I   E N D P O I N T S
######################################################################


# Define the Product model so that the docs can reflect what can be sent
create_product_model = api.model(
    "Product",
    {
        "wishlist_id": fields.Integer(required=True, description="Id of the wishlist"),
        "product_id": fields.Integer(required=True, description="SKU of the product"),
        "product_name": fields.String(required=True, description="Name of the product"),
        "product_price": fields.Float(required=True, description="Price of the product"),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_product_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The Id of the item assigned internally by the service"
        ),
        "wishlist_id": fields.Integer(
            readOnly=True, description="The Id of the wishlist to which the item belongs"
        ),
    },
)

# Define the Wishlist model so that the docs can reflect what can be sent
create_wishlist_model = api.model(
    "Wishlist",
    {
        "user_id": fields.Integer(required=True, description="Id of the user owning the wishlist"),
        "wishlist_name": fields.String(required=True, description="Name of the wishlist"),
        "archived": fields.Boolean(required=True, description="Is the wishlist archived?"),
        "wishlist_products": fields.List(fields.Nested(product_model), required=False, description="Products in the wishlist"),
    },
)

wishlist_model = api.inherit(
    "WishlistModel",
    create_wishlist_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The Id of the wishlist assigned internally by the service"
        ),
        "wishlist_products": fields.List(
            fields.Nested(product_model),
            required=False, description="Products in the wishlist"
        )
    },
)

# Wishlist Query String Arguments
wishlist_args = reqparse.RequestParser()
wishlist_args.add_argument(
    "wishlist_name", type=str, location="args", required=False, help="Filter Wishlists by name"
)

# Product Query String Arguments
product_args = reqparse.RequestParser()
product_args.add_argument(
    "product_id", type=int, location="args", required=False, help="Filter Wishlists by SKU"
)


######################################################################
# PATH: /wishlists/<wishlist_id>
######################################################################
@api.route("/wishlists/<int:wishlist_id>")
@api.param("wishlist_id", "The Wishlist identifier")
class WishlistResource(Resource):
    """ Handles all interactions with a Wishlist """

    # ---------------------------------------------------------------------
    #                READ A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("get_wishlists")
    @api.response(404, "Wishlist could not be found")
    @api.marshal_with(wishlist_model)
    def get(self, wishlist_id):
        """
        Get a Wishlist

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

        return wishlist.serialize(), status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                UPDATE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("update_wishlists")
    @api.response(404, "Wishlist not found")
    @api.response(400, "The posted Wishlist data was not valid")
    @api.response(409, "Wishlist name already exists")
    @api.response(415, "Invalid header content-type")
    @api.expect(create_wishlist_model)
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Update a Wishlist

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
        body = api.payload

        # Checking for conflicts when renaming
        update_wl = Wishlist.find_by_name(body['wishlist_name'])
        if len(update_wl) > 0:
            if update_wl[0].id != wishlist.id:
                abort(
                    status.HTTP_409_CONFLICT,
                    f"Wishlist with '{body['wishlist_name']}' already exists."
                )

        wishlist.deserialize(body)
        wishlist.update()

        return wishlist.serialize(), status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                DELETE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("delete_wishlists")
    @api.response(204, "Wishlist deleted")
    def delete(self, wishlist_id):
        """
        Delete a wishlist

        This endpoint will delete a Wishlist based on the id specified in the path
        """
        app.logger.info("Request to delete wishlist with id: %s", wishlist_id)

        # Retrieve the wishlist to delete, and delete it if it exists
        wishlist = Wishlist.find(wishlist_id)
        if wishlist:
            wishlist.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# PATH: /wishlists
######################################################################
@api.route("/wishlists", strict_slashes=False)
class WishlistCollection(Resource):
    """ Handles all interactions with collections of Wishlists """

    # ---------------------------------------------------------------------
    #                LIST ALL WISHLISTS
    # ---------------------------------------------------------------------
    @api.doc("list_wishlists")
    @api.expect(wishlist_args, validate=True)
    @api.marshal_list_with(wishlist_model)
    def get(self):
        """
        Return all wishlists

        This endpoint will return all Wishlists in the database
        """
        app.logger.info("Request for a list of Wishlists")

        # Filtering by wishlist name, if needed
        args = wishlist_args.parse_args()
        if args["wishlist_name"]:
            wishlists = Wishlist.find_by_name(args["wishlist_name"])
            if len(wishlists) == 0:
                abort(
                    status.HTTP_404_NOT_FOUND,
                    f"wishlist with '{args['wishlist_name']}' doesn't exist.")
            wishlists = [wishlists[0].serialize()]
        else:
            # Return as an array of JSON
            wishlists = [wishlist.serialize() for wishlist in Wishlist.all()]

        return wishlists, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                CREATE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("create_wishlists")
    @api.response(400, "Invalid wishlist request body")
    @api.response(409, "Wishlist name taken")
    @api.response(415, "Invalid header content-type")
    @api.expect(create_wishlist_model)
    @api.marshal_with(wishlist_model, code=201)
    def post(self):
        """
        Create a wishlist

        This endpoint will create a Wishlist based on the data in the body that is posted
        """
        app.logger.info("Request to create a Wishlist")
        check_content_type("application/json")

        # Create the wishlist
        wishlist = Wishlist()
        data = api.payload
        wishlist.deserialize(data)
        if len(Wishlist.find_by_name(data["wishlist_name"])) > 0:
            abort(
                status.HTTP_409_CONFLICT,
                f"Name: {data['wishlist_name']} has been taken."
            )
        else:
            wishlist.create()

        res = wishlist.serialize()
        location_url = api.url_for(WishlistResource, wishlist_id=wishlist.id, _external=True)

        return res, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# PATH: /wishlists/<wishlist_id>/archive
######################################################################
@api.route("/wishlists/<int:wishlist_id>/archive")
@api.param("wishlist_id", "The Wishlist identifier")
class ArchiveResource(Resource):
    """ Archive action on a Wishlist """

    # ---------------------------------------------------------------------
    #                ARCHIVE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("archive_wishlists")
    @api.response(404, "Wishlist not found")
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Archive a wishlist

        This action route will archive the given Wishlist
        """
        app.logger.info("Request to archive wishlist with id: %s", wishlist_id)

        # Retrieve the wishlist to be archived, and abort if not found
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' could not be found."
            )

        # Archive the fetched wishlist
        wishlist.archived = True
        wishlist.update()

        return wishlist.serialize(), status.HTTP_200_OK


######################################################################
# PATH: /wishlists/<wishlist_id>/unarchive
######################################################################
@api.route("/wishlists/<int:wishlist_id>/unarchive")
@api.param("wishlist_id", "The Wishlist identifier")
class UnarchiveResource(Resource):
    """ Unarchive action on a Wishlist """

    # ---------------------------------------------------------------------
    #                UNARCHIVE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("unarchive_wishlists")
    @api.response(404, "Wishlist not found")
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Unarchive a wishlist

        This action route will unarchive the given Wishlist
        """
        app.logger.info("Request to unarchive wishlist with id: %s", wishlist_id)

        # Retrieve the wishlist to be unarchived, and abort if not found
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' could not be found."
            )

        # Archive the fetched wishlist
        wishlist.archived = False
        wishlist.update()

        return wishlist.serialize(), status.HTTP_200_OK


######################################################################
# PATH: /wishlists/<wishlist_id>/products/<product_id>
######################################################################
@api.route("/wishlists/<int:wishlist_id>/products/<int:product_id>")
@api.param("wishlist_id", "Wishlist identifier")
@api.param("product_id", "Item identifier")
class ItemResource(Resource):
    """ Handles all interactions with an Item """

    # ---------------------------------------------------------------------
    #                READ AN ITEM
    # ---------------------------------------------------------------------
    @api.doc("get_items")
    @api.response(404, "Item not found")
    @api.marshal_with(product_model)
    def get(self, wishlist_id, product_id):
        """
        Get an Item

        This endpoint returns the requested product from the specified wishlist
        """
        app.logger.info("Request to retrieve a Product with id %s from Wishlist %s", product_id, wishlist_id)

        # See if the product exists, and abort if it does not
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

        return product.serialize(), status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                UPDATE AN ITEM
    # ---------------------------------------------------------------------
    @api.doc("update_items")
    @api.response(404, "Wishlist Item not found")
    @api.response(400, "Posted Item data not valid")
    @api.response(415, "Invalid header content-type")
    @api.expect(create_product_model)
    @api.marshal_with(product_model)
    def put(self, wishlist_id, product_id):
        """
        Update a product

        This endpoint updates the specified product from the given wishlist
        """
        app.logger.info("Request to update product %s in Wishlist %s", product_id, wishlist_id)
        check_content_type("application/json")

        # See if the product exists, and abort if it does not
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found")

        original_wishlist_id = product.wishlist_id
        product.deserialize(api.payload)
        product.id = product_id
        product.wishlist_id = original_wishlist_id
        product.update()

        return product.serialize(), status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                DELETE AN ITEM
    # ---------------------------------------------------------------------
    @api.doc("delete_items")
    @api.response(204, 'Item deleted')
    def delete(self, wishlist_id, product_id):
        """
        Remove a product from a wishlist

        This endpoint will remove the given product from the specified wishlist
        """
        app.logger.info("Request to delete product %s for Wishlist id: %s", product_id, wishlist_id)

        # See if the product exists, and delete it if it does
        product = Product.find(product_id)
        if product:
            product.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# PATH: /wishlists/<wishlist_id>/products
######################################################################
@api.route("/wishlists/<int:wishlist_id>/products", strict_slashes=False)
@api.param("wishlist_id", "Wishlist identifier")
class ItemCollection(Resource):
    """ Handles all interactions with collections of Items """

    # ---------------------------------------------------------------------
    #                LIST ALL ITEMS
    # ---------------------------------------------------------------------
    @api.doc("list_items")
    @api.response(404, 'Wishlist not found')
    @api.marshal_list_with(product_model)
    def get(self, wishlist_id):
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
        args = product_args.parse_args()
        if args["product_id"]:
            res = [product for product in res if product["product_id"] == int(args["product_id"])]
            if len(res) == 0:
                abort(
                    status.HTTP_404_NOT_FOUND,
                    f"Product with id '{args['product_id']}' cannot be found."
                )

        return res, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    #                CREATE AN ITEM
    # ---------------------------------------------------------------------
    @api.doc("create_items")
    @api.response(400, "Invalid item request body")
    @api.response(404, "Wishlist id not found")
    @api.response(415, "Invalid header content-type")
    @api.expect(create_product_model)
    @api.marshal_with(product_model, code=201)
    def post(self, wishlist_id):
        """
        Create an Item

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
        product.deserialize(api.payload)

        # Adding the product to the wishlist
        wishlist.wishlist_products.append(product)
        wishlist.update()

        message = product.serialize()
        location_url = api.url_for(ItemResource, wishlist_id=wishlist.id, product_id=product.id, _external=True)
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# K U B E R N E T E S   H E A L T H   C H E C K
######################################################################
@app.route('/health')
def check_kubernetes():
    """
    Health check for kubernetes
    """
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)


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
