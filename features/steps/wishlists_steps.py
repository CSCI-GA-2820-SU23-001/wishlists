#####################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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
######################################################################

"""
Wishlist Steps

Steps file for wishlists.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

@given('the following wishlists')
def step_impl(context):
    """ Delete all Wishlists and load new ones """

    # List all of the wishlists and delete them one by one
    rest_endpoint = f"{context.base_url}/wishlists"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    for wishlist in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{wishlist['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    # Load the database with new wishlists
    for row in context.table:
        payload = {
            "user_id": int(row['user_id']),
            "wishlist_name": row['wishlist_name'],
            "archived": True if row['archived'] == "true" else False
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert(context.resp.status_code == HTTP_201_CREATED)

@given('the following products')
def step_impl(context):
    rest_endpoint = f"{context.base_url}/wishlists"

    for row in context.table:
        resp = requests.get(rest_endpoint + "?name=" + row["wishlist_name"])
        assert(resp.status_code == HTTP_200_OK)

        data = resp.json()
        wishlist_id = data[0]["id"]
        payload = {
            "product_id":int(row['product_id']) ,
            "wishlist_id": wishlist_id,
            "product_name": row['product_name'],
            "product_price": float(row['product_price'])
        }

        resp = requests.post(rest_endpoint + "/" + str(wishlist_id) + "/products", json=payload)
        assert(resp.status_code == HTTP_201_CREATED)
