$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function wishlist_update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_user_id").val(res.user_id);
        $("#wishlist_name").val(res.wishlist_name);
    }

    /// Clears all form fields
    function wishlist_clear_form_data() {
        $("#wishlist_id").val("");
        $("#wishlist_user_id").val("");
        $("#wishlist_name").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function wishlist_clear_search_result() {
        $("#search_wishlist_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-1">Wishlist ID</th>'
        table += '<th class="col-md-1">User ID</th>'
        table += '<th class="col-md-4">Wishlist Name</th>'
        table += '</tr></thead><tbody>'
        table += '</tbody></table>';
        $("#search_wishlist_results").append(table);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-wishlist-btn").click(function () {
        wishlist_clear_search_result();
        let wishlist_name = $("#wishlist_name").val();
        let user_id = parseInt($("#wishlist_user_id").val());

        let data = {
            "wishlist_name": wishlist_name,
            "user_id": user_id
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            wishlist_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-wishlist-btn").click(function () {
        wishlist_clear_search_result();

        let wishlist_id = $("#wishlist_id").val();
        let wishlist_name = $("#wishlist_name").val();
        let user_id = parseInt($("#wishlist_user_id").val());

        let data = {
            "wishlist_id": wishlist_id,
            "wishlist_name": wishlist_name,
            "user_id": user_id
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlist_id}`,  // Using template literals to insert the wishlist_id into the URL
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            wishlist_update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-wishlist-btn").click(function () {
        wishlist_clear_search_result();
        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            wishlist_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            wishlist_clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-wishlist-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            wishlist_clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-wishlist-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        wishlist_clear_form_data()
    });

    // ****************************************
    // Search for User's Wishlist
    // ****************************************

    $("#search-wishlist-btn").click(function () {

        let wishlist_name = $("#wishlist_name").val();

        let queryString = ""

        if (wishlist_name) {
            queryString += 'wishlist_name=' + wishlist_name
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists?${queryString}`,
            contentType: "application/json",
            data: ''
        })
        //TODO: search result won't clear out
        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_wishlist_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Wishlist ID</th>'
            table += '<th class="col-md-1">User ID</th>'
            table += '<th class="col-md-4">Wishlist Name</th>'
            table += '</tr></thead><tbody>'
            let firstWishlist = "";
            for (let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table += `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.user_id}</td><td>${wishlist.wishlist_name}</td></tr>`;
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }
            table += '</tbody></table>';
            $("#search_wishlist_results").append(table);

            // copy the first result to the form
            if (firstWishlist != "") {
                wishlist_update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            wishlist_clear_search_result()
            flash_message(res.responseJSON.message)
        });

    });

})
