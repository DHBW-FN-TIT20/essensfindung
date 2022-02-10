/************ Initialize Multiselects ***************** */
$(document).ready(function() {
    $('.restaurant_filter_multiselects').select2({
        dropdownParent: $('#restaurantFilter'),
        width: "250"
    });
});

/******** inititialize star-rating-svg *****************/
$("#restaurant_filter_rating").raty({
    starOff: 'https://cdn.jsdelivr.net/npm/raty-js@3.1.1/lib/images/star-off.png',
    starOn: 'https://cdn.jsdelivr.net/npm/raty-js@3.1.1/lib/images/star-on.png',
    click: function(score, evt) {
        document.getElementById('restaurant_filter_rating_target').innerHTML = score;
    },
    score: function() {
        return document.getElementById('restaurant_filter_rating_selected').innerHTML;
    }
});

/*********** On modal close ****************************/
$('#restaurantFilter').on('hide.bs.modal', function(e) {
    document.getElementById("cuisine_selected").innerHTML = get_cuisine();
    document.getElementById("allergies_selected").innerHTML = get_allergies();
})

function change_url() {
    var latitude = get_latitude();
    var longitude = get_longitude();
    var zipcode = get_zipcode();
    var costs = get_costs();
    var cuisine = get_cuisine();
    var allergies = get_allergies();
    var rating = get_rating();
    var radius = get_radius();
    if (cuisine.length > 0 && allergies.length > 0) {
        document.getElementById("search_restaurant").href = "/findrestaurant?cuisine=" + cuisine + "&allergies=" + allergies + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else if (cuisine.length > 0) {
        document.getElementById("search_restaurant").href = "/findrestaurant?cuisine=" + cuisine + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else if (allergies.length > 0) {
        document.getElementById("search_restaurant").href = "/findrestaurant?allergies=" + allergies + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else {
        document.getElementById("search_restaurant").href = "/findrestaurant?rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    }
}

function reload_page() {
    window.location.reload(true);
}

function get_latitude() {
    return document.getElementById("restaurant_filter_latitude").innerHTML;
}

function get_longitude() {
    return document.getElementById("restaurant_filter_longitude").innerHTML;
}

function get_zipcode() {
    return document.getElementById("restaurant_filter_zipcode").value;
}

function get_costs() {
    return document.getElementById('restaurant_filter_costs').value;
}

function get_rating() {
    var rating = document.getElementById('restaurant_filter_rating_target').innerHTML;
    if (rating) {
        return rating;
    } else {
        return document.getElementById('restaurant_filter_rating_selected').innerHTML;
    }
}

function get_radius() {
    return document.getElementById('restaurant_filter_radius').value;
}

function get_cuisine() {
    var selections = $('#restaurant_filter_cuisine').select2('data');
    var cuisines = [];
    for (const element of selections) {
        cuisines.push(element.id);
    }
    // if (cuisines.length > 0) {
    return cuisines;
    // } else {
    //     update_cuisine_selected();
    //     selections = $('#restaurant_filter_cuisine').select2('data');
    //     for (const element of selections) {
    //         cuisines.push(element.id);
    //     }
    //     return cuisines;
    // }

}

function get_allergies() {
    var selections = $('#restaurant_filter_allergies').select2('data');
    var allergies = [];
    for (const element of selections) {
        allergies.push(element.id);
    }
    // if (allergies > 0) {
    return allergies;
    // } else {
    //     update_allergies_selected();
    //     selections = $('#restaurant_filter_allergies').select2('data');
    //     for (const element of selections) {
    //         allergies.push(element.id);
    //     }
    //     return allergies;
    // }
}

function update_allergies_selected() {
    var allergies_str = document.getElementById('allergies_selected').innerHTML;
    $('#restaurant_filter_allergies').val(strToArray(allergies_str));
    $('#restaurant_filter_allergies').trigger('change');
    // $('#restaurant_filter_allergies').on('change', function);
}

function update_allergies_options() {
    var allergie_options = strToArray(document.getElementById('allergies_options').innerHTML);
    for (const allergie of allergie_options) {
        if ($('#restaurant_filter_allergies').find("option[value='" + allergie + "']").length) {
            $('#restaurant_filter_allergies').val(allergie).trigger('change');
        } else {
            var new_option = new Option(allergie, allergie, false, false);
            $('#restaurant_filter_allergies').append(new_option).trigger('change');
        }
    }
}

function update_modal_on_show() {
    update_radius_text(document.getElementById('restaurant_filter_radius').value);
    update_costs_text(document.getElementById('restaurant_filter_costs').value);
    update_cuisine_options();
    update_allergies_options();
    update_cuisine_selected();
    update_allergies_selected();
}

function update_cuisine_selected() {
    var cuisine_str = document.getElementById('cuisine_selected').innerHTML;
    $('#restaurant_filter_cuisine').val(strToArray(cuisine_str));
    $('#restaurant_filter_cuisine').trigger('change');
}

function update_cuisine_options() {
    var cuisines_options = strToArray(document.getElementById('cuisine_options').innerHTML);
    for (const cuisine of cuisines_options) {
        if (cuisine != "Essen") {
            if ($('#restaurant_filter_cuisine').find("option[value='" + cuisine + "']").length) {
                $('#restaurant_filter_cuisine').val(cuisine).trigger('change');
            } else {
                var new_option = new Option(cuisine, cuisine, false, false);
                $('#restaurant_filter_cuisine').append(new_option).trigger('change');
            }
        }
    }
}

function update_radius_text(val) {
    document.getElementById('restaurant_filter_radius_text').value = val + " km";
}

function update_costs_text(val) {
    if (val == 0) {
        document.getElementById('restaurant_filter_costs_text').value = "Kostenlos";
    } else if (val == 1) {
        document.getElementById('restaurant_filter_costs_text').value = "Preiswert";
    } else if (val == 2) {
        document.getElementById('restaurant_filter_costs_text').value = "Mittelmäßig";
    } else if (val == 3) {
        document.getElementById('restaurant_filter_costs_text').value = "Teuer";
    } else {
        document.getElementById('restaurant_filter_costs_text').value = "Sehr Teuer";
    }
}

function strToArray(commaSeperatedString) {
    return commaSeperatedString.split(',');
}