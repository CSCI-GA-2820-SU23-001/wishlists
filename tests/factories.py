# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyDecimal
from service.models import Wishlist, Product


class WishlistFactory(factory.Factory):
    """Creates fake Wishlists"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("random_number")
    wishlist_name = factory.Faker("word")
    # the many side of relationships can be a little wonky in factory boy:
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    @factory.post_generation
    def products(self, create, extracted, **kwargs):   # pylint: disable=method-hidden, unused-argument
        """Creates the products list"""
        if not create:
            return

        if extracted:
            self.wishlist_products = extracted


class ProductFactory(factory.Factory):
    """Creates fake Products"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""
        model = Product

    id = factory.Sequence(lambda n: n)
    wishlist_id = None
    product_id = factory.Faker("random_number")
    product_name = factory.Faker("word")
    product_price = FuzzyDecimal(0, 2000.0, 2)
    wishlist = factory.SubFactory(WishlistFactory)
