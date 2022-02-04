/************ Initialize Multiselects ***************** */
$(document).ready(function() {
    $('.restaurant_filter_multiselects').select2({
        dropdownParent: $('#restaurantFilter'),
        width: "250"
    });
});

/******** inititialize star-rating-svg *****************/
$("#restaurant_filter_rating").rating({ min: 1, max: 10, step: 2, size: 'lg' });

function change_url() {
    var latitude = get_latitude();
    var longitude = get_longitude();
    var zipcode = get_zipcode();
    var costs = get_costs();
    var cuisine = get_cuisine();
    var allergies = get_allergies();
    var rating = get_rating();
    var radius = get_radius();
    if (allergies.length > 0) {
        document.getElementById("search_restaurant").href = "/findrestaurant?cuisine=" + cuisine + "&allergies=" + allergies + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else {
        document.getElementById("search_restaurant").href = "/findrestaurant?cuisine=" + cuisine + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    }
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
    return 3;
}

function get_radius() {
    return document.getElementById('restaurant_filter_radius').value;
}

function get_cuisine() {
    var selections = $('#restaurant_filter_cuisine').select2('data');
    var cuisines = [];
    for (const element of selections) {
        console.log(element.id);
        cuisines.push(element.id);
    }
    return cuisines;
}

function get_allergies() {
    var selections = $('#restaurant_filter_allergies').select2('data');
    var allergies = [];
    for (const element of selections) {
        console.log(element.id);
        allergies.push(element.id);
    }
    return allergies;
}

function update_modal_on_show() {
    update_radius_text(document.getElementById('restaurant_filter_radius').value);
    update_costs_text(document.getElementById('restaurant_filter_costs').value);
    update_cuisine_selected();
}

function update_cuisine_selected() {
    var cuisine = document.getElementById('cuisine').innerHTML;
    $('#restaurant_filter_cuisine').val(cuisine);
    $('#restaurant_filter_cuisine').trigger('change');
}

function update_radius_text(val) {
    document.getElementById('restaurant_filter_radius_text').value = (val | 0) + " km";
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