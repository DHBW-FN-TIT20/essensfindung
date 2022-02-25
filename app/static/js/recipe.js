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
    var new_link = "/findrecipe?length=" + length + "&keywords=" + keywords;
    document.getElementById("search_recipe").href = new_link;
    document.getElementById("search_recipe_from_modal").href = new_link;
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


/*============================  Recipe Result JS ===============================*/

function fillTimesNumbers() {
    let prepString = "";
    prepString += (prepTime.days == 0) ? "" : prepTime.days + ":";
    prepString += (prepTime.hours == 0) ? "" : prepTime.hours + ":";
    prepString += (prepTime.minutes.length == 1) ? "0" + prepTime.minutes + ":" : prepTime.minutes + ":";
    prepString += (prepTime.seconds.length == 1) ? "0" + prepTime.seconds : prepTime.seconds;
    document.getElementById("prepTime").innerText = prepString;

    let cookString = "";
    cookString += (cookTime.days == 0) ? "" : cookTime.days + ":";
    cookString += (cookTime.hours == 0) ? "" : cookTime.hours + ":";
    cookString += (cookTime.minutes.length == 1) ? "0" + cookTime.minutes + ":" : cookTime.minutes + ":";
    cookString += (cookTime.seconds.length == 1) ? "0" + cookTime.seconds : cookTime.seconds;
    document.getElementById("cookTime").innerText = cookString;
}

function fillTimesLabels() {
    let prepString = "";
    prepString += (prepTime.days == 0) ? "" : prepTime.days + " tage ";
    prepString += (prepTime.hours == 0) ? "" : prepTime.hours + " std. ";
    prepString += (prepTime.minutes == 0) ? "" : prepTime.minutes + " min. ";
    prepString += (prepTime.seconds == 0) ? "" : prepTime.seconds + " sek. ";
    document.getElementById("prepTime").innerText = prepString;

    let cookString = "";
    cookString += (cookTime.days == 0) ? "" : cookTime.days + " tage ";
    cookString += (cookTime.hours == 0) ? "" : cookTime.hours + " std. ";
    cookString += (cookTime.minutes == 0) ? "" : cookTime.minutes + " min. ";
    cookString += (cookTime.seconds == 0) ? "" : cookTime.seconds + " sek. ";
    document.getElementById("cookTime").innerText = cookString;
}

function parseIngredientString() {
    ingredientArray = ingredientString.split("\n");

    parent = document.createElement('ul');
    parent.setAttribute('class', 'list-group-flush ps-1')

    for (i = 0; i < ingredientArray.length; i++) {
        let li = document.createElement('li');
        li.setAttribute('class', 'list-group-item')
        li.innerText = ingredientArray[i];
        parent.appendChild(li);
    }

    document.getElementById("ingredientContainer").appendChild(parent);    
}

function addIngredientsDisplayListener() {
    document.getElementById("toggleIngredients").addEventListener("click", e => {
        e.preventDefault();
        let ings = document.getElementById("ingredientContainer");
        if (ings.classList.contains("d-none")) {
            e.target.innerText = "Zutaten verbergen";
            ings.classList.remove("d-none");
        } else {
            e.target.innerText = "Zutaten anzeigen";
            ings.classList.add("d-none");
        }
    })
}

function fillRecipeHref() {
    document.getElementById("recipeHref").innerText = recipeURL.hostname;
    if (recipeURL.hostname == "tastykitchen.com") {
        //turn off ingredients due to bad source in JSON
        document.getElementById("toggleIngredients").classList.add("d-none");
    }
}

//code borrowed from https://keith.gaughan.ie/detecting-broken-images-js.html
function testImg(img) {
    // During the onload event, IE correctly identifies any images that
    // weren't downloaded as not complete. Others should too. Gecko-based
    // browsers act like NS4 in that they report this incorrectly.
    if (!img.complete) {
        return false;
    }

    // However, they do have two very useful properties: naturalWidth and
    // naturalHeight. These give the true size of the image. If it failed
    // to load, either of these should be zero.
    if (typeof img.naturalWidth != "undefined" && img.naturalWidth == 0) {
        return false;
    }

    // No other way of checking: assume it's ok.
    return true;
}

function addImageLoadListener() {
    window.addEventListener("load", e => {
        if (!testImg(document.getElementById("recipe-image"))) {
            document.getElementById("imageContainer").classList.add("d-none")
        } 
    });
}

function initRecipeResult() {
    fillTimesLabels();
    fillRecipeHref();
    parseIngredientString();
    addIngredientsDisplayListener();
    addImageLoadListener();
}
