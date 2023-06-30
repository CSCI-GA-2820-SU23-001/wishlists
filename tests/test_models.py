"""
Test cases for Wishlist Model

"""
import os
import logging
import unittest
from service import app
from service.models import Wishlist, Product, DataValidationError, db
from tests.factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  Wishlist   M O D E L   T E S T   C A S E S
######################################################################


class TestWishlist(unittest.TestCase):
    """ Test Cases for Wishlist Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Product).delete()  # clean up the last tests
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """It should Create a Wishlist and assert that it exists"""
        fake_wishlist = WishlistFactory()
        # pylint: disable=unexpected-keyword-arg
        wishlist = Wishlist(
            user_id=fake_wishlist.user_id,
            wishlist_name=fake_wishlist.wishlist_name
        )
        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.user_id, fake_wishlist.user_id)
        self.assertEqual(wishlist.wishlist_name, fake_wishlist.wishlist_name)

    def test_add_a_wishlist(self):
        """It should Create a Wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_list_all_wishlists(self):
        """It should List all Wishlists in the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        for wishlist in WishlistFactory.create_batch(10):
            wishlist.create()
        # Assert that there are now 5 wishlists in the database
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 10)
