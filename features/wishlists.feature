Feature: The wishlist service back-end
    As a a Wishlist Manager
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

    Background:
        Given the following wishlists
            | user_id | wishlist_name | archived |
            | 1       | wishlist_1    | false    |
            | 1       | wishlist_2    | false    |
            | 2       | wishlist_3    | true     |
            | 3       | wishlist_4    | false    |
            | 4       | wishlist_5    | false    |

        Given the following products
            | wishlist_name | product_id | product_name | product_price |
            | wishlist_2    | 1          | product_1    | 100.0         |
            | wishlist_2    | 1          | product_2    | 120.0         |
            | wishlist_3    | 2          | product_3    | 150.0         |
            | wishlist_3    | 2          | product_4    | 170.0         |
            | wishlist_4    | 3          | product_5    | 190.0         |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Wishlists RESTful Service" in the title
        And I should not see "404 Not Found"

    #########################################################
    # B D D   F O R   W I S H L I S T S
    #########################################################

    Scenario: List all Wishlists
        When I visit the "Home Page"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the "wishlist" results
        And I should see "wishlist_2" in the "wishlist" results
        And I should see "wishlist_3" in the "wishlist" results
        And I should see "wishlist_4" in the "wishlist" results
        And I should see "wishlist_5" in the "wishlist" results

    Scenario: Create a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist User ID" to "1234"
        And I set the "Wishlist Name" to "NYE Wishlist"
        And I select "true" from the "Wishlist Archived"
        And I press the "Create_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Wishlist" button
        Then the "Wishlist Id" field should be empty
        And the "Wishlist User ID" field should be empty
        And the "Wishlist Name" field should be empty
        And "False" should be selected in the "Wishlist Archived" field
        When I paste the "Wishlist Id" field
        And I press the "Retrieve_Wishlist" button
        Then I should see the message "Success"
        And I should see "1234" in the "Wishlist User ID" field
        And I should see "NYE Wishlist" in the "Wishlist Name" field
        And "True" should be selected in the "Wishlist Archived" field
        
    Scenario: Read a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_1"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Wishlist" button
        And I paste the "Wishlist Id" field
        And I press the "Retrieve_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the "Wishlist Name" field
        And I should see "1" in the "Wishlist User Id" field
        And "False" should be selected in the "Wishlist Archived" field

    Scenario: Archive a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_1"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I press the "Archive_Wishlist" button
        Then I should see the message "Wishlist has been Archived!"
        And I should see "True" in the "wishlist_archived" option
        When I press the "Unarchive_Wishlist" button
        Then I should see the message "Wishlist has been Unarchived!"
        And I should see "False" in the "wishlist_archived" option

    Scenario: Update a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_1"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the "Wishlist Name" field
        When I change the "Wishlist Name" to "wishlist_first"
        And I press the "Update_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Wishlist" button
        And I paste the "Wishlist Id" field
        And I press the "Retrieve_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_first" in the "Wishlist Name" field
        When I press the "Clear_Wishlist" button
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        Then I should see "wishlist_first" in the "wishlist" results
        And I should not see "wishlist_1" in the "wishlist" results

    Scenario: Delete a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist User ID" to "9876"
        And I set the "Wishlist Name" to "Test Delete"
        And I press the "Create_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Wishlist" button
        Then the "Wishlist Id" field should be empty
        And the "Wishlist User ID" field should be empty
        And the "Wishlist Name" field should be empty
        When I paste the "Wishlist Id" field
        And I press the "Delete_Wishlist" button
        Then I should see the message "Wishlist has been Deleted!"

    Scenario: Filter Wishlists by Name
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_1"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the "wishlist" results
        And I should not see "wishlist_2" in the "wishlist" results
        And I should not see "wishlist_3" in the "wishlist" results
        And I should not see "wishlist_4" in the "wishlist" results
        And I should not see "wishlist_5" in the "wishlist" results

    #########################################################
    # B D D   F O R   P R O D U C T S
    #########################################################

    Scenario: List products in a wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        And I set the "Product ID" to "7"
        And I set the "Product Name" to "product_23"
        And I set the "Product Price" to "120.0"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id Product Mapping" field
        And I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I press the "Search_Product" button
        Then I should see the message "Success"
        Then I should see "product_23" in the "product" results
        And I should not see "product_3" in the "product" results
        And I should not see "product_4" in the "product" results
        And I should not see "product_5" in the "product" results

    Scenario: Create a Product in a Wishlist
        When I visit the "Home Page"
        When I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        And I set the "Product ID" to "6"
        And I set the "Product Name" to "product_6"
        And I set the "Product Price" to "220.0"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I press the "Search_Product" button
        Then I should see "product_6" in the "product" results

    Scenario: Update a product under a wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        And I set the "Product ID" to "7"
        And I set the "Product Name" to "product_23"
        And I set the "Product Price" to "120.0"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I press the "Search_Product" button
        Then I should see the message "Success"
        And I should see "product_23" in the "product" results
        When I set the "Product ID" to "9"
        And I set the "Product Name" to "product_55_updated"
        And I set the "Product Price" to "25.0"
        And I press the "Update_Product" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id Product Mapping" field
        And I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I press the "Search_Product" button
        Then I should see the message "Success"
        Then I should see "product_55_updated" in the "product" results
        And I should not see "product_23" in the "product" results

    Scenario: Delete a product under a wishlist
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        When I set the "Product Name" to "delete_prod"
        When I set the "Product ID" to "9"
        And I set the "Product Price" to "25.0"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I copy the "Product Model ID" field
        And I press the "Delete_Product" button
        Then I should see the message "Product has been Deleted!"
        When I paste the "Product Model ID" field
        And I press the "Wishlist_Page" button of form
        And I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        And I press the "Retrieve_Product" button
        Then I should see the message "404 Not Found"
        And I should not see "Success"

    Scenario: Filter items by product id
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_2"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Items_Page" button of form
        And I paste the "Wishlist Id Product Mapping" field
        When I set the "Product Name" to "product_to_be_shown"
        When I set the "Product ID" to "9"
        And I set the "Product Price" to "25.0"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I set the "Product ID" to "10"
        And I set the "Product Name" to "product_not_to_be_shown"
        And I set the "Product Price" to "33.45"
        And I press the "Create_Product" button
        Then I should see the message "Success"
        When I press the "Clear_Product" button
        And I paste the "Wishlist Id Product Mapping" field
        And I set the "Product Id" to "9"
        And I press the "Search_Product" button
        Then I should see "product_to_be_shown" in the "product" results
        And I should not see "product_not_to_be_shown" in the "product" results
