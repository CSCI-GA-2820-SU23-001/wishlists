$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#user_id").val(res.user_id);
        $("#wishlist_name").val(res.wishlist_name);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_id").val("");
        $("#user_id").val("");
        $("#wishlist_name").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function clear_search_result() {
        $("#search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-1">Wishlist ID</th>'
        table += '<th class="col-md-1">User ID</th>'
        table += '<th class="col-md-4">Wishlist Name</th>'
        table += '</tr></thead><tbody>'
        table += '</tbody></table>';
        $("#search_results").append(table);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {
        clear_search_result();
        let wishlist_name = $("#wishlist_name").val();
        let user_id = parseInt($("#user_id").val());
        
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

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // TODO: update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        let pet_id = $("#pet_id").val();
        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";
        let gender = $("#pet_gender").val();
        let birthday = $("#pet_birthday").val();

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "gender": gender,
            "birthday": birthday
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/pets/${pet_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {
        clear_search_result();
        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for User's Wishlist
    // ****************************************

    $("#search-btn").click(function () {

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
        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Wishlist ID</th>'
            table += '<th class="col-md-1">User ID</th>'
            table += '<th class="col-md-4">Wishlist Name</th>'
            table += '</tr></thead><tbody>'
            let firstWishlist = "";
            for(let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table +=  `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.user_id}</td><td>${wishlist.wishlist_name}</td></tr>`;
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstWishlist != "") {
                update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_search_result()
            flash_message(res.responseJSON.message)
        });

    });

})
