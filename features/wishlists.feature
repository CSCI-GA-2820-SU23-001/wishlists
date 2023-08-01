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