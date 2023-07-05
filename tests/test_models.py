"""
Test cases for Wishlist Model and Product Model

"""
import os
import logging
import unittest
from service import app
from service.models import Wishlist, Product, db
from tests.factories import WishlistFactory, ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  W I S H L I S T   M O D E L   T E S T   C A S E S
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
        db.session.query(Product).delete()   # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
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
        # Assert that there are now 10 wishlists in the database
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 10)

    def test_read_a_wishlist(self):
        """It should Read a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        # Read it back
        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.user_id, wishlist.user_id)
        self.assertEqual(found_wishlist.wishlist_name, wishlist.wishlist_name)
        self.assertEqual(found_wishlist.wishlist_products, [])

    def test_update_a_wishlist(self):
        """It should Update a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        original_id = wishlist.id
        # Rename the wishlist
        wishlist.wishlist_name = "Test"
        wishlist.update()
        self.assertEqual(wishlist.wishlist_name, "Test")
        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        # Assert that the id remained unchanged
        self.assertEqual(wishlist.id, original_id)
        # Assert that the name was indeed updated
        self.assertEqual(wishlist.wishlist_name, "Test")

    def test_delete_a_wishlist(self):
        """It should Delete a Wishlist"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 0)

    def test_add_wishlist_product(self):
        """It should Create a Wishlist with a Product and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        product = ProductFactory(wishlist=wishlist)
        wishlist.wishlist_products.append(product)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        # Fetch it back
        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(new_wishlist.wishlist_products), 1)
        self.assertEqual(new_wishlist.wishlist_products[0].product_id, product.product_id)
        self.assertEqual(new_wishlist.wishlist_products[0].product_name, product.product_name)
        self.assertAlmostEqual(new_wishlist.wishlist_products[0].product_price, product.product_price)
        # Adding another product
        product2 = ProductFactory(wishlist=wishlist)
        wishlist.wishlist_products.append(product2)
        wishlist.update()
        # Fetch it back
        new_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(new_wishlist.wishlist_products), 2)
        self.assertEqual(new_wishlist.wishlist_products[1].product_id, product2.product_id)
        self.assertEqual(new_wishlist.wishlist_products[1].product_name, product2.product_name)
        self.assertAlmostEqual(new_wishlist.wishlist_products[1].product_price, product2.product_price)

    def test_list_all_wishlist_products(self):
        """It should List all Products in a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        # Assert that it has no products to begin with
        self.assertEqual(wishlist.wishlist_products, [])
        products = ProductFactory.create_batch(5)
        for product in products:
            wishlist.wishlist_products.append(product)
        wishlist.update()
        # Fetch it back
        fetch_wishlist = Wishlist.find(wishlist.id)
        # Assert there are now 5 products in the wishlist
        self.assertEqual(len(fetch_wishlist.wishlist_products), 5)
        # Assert that the products in the wishlist match the ones added
        for i, product in enumerate(products):
            self.assertEqual(fetch_wishlist.wishlist_products[i].product_id, product.product_id)
            self.assertEqual(fetch_wishlist.wishlist_products[i].product_name, product.product_name)
            self.assertAlmostEqual(fetch_wishlist.wishlist_products[i].product_price, product.product_price)

    def test_read_a_product_from_wishlist(self):
        """It should return a Product from a Wishlist"""
        wishlist = WishlistFactory()
        product = ProductFactory(wishlist=wishlist)
        wishlist.create()
        # Obtain the id of the newly created product
        new_product_id = Wishlist.find(wishlist.id).wishlist_products[0].id
        self.assertIsNotNone(new_product_id)
        # Fetch the product from the database
        new_product = Product.find(new_product_id)
        # Ensuring that the data of the fetched product matches with that inserted
        self.assertEqual(product.wishlist_id, wishlist.id)
        self.assertEqual(product.product_id, new_product.product_id)
        self.assertEqual(product.product_name, new_product.product_name)
        self.assertAlmostEqual(product.product_price, new_product.product_price)

    def test_remove_wishlist_product(self):
        """It should remove a Product from a Wishlist"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        product = ProductFactory(wishlist=wishlist)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        product = wishlist.wishlist_products[0]
        product.delete()
        wishlist.update()
        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(wishlist.wishlist_products), 0)
