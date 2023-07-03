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
from service.models import Wishlist, Product, db
from tests.factories import WishlistFactory
from service.common import status  # HTTP Status Codes

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
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Product).delete()  # clean up the last tests
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
            status.HTTP_201_CREATED,
            "Could not create test Wishlist"
        )
        # TODO: check location exist

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

        # TODO: check location was correct by getting it.

    def test_delete_wishlist(self):
        """ It should Delete a Wishlist"""
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_rename_wishlist(self):
        """ It should rename a Wishlist"""
        #generate 2 wishlist and insert into db
        wishlist1 = WishlistFactory()
        wishlist2 = WishlistFactory()
        res=self.client.post(BASE_URL, json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        data1=res.get_json()
        res=self.client.post(BASE_URL, json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        data2=res.get_json()

        #update 2 data with same name. 1st should get 200 and 2nd should get 409
        wishlist1.wishlist_name = "new_Name"
        wishlist2.wishlist_name = "new_Name"
        res1 = self.client.put(f"{BASE_URL}/{data1['id']}", json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res1.status_code, status.HTTP_200_OK,"Could not rename Wishlist1")
        res2 = self.client.put(f"{BASE_URL}/{data2['id']}", json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res2.status_code, status.HTTP_409_CONFLICT,"Could not rename Wishlist2")

        #check updated data
        updated_wishlist = res1.get_json()
        self.assertEqual(updated_wishlist["wishlist_name"], "new_Name")

        