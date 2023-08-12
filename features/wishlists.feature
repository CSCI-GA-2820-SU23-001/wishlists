Feature: The wishlist service back-end
    As a a Wishlist Manager
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

    Background:
        Given the following wishlists
            | user_id | wishlist_name |
            | 1       | wishlist_1    |
            | 1       | wishlist_2    |
            | 2       | wishlist_3    |
            | 3       | wishlist_4    |
            | 4       | wishlist_5    |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Wishlists RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Create a Wishlist
        When I visit the "Home Page"
        And I set the "Wishlist User ID" to "1234"
        And I set the "Wishlist Name" to "NYE Wishlist"
        And I press the "Create_Wishlist" button
        Then I should see the message "Success"
        When I copy the "Wishlist Id" field
        And I press the "Clear_Wishlist" button
        Then the "Wishlist Id" field should be empty
        And the "Wishlist User ID" field should be empty
        And the "Wishlist Name" field should be empty
        When I paste the "Wishlist Id" field
        And I press the "Retrieve_Wishlist" button
        Then I should see the message "Success"
        And I should see "1234" in the "Wishlist User ID" field
        And I should see "NYE Wishlist" in the "Wishlist Name" field

    Scenario: Get a Wishlist by Name
        When I visit the "Home Page"
        And I set the "Wishlist Name" to "wishlist_1"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the wishlist results
        And I should not see "wishlist_2" in the wishlist results
        And I should not see "wishlist_3" in the wishlist results
        And I should not see "wishlist_4" in the wishlist results
        And I should not see "wishlist_5" in the wishlist results

    Scenario: List all Wishlists
        When I visit the "Home Page"
        And I press the "Search_Wishlist" button
        Then I should see the message "Success"
        And I should see "wishlist_1" in the wishlist results
        And I should see "wishlist_2" in the wishlist results
        And I should see "wishlist_3" in the wishlist results
        And I should see "wishlist_4" in the wishlist results
        And I should see "wishlist_5" in the wishlist results

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
        And I should see "wishlist_first" in the wishlist results
        And I should not see "wishlist_1" in the wishlist results