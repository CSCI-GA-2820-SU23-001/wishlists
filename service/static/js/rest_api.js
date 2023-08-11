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

    function product_update_form_data(res) {
        $("#product_model_id").val(res.id);
        $("#product_id").val(res.product_id);
        $("#product_name").val(res.product_name);
        $("#wishlist_id_product_mapping").val(res.wishlist_id);
        $("#product_price").val(res.product_price);
    }

    /// Clears all form fields
    function wishlist_clear_form_data() {
        $("#wishlist_id").val("");
        $("#wishlist_user_id").val("");
        $("#wishlist_name").val("");
        wishlist_clear_search_result();
    }

    function product_clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#wishlist_id_product_mapping").val("");
        $("#product_price").val("");    
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function wishlist_clear_search_result() {
        $("#wishlist_search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-1">Wishlist ID</th>'
        table += '<th class="col-md-1">User ID</th>'
        table += '<th class="col-md-4">Wishlist Name</th>'
        table += '</tr></thead><tbody>'
        table += '</tbody></table>';
        $("#wishlist_search_results").append(table);
    }

    function product_clear_search_result() {
        $("#product_search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-1">Product Model ID</th>'
        table += '<th class="col-md-1">Wishlist ID</th>'
        table += '<th class="col-md-1">Product ID</th>'
        table += '<th class="col-md-4">Product Name</th>'
        table += '<th class="col-md-2">Product Price</th>'
        table += '</tr></thead><tbody>'
        table += '</tbody></table>';
        $("#product_search_results").append(table);
    }

    // ************************************************************************************
    // WISHLIST
    // ************************************************************************************
    
    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create_wishlist_btn").click(function () {
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

        ajax.done(function (res){
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

    $("#update-wishlist_btn").click(function () {
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

    $("#retrieve_wishlist_btn").click(function () {
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

        ajax.fail(function (res){
            wishlist_clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete_wishlist_btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })
        
        ajax.done(function (res){

            wishlist_clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });
    
    // ************************************************************************************
    // PRODUCTS
    // ************************************************************************************
    
    // ****************************************
    // Create a Product
    // ****************************************

    $("#create_product_btn").click(function () {
        clear_search_result();
        let product_id = parseInt($("#product_id").val());
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_name = $("#product_name").val();
        let product_price = parseInt($("#product_price").val());
        
        let data = {
            "product_id": product_id,
            "wishlist_id": wishlist_id,
            "product_name": product_name,
            "product_price": product_price
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/wishlists/${wishlist_id}/products`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            product_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // TODO: update a Product
    // ****************************************

    $("#update_product_btn").click(function () {
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_name = $("#product_name").val();
        let product_model_id = parseInt($("#product_model_id").val());
        let product_id = parseInt($("#product_id").val());
        let product_price = parseInt($("#product_price").val());

        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }
        if (product_name == "") {
            flash_message("Error: Product Name must not be empty")
            return
        }
        if (product_id == "") {
            flash_message("Error: Product ID must not be empty")
            return
        }
        if (product_price == "") {
            flash_message("Error: Product Price must not be empty")
            return
        }
        let data = {
            "id": product_model_id,
            "wishlist_id": wishlist_id,
            "product_name": product_name,
            "product_id": product_id,
            "product_price": product_price
        };


        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/wishlists/${wishlist_id}/products/${product_model_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            product_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve_product_btn").click(function () {
        clear_search_result();
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_model_id = $("#product_model_id").val();
        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/products/${product_model_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            product_update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            product_clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete_product_btn").click(function () {
        let wishlist_id = $("#wishlist_product_mapping_id").val();
        let product_model_id = $("#product_model_id").val();

        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}/products/${product_model_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            product_clear_form_data(res)
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear_wishlist_btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        wishlist_clear_form_data()
    });

    $("#clear_product_btn").click(function () {
        $("#product_model_id").val("");
        $("#flash_message").empty();
        product_clear_form_data()
    });

    // ****************************************
    // Search for User's Wishlist
    // ****************************************

    $("#search_wishlist_btn").click(function () {

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
            $("#wishlist_search_results").empty();

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

            $("#wishlist_search_results").append(table);


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

    $("#search_product_btn").click(function () {
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_name = $("#product_name").val();
        let product_id = $("#product_id").val();
        let product_price = $("#product_price").val();

        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }
        
        let queryString = ""

        if (product_name) {
            queryString += 'product_name=' + name
        }
        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + product_id
            } else {
                queryString += 'product_id=' + product_id
            }
        }
        if (product_price) {
            if (queryString.length > 0) {
                queryString += '&product_price=' + product_price
            } else {
                queryString += ' product_price=' + product_price
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/products?${queryString}`,
            contentType: "application/json",
            data: ''
        })
        //TODO: search result won't clear out
        ajax.done(function(res){
            //alert(res.toSource())
            $("#product_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Product Model ID</th>'
            table += '<th class="col-md-1">Wishlist ID</th>'
            table += '<th class="col-md-1">Product ID</th>'
            table += '<th class="col-md-4">Product Name</th>'
            table += '<th class="col-md-2">Product Price</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let prod = res[i];
                table +=  `<tr id="row_${i}"><td>${prod.id}</td><td>${prod.wishlist_id}</td><td>${prod.product_id}</td><td>${prod.product_name}</td><td>${prod.product_price}</td></tr>`;
                if (i == 0) {
                    firstProduct = prod;
                }
            }
            table += '</tbody></table>';
            $("#product_search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                product_update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            product_clear_search_result()
            flash_message(res.responseJSON.message)
        });

    })
})
