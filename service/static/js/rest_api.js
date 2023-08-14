$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function wishlist_update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_user_id").val(res.user_id);
        $("#wishlist_name").val(res.wishlist_name);
        $('#wishlist_archived').val(String(res.archived));
        $("#product_list_result").empty();
        product_list_rowIdx = 0;
        var products = res.wishlist_products;

        for(let i = 0; i < products.length; i++) {
            append_existed_product_list(products[i].product_id, products[i].product_name, products[i].product_price);
        }
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
        $('#wishlist_archived').val("false");
        $("#product_list_result").empty();
        wishlist_clear_search_result();
    }

    function product_clear_form_data() {
        $("#product_model_id").val("");
        $("#product_id").val("");
        $("#product_name").val("");
        $("#wishlist_id_product_mapping").val("");
        $("#product_price").val("");
        product_clear_search_result();
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
        table += '<th class="col-md-2">Wishlist Name</th>'
        table += '<th class="col-md-4">Items</th>'
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

    var product_list_rowIdx = 0;

    function append_existed_product_list(product_id, product_name, product_price) {
        $("#product_list_result").append(
        `<tr id="product_list_row_${++product_list_rowIdx}">
            <td> <input type="number" name="text" class="form-control" value=${product_id} readonly=true></td>
            <td> <input type="text" name="text" class="form-control" value=${product_name} readonly=true></td>
            <td> <input type="number" name="text" class="form-control" value=${product_price} readonly=true></td>
            <td> <button type="submit" class="btn btn-danger remove">Remove</button></td>
        </tr>`);
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
        let archived = document.querySelector("#wishlist_archived").value == "true" ? true : false;

        let product_list = [];
        let product_list_result = document.getElementById("product_list_result");
        for(let i = 0, row; row = product_list_result.rows[i]; i++) {
            let product = {
                "wishlist_id": "null",
                "product_id": parseInt(row.cells[0].children[0].value),
                "product_name": row.cells[1].children[0].value,
                "product_price": parseFloat(row.cells[2].children[0].value)
            };
            product_list.push(product);
        }

        let data = {
            "wishlist_name": wishlist_name,
            "user_id": user_id,
            "archived": archived,
            "wishlist_products": product_list
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

    $("#update_wishlist_btn").click(function () {
        wishlist_clear_search_result();

        let wishlist_id = $("#wishlist_id").val();
        let wishlist_name = $("#wishlist_name").val();
        let user_id = parseInt($("#wishlist_user_id").val());
        let archived = document.querySelector("#wishlist_archived").value == "true" ? true : false;
        
        let product_list = [];
        let product_list_result = document.getElementById("product_list_result");
        for(let i = 0, row; row = product_list_result.rows[i]; i++) {
            if(row.cells[1].children[0].getAttribute('readonly')) {
                continue;
            }
            let product = {
                    "wishlist_id": wishlist_id,
                    "product_id": parseInt(row.cells[0].children[0].value),
                    "product_name": row.cells[1].children[0].value,
                    "product_price": parseFloat(row.cells[2].children[0].value)
                };
            product_list.push(product);
        }

        let data = {
            "wishlist_id": wishlist_id,
            "wishlist_name": wishlist_name,
            "user_id": user_id,
            "archived": archived,
            "wishlist_products": product_list
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

    // ****************************************
    // Archive a Wishlist
    // ****************************************

    $("#archive_wishlist_btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlist_id}/archive`
        })
        
        ajax.done(function (res){
            wishlist_update_form_data(res)
            flash_message("Wishlist has been Archived!")
        });

        ajax.fail(function (res){
            wishlist_clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });
    
    // ****************************************
    // Unarchive a Wishlist
    // ****************************************

    $("#unarchive_wishlist_btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlist_id}/unarchive`
        })
        
        ajax.done(function (res){
            wishlist_update_form_data(res)
            flash_message("Wishlist has been Unarchived!")
        });

        ajax.fail(function (res){
            wishlist_clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });

    // ************************************************************************************
    // PRODUCTS
    // ************************************************************************************
    
    // ****************************************
    // Create a Product
    // ****************************************

    $("#create_product_btn").click(function () {
        product_clear_search_result();
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
        product_clear_search_result();
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_model_id = $("#product_model_id").val();
        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }

        if (product_model_id == "") {
            flash_message("Error: Product Model ID must not be empty")
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
        flash_message(`/wishlists/${wishlist_id}/products/${product_model_id}`)
        ajax.fail(function(res){
            product_clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete_product_btn").click(function () {
        let wishlist_id = $("#wishlist_id_product_mapping").val();
        let product_model_id = $("#product_model_id").val();

        if (wishlist_id == "") {
            flash_message("Error: Wishlist ID must not be empty")
            return
        }

        if (product_model_id == "") {
            flash_message("Error: Product Model ID must not be empty")
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
            $("#product_model_id").val("");
            flash_message("Product has been Deleted!")
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

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#wishlist_search_results").empty();

            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Wishlist ID</th>'
            table += '<th class="col-md-1">User ID</th>'
            table += '<th class="col-md-2">Wishlist Name</th>'
            table += '<th class="col-md-4">Items</th>'
            table += '</tr></thead><tbody>'
            let firstWishlist = "";
            for (let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table += `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.user_id}</td><td>${wishlist.wishlist_name}</td>`
                table += `<td><table>`

                let wishlist_products = wishlist.wishlist_products
                if(wishlist_products.length == 0) {
                    table += `<tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr>`
                }
                for(let j = 0; j < wishlist_products.length; j++) {
                    let product = wishlist_products[j]
                    table += `<tr>
                                <td><b>Item ID:</b> ${product.id}&emsp;</td>
                                <td><b>Product ID:</b> ${product.product_id}&emsp;</td>
                                <td><b>Product Name:</b> ${product.product_name}&emsp;</td>
                                <td><b>Product Price:</b> ${product.product_price}&emsp;</td>
                             </tr>`;
                }
                
                table += `</table></td></tr>`
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

    });

    $("#append_product_list_btn").click(function () {
        $("#product_list_result").append(
        `<tr id="product_list_row_${++product_list_rowIdx}">
            <td> <input type="number" name="text" class="form-control"  placeholder="Product ID"></td>
            <td> <input type="text" name="text" class="form-control"  placeholder="Product Name"></td>
            <td> <input type="number" name="text" class="form-control"  placeholder="Product Price"></td>
            <td> <button type="submit" class="btn btn-danger remove">Remove</button></td>
        </tr>`);
    });

    $('#product_list_result').on('click', '.remove', function () {
        var child = $(this).closest('tr').nextAll();
    
        // Iterating across all the rows 
        // obtained to change the index
        child.each(function () {
            
            // Getting <tr> id.
            var id = $(this).attr('id');
    
            // Gets the row number from <tr> id.
            var dig = parseInt(id.substring(1));
    
            // Modifying row id.
            $(this).attr('id', `product_list_row_${dig - 1}`);
        });
    
        // Removing the current row.
        $(this).closest('tr').remove();
    
        // Decreasing the total number of rows by 1.
        product_list_rowIdx--;
    });
});
