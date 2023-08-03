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
    And I set the "User ID" to "1234"
    And I set the "Name" to "NYE Wishlist"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "User ID" field should be empty
    And the "Name" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "1234" in the "User ID" field
    And I should see "NYE Wishlist" in the "Name" field