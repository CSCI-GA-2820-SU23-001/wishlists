"""
TestWishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import Wishlist, Product, db, init_db
from tests.factories import WishlistFactory, ProductFactory
from service.common import status  # HTTP Status Codes

logger = logging.getLogger("flask.app")

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/wishlists"


######################################################################
#  T E S T   C A S E S
######################################################################


class TestWishlistServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        # db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        # db.session.query(Wishlist).delete()  # clean up the last tests
        # db.session.query(Product).delete()  # clean up the last tests
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count):
        """Factory method to create accounts in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistFactory()
            resp = self.client.post(BASE_URL, json=wishlist.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Wishlist"
            )
            new_wishlist = resp.get_json()
            wishlist.id = new_wishlist["id"]
            wishlists.append(wishlist)
        return wishlists

    ######################################################################
    #  W I S H L I S T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_wishlist_list(self):
        """It should Get a list of Wishlists"""
        self._create_wishlists(10)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 10)

    def test_create_a_valid_wishlist(self):
        """It should create a wishlist"""
        wishlist = WishlistFactory()
        resp = self.client.post(
            BASE_URL, json=wishlist.serialize(), content_type="application/json"
        )
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED
            # "Could not create test Wishlist"
        )
       

        location = resp.headers.get("location", None)
        self.assertIsNotNone(location)

        new_wishlist = resp.get_json()
        # Do not need to check for wishlist id, since it will be assigned with unique id while creating one.
        self.assertEqual(
            new_wishlist["user_id"], wishlist.user_id, "wishlist user_id does not match"
        )
        self.assertEqual(
            new_wishlist["wishlist_name"], wishlist.wishlist_name, "wishlist_name does not match"
        )
        self.assertEqual(
            new_wishlist["wishlist_products"], wishlist.wishlist_products, "wishlist products does not match"
        )

        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(
            new_wishlist["user_id"], wishlist.user_id, "wishlist user_id does not match"
        )
        self.assertEqual(
            new_wishlist["wishlist_name"], wishlist.wishlist_name, "wishlist_name does not match"
        )
        self.assertEqual(
            new_wishlist["wishlist_products"], wishlist.wishlist_products, "wishlist products does not match"
        )

    def test_delete_wishlist(self):
        """ It should Delete a Wishlist"""
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

     ######################################################################
    #  P R O D U C T   T E S T   C A S E S
    ######################################################################

    def test_add_product(self):
        """Add a Product to a Wishlist"""
        wishlist = self._create_wishlists(1)[0] # create a single wishlist
        logger.info(wishlist)
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED) # assert that the product was added successfully

        data = resp.get_json() # get the data returned (this should be the created product)
        logging.debug(data)

        self.assertEqual(data['product_id'], product.product_id)
        self.assertEqual(data['product_name'], product.product_name)
        self.assertEqual(data['product_price'], product.product_price)

    def test_remove_product(self):
        """Remove a Product from a Wishlist"""
        wishlist = self._create_wishlists(1)[0] # create a single wishlist
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED) # assert that the product was added successfully

        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]

        # remove the product from the wishlist
        resp = self.client.delete(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json"
            )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT) # assert that the product was removed successfully

        # retrieve it back and make sure product is not there
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

