function change_recipe_url() {
    var length_int = get_length()
    if (length_int == 0) {
        var length = 900;
    } else if (length_int == 1) {
        var length = 1800;
    } else if (length_int == 2) {
        var length = 3600;
    } else if (length_int == 3) {
        var length = 7200;
    } else {
        var length = 0;
    }
    var keywords = get_keywords()
    document.getElementById("search_recipe").href = "/findrecipe?length=" + length + "&keywords=" + keywords;
}

function reload_page() {
    window.location.reload(true);
}

function get_keywords() {
    return document.getElementById('recipe_filter_keywords').value;
}

function get_length() {
    return document.getElementById('recipe_filter_length').value;
}

function update_recipe_modal_on_show() {
    update_length_text(document.getElementById('recipe_filter_length').value);
}

function update_length_text(val) {
    if (val == 0) {
        document.getElementById('recipe_filter_length_text').value = "höchstens 15 min";
    } else if (val == 1) {
        document.getElementById('recipe_filter_length_text').value = "höchstens 30 min";
    } else if (val == 2) {
        document.getElementById('recipe_filter_length_text').value = "höchstens 60 min";
    } else if (val == 3) {
        document.getElementById('recipe_filter_length_text').value = "höchstens 120 min";
    } else {
        document.getElementById('recipe_filter_length_text').value = "Länge irrelevant";
    }
}
