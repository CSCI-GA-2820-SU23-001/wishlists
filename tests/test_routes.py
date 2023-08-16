"""
TestWishlist API Service Test Suite

Test cases can be run with the following:
  green
"""
import os
import logging
from unittest import TestCase
from tests.factories import WishlistFactory, ProductFactory
from service.common import status  # HTTP Status Codes
from service import app
from service.models import Wishlist, db, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/api/wishlists"


######################################################################
#  T E S T   C A S E S
######################################################################

# pylint: disable=too-many-public-methods
class TestWishlistServer(TestCase):
    """ Wishlist Server Tests """

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
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count):
        """Factory method to create accounts in bulk"""
        wishlists = []
        for i in range(count):
            wishlist = WishlistFactory()
            wishlist.wishlist_name = f"wishlist-x-{i}"
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
        """ It should Get a list of Wishlists """
        self._create_wishlists(10)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 10)

    def test_get_wishlist_by_name(self):
        """ It should Get a wishlist with same name """
        wls = self._create_wishlists(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
        wl_name = wls[0].wishlist_name
        res = self.client.get(f'{BASE_URL}?wishlist_name={wl_name}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.get_json()[0]['wishlist_name'], wl_name)
        wr_name = "Wringsoffhasf"
        res = self.client.get(f'{BASE_URL}?wishlist_name={wr_name}')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_wishlist(self):
        """ It should create a wishlist """
        wishlist = WishlistFactory()
        resp = self.client.post(BASE_URL, json=wishlist.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("location", None)
        self.assertIsNotNone(location)
        # Check that data is correct
        new_wishlist = resp.get_json()
        # Do not need to check for wishlist id, since it will be assigned with unique id while creating one.
        self.assertEqual(new_wishlist["user_id"], wishlist.user_id, "wishlist user_id does not match")
        self.assertEqual(new_wishlist["wishlist_name"], wishlist.wishlist_name, "wishlist  name does not match")
        self.assertEqual(new_wishlist["wishlist_products"], wishlist.wishlist_products, "wishlist products do not match")
        # Check that the location header was correct by getting it
        resp = self.client.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["user_id"], wishlist.user_id, "wishlist user_id does not match")
        self.assertEqual(new_wishlist["wishlist_name"], wishlist.wishlist_name, "wishlist_name does not match")
        self.assertEqual(new_wishlist["wishlist_products"], wishlist.wishlist_products, "wishlist products do not match")

    def test_cannot_create_a_wishlist(self):
        """ It should fail to create a Wishlist with an already-existing name """
        wishlist1 = self._create_wishlists(1)[0]
        wishlist2 = WishlistFactory()
        wishlist2.wishlist_name = wishlist1.wishlist_name
        resp = self.client.post(BASE_URL, json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_read_a_wishlist(self):
        """ It should read a Wishlist """
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.get(f"{BASE_URL}/{wishlist.id}", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], wishlist.id)
        self.assertEqual(data["wishlist_name"], wishlist.wishlist_name)
        self.assertEqual(data["user_id"], wishlist.user_id)
        self.assertEqual(wishlist.wishlist_products, [])

    def test_cannot_read_a_wishlist(self):
        """ It should fail to read a non-existent Wishlist """
        wishlist = self._create_wishlists(1)[0]
        non_existent_wishlist_id = wishlist.id + 1
        resp = self.client.get(f"{BASE_URL}/{non_existent_wishlist_id}", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_wishlist(self):
        """ It should update a Wishlist """
        wishlist1 = WishlistFactory()
        wishlist2 = WishlistFactory()
        res = self.client.post(BASE_URL, json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data1 = res.get_json()
        res = self.client.post(BASE_URL, json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data2 = res.get_json()
        # Attempt to rename both to the same name
        wishlist1.wishlist_name = "new_Name"
        wishlist2.wishlist_name = "new_Name"
        res1 = self.client.put(f"{BASE_URL}/{data1['id']}", json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res1.status_code, status.HTTP_200_OK, "Could not rename Wishlist1")
        res2 = self.client.put(f"{BASE_URL}/{data2['id']}", json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res2.status_code, status.HTTP_409_CONFLICT, "Incorrectly renamed Wishlist2")
        # Verify the updated data
        wl1 = Wishlist.find(data1['id']).wishlist_name
        wl2 = Wishlist.find(data2['id']).wishlist_name
        self.assertEqual(wl1, "new_Name")
        self.assertNotEqual(wl2, "new_Name")

    def test_cannot_update_a_wishlist(self):
        """ It should fail to update a Wishlist when it doesn't exist or the desired name already exists """
        created_wishlists = self._create_wishlists(2)
        created_wishlist_ids = [wishlist.id for wishlist in created_wishlists]
        # Picking a non-existent wishlist id
        non_existent_wishlist_id = created_wishlist_ids[0]
        while non_existent_wishlist_id in created_wishlist_ids:
            non_existent_wishlist_id += 1
        # Attempting to update a non-existent wishlist
        wishlist = WishlistFactory()
        resp = self.client.put(
            f"{BASE_URL}/{non_existent_wishlist_id}",
            json=wishlist.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        # Attempting to rename a wishlist with an already-consumed name
        wishlist.wishlist_name = created_wishlists[0].wishlist_name
        resp = self.client.put(
            f"{BASE_URL}/{created_wishlist_ids[1]}",
            json=wishlist.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_delete_wishlist(self):
        """ It should Delete a Wishlist """
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_rename_wishlist(self):
        """ It should rename a Wishlist"""
        # generate 2 wishlist and insert into db
        wishlist1 = WishlistFactory()
        wishlist2 = WishlistFactory()
        res = self.client.post(BASE_URL, json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data1 = res.get_json()
        res = self.client.post(BASE_URL, json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data2 = res.get_json()

        # update 2 data with same name. 1st should get 200 and 2nd should get 409
        wishlist1.wishlist_name = "new_Name"
        wishlist2.wishlist_name = "new_Name"
        res1 = self.client.put(f"{BASE_URL}/{data1['id']}", json=wishlist1.serialize(), content_type="application/json")
        self.assertEqual(res1.status_code, status.HTTP_200_OK, "Could not rename Wishlist1")
        res2 = self.client.put(f"{BASE_URL}/{data2['id']}", json=wishlist2.serialize(), content_type="application/json")
        self.assertEqual(res2.status_code, status.HTTP_409_CONFLICT, "rename Wishlist2, WRONG")

        # check updated data
        wl1 = Wishlist.find(data1['id']).wishlist_name
        wl2 = Wishlist.find(data2['id']).wishlist_name
        self.assertEqual(wl1, "new_Name")
        self.assertNotEqual(wl2, "new_Name")

    def test_archive_wishlist(self):
        """ It should archive a Wishlist """
        wishlist = WishlistFactory()
        wishlist.archived = False
        res = self.client.post(BASE_URL, json=wishlist.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.get_json()
        self.assertEqual(data['archived'], False)
        res = self.client.put(f"{BASE_URL}/{data['id']}/archive")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.get_json()
        self.assertEqual(data['archived'], True)

    def test_cannot_archive_wishlist(self):
        """ It should not archive a non-existent Wishlist """
        wishlist = WishlistFactory()
        wishlist.archived = False
        res = self.client.post(BASE_URL, json=wishlist.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.get_json()
        self.assertEqual(data['archived'], False)
        res = self.client.put(f"{BASE_URL}/{data['id'] + 1}/archive")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unarchive_wishlist(self):
        """ It should unarchive a Wishlist """
        wishlist = WishlistFactory()
        wishlist.archived = True
        res = self.client.post(BASE_URL, json=wishlist.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.get_json()
        self.assertEqual(data['archived'], True)
        res = self.client.put(f"{BASE_URL}/{data['id']}/unarchive")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.get_json()
        self.assertEqual(data['archived'], False)

    def test_cannot_unarchive_wishlist(self):
        """ It should not unarchive a non-existent Wishlist """
        wishlist = WishlistFactory()
        wishlist.archived = True
        res = self.client.post(BASE_URL, json=wishlist.serialize(), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.get_json()
        self.assertEqual(data['archived'], True)
        res = self.client.put(f"{BASE_URL}/{data['id'] + 1}/unarchive")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  P R O D U C T   T E S T   C A S E S
    ######################################################################

    def test_list_products_in_wishlist(self):
        """ It should list all the products in a wishlist """
        wishlist = self._create_wishlists(1)[0]
        products = ProductFactory.create_batch(5)
        for product in products:
            resp = self.client.post(
                f"{BASE_URL}/{wishlist.id}/products",
                json=product.serialize(),
                content_type="application/json",
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Retrieve the list of products in the wishlist
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        # Assert that the number of products in the response matches the number of added products
        self.assertEqual(len(data), 5)
        # Assert that the product details in the response match those of added products
        for i, product in enumerate(products):
            self.assertEqual(data[i]['product_id'], product.product_id)
            self.assertEqual(data[i]['product_name'], product.product_name)
            self.assertEqual(data[i]['product_price'], product.product_price)

    def test_get_products_by_product_id(self):
        """ It should Get a Product with same product_id """
        wishlist = self._create_wishlists(1)[0]
        products = ProductFactory.create_batch(1)
        for product in products:
            resp = self.client.post(
                f"{BASE_URL}/{wishlist.id}/products",
                json=product.serialize(),
                content_type="application/json",
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Retrieve the list of products in the wishlist
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products?product_id={products[0].product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Should not retrieve the list of products in the wishlist, when an incorrect id is passed
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products?product_id={products[0].product_id + 1}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_list_products(self):
        """ It should fail to list the products in a non-existent wishlist """
        wishlist = self._create_wishlists(1)[0]
        products = ProductFactory.create_batch(5)
        for product in products:
            resp = self.client.post(
                f"{BASE_URL}/{wishlist.id}/products",
                json=product.serialize(),
                content_type="application/json",
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Obtain a non-existent wishlist id
        non_existent_wishlist_id = wishlist.id + 1
        resp = self.client.get(
            f"{BASE_URL}/{non_existent_wishlist_id}/products",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product(self):
        """ It should add a Product to a Wishlist """
        wishlist = self._create_wishlists(1)[0]     # create a single wishlist
        app.logger.info(wishlist)
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)     # assert that the product was added successfully
        data = resp.get_json()     # get the data returned (this should be the created product)
        logging.debug(data)
        self.assertEqual(data['product_id'], product.product_id)
        self.assertEqual(data['product_name'], product.product_name)
        self.assertEqual(data['product_price'], product.product_price)

    def test_cannot_add_product(self):
        """ It should fail to add a product to a non-existent Wishlist """
        wishlist = self._create_wishlists(1)[0]     # create a single wishlist
        # Obtaining a non-existent wishlist id
        non_existent_wishlist_id = wishlist.id + 1
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{non_existent_wishlist_id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_product(self):
        """ It should read a Product from a Wishlist """
        # Create a known product
        wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]
        # Retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json"
        )
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["product_id"], product.product_id)
        self.assertEqual(data["product_name"], product.product_name)
        self.assertEqual(data["product_price"], product.product_price)

    def test_cannot_read_a_product(self):
        """ It should fail to read a non-existent Product """
        wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Obtain a non-existent product id
        non_existent_product_id = resp.get_json()["id"] + 1
        resp = self.client.get(f"{BASE_URL}/{non_existent_product_id}", content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """ It should update a Product in a Wishlist """
        # Create a known product
        wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]
        data["product_name"] = "newProduct"
        data["product_price"] = 2.2
        # Send the update back
        res = self.client.put(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            json=data,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Retrieve it back, and ensure data correctness
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json"
        )
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], product_id)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["product_id"], product.product_id)
        self.assertEqual(data["product_name"], "newProduct")
        self.assertAlmostEqual(data["product_price"], 2.2)

    def test_cannot_update_a_product(self):
        """ It should fail to update a non-existent Product """
        # Create a known product
        wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        non_existent_product_id = data["id"] + 1
        data["product_name"] = "newProduct"
        data["product_price"] = 2.2
        # Send the update back
        res = self.client.put(
            f"{BASE_URL}/{wishlist.id}/products/{non_existent_product_id}",
            json=data,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_product(self):
        """ It should remove a Product from a Wishlist """
        wishlist = self._create_wishlists(1)[0]     # create a single wishlist
        product = ProductFactory()
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)     # assert that the product was added successfully
        data = resp.get_json()
        logging.debug(data)
        product_id = data["id"]
        # Remove the just-added product from the wishlist
        resp = self.client.delete(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)     # assert that the product was removed successfully
        # Retrieve it back to make sure it isn't there
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}/products/{product_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  O T H E R   T E S T   C A S E S
    ######################################################################

    def test_unsupported_media_type(self):
        """It should fail to create a Wishlists when incorrect media type is sent"""
        wishlist = WishlistFactory()
        resp = self.client.post(
            BASE_URL, json=wishlist.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_bad_wishlist_data(self):
        """It should fail to create a Wishlist when incorrect data is sent"""
        resp = self.client.post(BASE_URL, json={"wishlist_name": "not my wishlist"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Wishlist with user id of incorrect type
        resp = self.client.post(BASE_URL, json={"user_id": "myID", "wishlist_name": "not my wishlist"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Wishlist with name of incorrect type
        resp = self.client.post(BASE_URL, json={"user_id": 1234, "wishlist_name": 678})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_product_data(self):
        """It should fail to create a Product when incorrect data is sent"""
        wishlist = self._create_wishlists(1)[0]
        product = ProductFactory()
        # Product with negative price
        product.product_price = -123.45
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Product with price of incorrect type
        product.product_price = "Hello, World"
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Product with name of incorrect type
        product.product_price = 123.45
        product.product_name = 123
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Product with id of incorrect type
        product.product_name = "myProduct"
        product.product_id = "XYZ"
        resp = self.client.post(
            f"{BASE_URL}/{wishlist.id}/products",
            json=product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.put(BASE_URL, json={"wishlist_name": "rubbish"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_kubernetes(self):
        """It should be a healthy kubernetes"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")
