function change_url(){
    var zipcode = document.getElementById("restaurant_filter_zipcode").value;
    var costs = get_costs();
    document.getElementById("search_restaurant").href = "/findrestaurant?rest_name="+zipcode+"&costs="+costs;
}

function get_costs(){
    return 0;
}