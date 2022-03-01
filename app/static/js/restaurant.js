/************ Initialize Multiselects ***************** */
$(document).ready(function() {
    get_location();
    update_restaurant_modal_on_show();
});

/************ checkbox selection code ***************** */
function updateCuisineCheckboxes() {
    if (document.getElementById("allCuisineCheckbox").checked) {
        document.getElementById("cuisineCheckboxesContainer").classList.add("d-none"); 
    } else {
        document.getElementById("cuisineCheckboxesContainer").classList.remove("d-none"); 
    }
}
function updateAllergyCheckboxes() {
    if (document.getElementById("allAllergyCheckbox").checked) {
        document.getElementById("allergyCheckboxesContainer").classList.add("d-none"); 
    } else {
        document.getElementById("allergyCheckboxesContainer").classList.remove("d-none"); 
    }
}

/******** inititialize star-rating-svg *****************/
$("#restaurant_filter_rating").raty({
    starOff: '/static/img/icons8-star-32.png',
    starOn: '/static/img/icons8-star-32-filled.png',
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

function change_restaurant_url() {
    var latitude = get_latitude();
    var longitude = get_longitude();
    var zipcode = get_zipcode();
    var costs = get_costs();
    var cuisine = get_cuisine();
    var allergies = get_allergies();
    var rating = get_rating();
    var radius = get_radius();
    if (cuisine.length > 0 && allergies.length > 0) {
        var new_link = "/findrestaurant?cuisine=" + cuisine + "&allergies=" + allergies + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else if (cuisine.length > 0) {
        var new_link = "/findrestaurant?cuisine=" + cuisine + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else if (allergies.length > 0) {
        var new_link = "/findrestaurant?allergies=" + allergies + "&rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    } else {
        var new_link = "/findrestaurant?rating=" + rating + "&costs=" + costs + "&radius=" + radius + "&lat=" + latitude + "&lng=" + longitude;
    }
    document.getElementById("search_restaurant").href = new_link;
    document.getElementById("search_restaurant_from_modal").href = new_link;
}

function search_from_modal() {
    change_restaurant_url();
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
    let cuisines = [];
    if (!document.getElementById("allCuisineCheckbox").checked) {
        document.querySelectorAll("#cuisineCheckboxesContainer div.form-check input[type=checkbox]").forEach(e => {
            if (e.checked) {
                cuisines.push(e.nextSibling.nextSibling.innerText);         
            }
        });
    }
    return cuisines;
}

function get_allergies() {
    let allergies = [];
    if (!document.getElementById("allAllergyCheckbox").checked) {
        document.querySelectorAll("#allergyCheckboxesContainer div.form-check input[type=checkbox]").forEach(e => {
            if (e.checked) {
                allergies.push(e.nextSibling.nextSibling.innerText);         
            }
        });
    }
    return allergies;
}

function update_allergies_selected() {
    let allergies_arr = document.getElementById('allergies_selected').innerHTML.split(",");
    if (allergies_arr.length > 0) {
        for (i = 0; i < allergies_arr.length; i++) {
            let checkbox = document.getElementsByName("allergyCheckbox" + allergies_arr[i])
            if (checkbox.length > 0) {
                if (!checkbox[0].checked) {
                    checkbox[0].checked = true;
                }
            }
        }
        document.getElementById("allAllergyCheckbox").checked = false;
        updateAllergyCheckboxes();
    }
}

function update_restaurant_modal_on_show() {
    update_radius_text(document.getElementById('restaurant_filter_radius').value);
    update_costs_text(document.getElementById('restaurant_filter_costs').value);
}

function update_cuisine_selected() {
    let cuisine_arr = document.getElementById('cuisine_selected').innerText.split(",");
    if (cuisine_arr.length > 0) {
        for (i = 0; i < cuisine_arr.length; i++) {
            let checkbox = document.getElementsByName("cuisineCheckbox" + cuisine_arr[i])
            if (checkbox.length > 0) {
                if (!checkbox[0].checked) {
                    checkbox[0].checked = true;
                }
            }
        }
        document.getElementById("allCuisineCheckbox").checked = false;
        updateCuisineCheckboxes();
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