"""
Models for Wishlist

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Wishlist.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class Wishlist(db.Model):
    """
    Class that represents a Wishlist

    Schema Description:
    id = primary key for user-wishlist table
    user_id = id of the user who owns the wishlist
    wishlist_name = user-assigned name of the wishlist
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    wishlist_name = db.Column(db.String(63), nullable=False)
    wishlist_products = db.relationship("Product", backref="wishlist", passive_deletes=True)

    def __repr__(self):
        return f"<Wishlist {self.wishlist_name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self.wishlist_name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.wishlist_name)
        db.session.commit()

    def delete(self):
        """ Removes a Wishlist from the data store """
        logger.info("Deleting %s", self.wishlist_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Wishlist into a dictionary """
        wishlist = {
            "id": self.id,
            "user_id": self.user_id,
            "wishlist_name": self.wishlist_name,
            "wishlist_products": []
        }
        for product in self.wishlist_products:
            wishlist["wishlist_products"].append(product.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.user_id = data["user_id"]
            self.wishlist_name = data["wishlist_name"]

            product_list = data.get("wishlist_products")
            if product_list is not None:
                for json_product in product_list:
                    product = Product()
                    product.deserialize(json_product)
                    self.wishlist_products.append(product)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlist: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing wishlists database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlists in the database """
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Wishlist by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, by_name):
        """Returns all Wishlists with the given name

        Args:
            name (string): the name of the Wishlists you want to match
        """
        logger.info("Processing name query for %s ...", by_name)
        return cls.query.filter(cls.wishlist_name == by_name)


class Product(db.Model):
    """
    Class that represents an Product

    Schema Description:
    id = primary key for product-wishlist table
    wishlist_id = id of the wishlist the product is mapped to
    product_id = unique id of the product (sku)
    product_name = name of the product
    product_price = current price of the product
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(63), nullable=False)
    product_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.product_name} id=[{self.product_id}] in Wishlist {self.wishlist_id}>"

    def create(self):
        """
        Creates an Product-Wishlist mapping to the database
        """
        logger.info("Adding product %s to wishlist %d", self.product_name, self.wishlist_id)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Product-Wishlist mapping to the database
        """
        logger.info("Saving product %s in wishlist %d", self.product_name, self.wishlist_id)
        db.session.commit()

    def delete(self):
        """ Removes an Product-Wishlist mapping from the data store """
        logger.info("Deleting product %s from wishlist %d", self.product_name, self.wishlist_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Wishlist into a dictionary """
        product = {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_price": self.product_price
        }
        return product

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.product_id = data["product_id"]
            self.product_name = data["self.product_name"]
            self.product_price = data["self.product_price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing products database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlists in the database """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Wishlist by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, by_name):
        """Returns all Products with the given name

        Args:
            name (string): the name of the Product you want to match
        """
        logger.info("Processing name query for %s ...", by_name)
        return cls.query.filter(cls.product_name == by_name)
