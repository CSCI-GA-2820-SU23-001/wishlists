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
    wishlist_items = db.relationship("Item", backref="wishlist", passive_deletes=True)

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
            "wishlist_items": []
        }
        for item in self.wishlist_items:
            wishlist["wishlist_items"].append(item.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.user_id = data["user_id"]
            self.wishlist_name = data["name"]
            item_list = data.get("wishlist_items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.wishlist_items.append(item)
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
        return cls.query.filter(cls.name == by_name)


class Item(db.Model):
    """
    Class that represents an Item
    
    Schema Description:
    id = primary key for item-wishlist table
    wishlist_id = id of the wishlist the item is mapped to
    item_id = unique id of the item (sku)
    item_name = name of the item
    item_price = current price of the item
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(63), nullable=False)
    item_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Item {self.item_name} id=[{self.item_id}] in Wishlist {self.wishlist_id}>"

    def create(self):
        """
        Creates an Item-Wishlist mapping to the database
        """
        logger.info("Adding item %s to wishlist %d", self.item_name, self.wishlist_id)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Item-Wishlist mapping to the database
        """
        logger.info("Saving item %s in wishlist %d", self.item_name, self.wishlist_id)
        db.session.commit()

    def delete(self):
        """ Removes an Item-Wishlist from the data store """
        logger.info("Deleting item %s from wishlist %d", self.item_name, self.wishlist_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Wishlist into a dictionary """
        item = {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "item_id": self.item_id, 
            "item_name": self.item_name,
            "item_price": self.item_price
        }
        return item
    
    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.item_id = data["item_id"]
            self.item_name = data["self.item_name"]
            self.item_price = data["self.item_price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self
    
    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing items database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlists in the database """
        logger.info("Processing all Items")
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
        return cls.query.filter(cls.name == by_name)
