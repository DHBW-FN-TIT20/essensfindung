function change_url(){
    var zipcode = document.getElementById("restaurant_filter_zipcode").value;
    var costs = get_costs();
    var cuisine = get_cuisine();
    document.getElementById("search_restaurant").href = "/findrestaurant?rest_name="+zipcode+"&costs="+costs+"&cuisine="+cuisine;
}

function get_costs(){
    return document.getElementById('restaurant_filter_costs').value;
}

function get_cuisine(){
    // var thisiscuisine = document.getElementById('restaurant_filter_cuisine').value;
    // return thisiscuisine;
    return 0;
}

function update_modal_on_show() {
    update_radius_text(document.getElementById('restaurant_filter_radius').value);
    update_costs_text(document.getElementById('restaurant_filter_costs').value);
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