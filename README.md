# NYU DevOps Project Template

[![Build Status](https://github.com/CSCI-GA-2820-SU23-001/wishlists/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU23-001/wishlists/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SU23-001/wishlists/branch/master/graph/badge.svg?token=0d12e1c4-7425-4ad5-a59a-208223890746)](https://codecov.io/gh/CSCI-GA-2820-SU23-001/wishlists)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```
## Wishlist APIs 

| Operation | Method | Endpoints |
| -------- | -------- | -------- |
|  create_a_wishlist  |  POST  | ```/wishlists``` |
| update_a_wishlist    | PUT   | ```/wishlists/<int:wishlist_id> ```  |
| list_all_wishlists    | GET   |  ```/wishlists```     |
| get_wishlists   | GET | ```/wishlists/<int:wishlist_id>``` |
| delete_wishlist   | DELETE  | ```/wishlists/<int:wishlist_id>```  |

## Product APIs 

| Operation | Method | Endpoints |
| -------- | -------- | -------- |
|  create_a_product  |  POST  | ```/wishlists/<int:wishlist_id>/products``` |
| update_product   | PUT   | ```/wishlists/<int:wishlist_id> ```  |
| list_products | GET | ```/wishlists/<int:wishlist_id>/products```|
| get_products  | GET | ```/wishlists/<int:wishlist_id>/products/<int:product_id>``` |
| remove_product  | DELETE  | ```/wishlists/<int:wishlist_id>/products/<int:product_id>```  |


## API usage documentation 

### Create a Wishlist  

**URL:** `http://127.0.0.1:8000/wishlists`

**Method:** `POST`

This API creates a wishlist when a JSON body comprising of an id, user id, name for the wishlist and the products associated with that wishlist is passed. 

Example:

Request Body (JSON)

```
{
"id" : 1,
"user_id" : 3,
"wishlist_name" : "Name",
"wishlist_products" : []

}

```
Response : ``` HTTP_201_CREATED ```

```
{
"id" : 1,
"user_id" : 3,
"wishlist_name" : "Name",
"wishlist_products" : []

}

```

### Update a wishlist  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}`

**Method:** `PUT`

This API updates a wishlist whose wishlist_list id is passed to the fields passed as a JSON body accordingly

Example:

``` http://127.0.0.1:8000/wishlists/1 ```

Request Body (JSON)

```
{
  "user_id" : 1,
"wishlist_name" : "wishlist-id1",
"wishlist_products" : []
}


```
Response : ``` HTTP_200_OK```

```
{
  "id": 1,
  "user_id": 1,
  "wishlist_name": "wishlist-id1",
  "wishlist_products": []
}

```

### List all wishlists  

**URL:** `http://127.0.0.1:8000/wishlists`

**Method:** `GET`

This API lists all the wishlists present in the database.

Example:

Response : ``` HTTP_200_OK ```

```
[
  {
    "id": 2,
    "user_id": 3,
    "wishlist_name": "wishlist",
    "wishlist_products": []
  },
  {
    "id": 1,
    "user_id": 1,
    "wishlist_name": "wishlist-id1",
    "wishlist_products": []
  }
]
```

### Get a wishlist  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}`

**Method:** `GET`


This API retrieves a wishlist whose id is passed 

Example:

API :   ``` http://127.0.0.1:8000/wishlists/1 ```

Response : ``` HTTP_200_OK ```

```
{
  "id": 1,
  "user_id": 1,
  "wishlist_name": "wishlist-id1",
  "wishlist_products": []
}
```

### Delete a wishlist  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}`

**Method:** `DELETE`

This API deletes a wishlist whose wishlist id is passed

Example: http://127.0.0.1:8000/wishlists/1

Response : ``` 204 NO_CONTENT ```


### Create a Product  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}/products`

**Method:** `POST`

This API creates a product when a JSON body comprising of an id, product_id, wishlist_id, product_name and product_price associated with that wishlist is passed. 

Example:

API :   ``` http://127.0.0.1:8000/wishlists/51/products ```

Request Body (JSON)

```
{
"id" : 1,
"wishlist_id" : 51,
"product_id" : "1",
"product_name" : "Product 1",
"product_price" : 250

}
```
Response : ``` HTTP_201_CREATED ```

```
{
  "id": 17,
  "product_id": 1,
  "product_name": "Product 1",
  "product_price": 250.0,
  "wishlist_id": 51
}

```

### Update a product  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}/products/{int:product_id}`

**Method:** `PUT`

This API updates a product in the wishlist of wishlist_id passed with the passed data accordingly.

Example:

``` http://127.0.0.1:8000/wishlists/51/products/17 ```

Request Body (JSON)

```
{
  "id": 17,
  "wishlist_id" : 51,
  "product_id" : 1,
  "product_name": "New Product name",
  "product_price": 300
}
```
Response : ``` HTTP_200_OK```

```
{
  "id": 17,
  "product_id": 1,
  "product_name": "New Product name",
  "product_price": 300.0,
  "wishlist_id": 51
}
```
### List all products  

**URL:** `http://127.0.0.1:8000/wishlists/51/products`

**Method:** `GET`

This API lists all the products present in the wishlist of id wishlist_id that is passed.

Example:

Response : ``` HTTP_200_OK ```

```
[
  {
    "id": 16,
    "product_id": 719,
    "product_name": "newProduct",
    "product_price": 2.2,
    "wishlist_id": 51
  },
  {
    "id": 17,
    "product_id": 1,
    "product_name": "New Product name",
    "product_price": 300.0,
    "wishlist_id": 51
  }
]
```

### Get a product  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}/products/{int:product_id}`

**Method:** `GET`

This API retrieves a product whose id is passed from the wishlist of id wishlist_id that is passed.

Example:

API :   ``` http://127.0.0.1:8000/wishlists/51/products/17```

Response : ``` HTTP_200_OK ```

```
{
  "id": 17,
  "product_id": 1,
  "product_name": "New Product name",
  "product_price": 300.0,
  "wishlist_id": 51
}
```

### Delete a product  

**URL:** `http://127.0.0.1:8000/wishlists/{int:wishlist_id}/products/{int:product_id}`

**Method:** `DELETE`

This API deletes a product from a wishlist whose wishlist id and product id are passed

Example: http://127.0.0.1:8000/wishlists/1/products/17

Response : ``` 204 NO_CONTENT ```


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
