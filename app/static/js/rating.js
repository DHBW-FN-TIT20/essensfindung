/* sort and filter code */

//contains objects corresponding to each entry on the page
let entries = []

function sortDOMbyTime(list, direction, parent) {
    //bubble sorts a list of objects as well as the DOM according to a UNIX timestamp
    //  list: array of objects (see "generating objects for each page entry")
    //  direction: bool that changes sort direction, true for asc and false for desc
    //  parent: node of the parent element of the dom elements to be sorted
    let s, n = list.length;
    do {
        s = false;
        for (i = 1; i < n; i++) {
            if (direction) {
                if (list[i - 1].timestamp > list[i].timestamp) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            } else {
                if (list[i - 1].timestamp < list[i].timestamp) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            }
        }
        n = n - 1;
    } while (s);
}
function sortDOMbyRating(list, direction, parent) {
    //bubble sorts a list of objects as well as the DOM according to the object rating
    //  list: array of objects (see "generating objects for each page entry")
    //  direction: bool that changes sort direction, true for asc and false for desc
    //  parent: node of the parent element of the dom elements to be sorted
    let s, n = list.length;
    do {
        s = false;
        for (i = 1; i < n; i++) {
            if (direction) {
                if (list[i - 1].rating > list[i].rating) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            } else {
                if (list[i - 1].rating < list[i].rating) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            }
        }
        n = n - 1;
    } while (s);
}
function sortDOMbyName(list, direction, parent) {
    //bubble sorts a list of objects as well as the DOM according to the entry name
    //  list: array of objects (see "generating objects for each page entry")
    //  direction: bool that changes sort direction, true for asc and false for desc
    //  parent: node of the parent element of the dom elements to be sorted
    let s, n = list.length;
    do {
        s = false;
        for (i = 1; i < n; i++) {
            if (direction) {
                if (list[i - 1].name.toLowerCase() > list[i].name.toLowerCase()) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            } else {
                if (list[i - 1].name.toLowerCase() > list[i].name.toLowerCase()) {
                    parent.insertBefore(list[i].parent, list[i - 1].parent);
                    x = list[i];
                    list[i] = list[i - 1];
                    list[i - 1] = x;
                    s = true;
                }
            }
        }
        n = n - 1;
    } while (s);
}

function initDrawers() {
    //creates event listeners to enable Filter/Sort Drawer functionality

    /* filter and sort drawer functionality */

    let filterSymbol = document.getElementById("filterSymbol");
    let filterButton = document.getElementById("filterButton")
    let sortSymbol = document.getElementById("sortSymbol");
    let sortButton = document.getElementById("sortButton");

    let filterButtons = document.getElementById("filterButtonsContainer");
    let sortButtons = document.getElementById("sortButtonsContainer");

    filterButton.addEventListener("click", e => {
        if (filterButton.classList.contains("filter-up")) {
            filterButton.classList.remove("filter-up");
            filterButton.classList.add("filter-down");
            filterSymbol.classList.remove("filter-character-up");
            filterSymbol.classList.add("filter-character-down");

            filterButtons.classList.remove("d-none");
            filterButtons.classList.add("d-flex");
        } else if (filterButton.classList.contains("filter-down")) {
            filterButton.classList.add("filter-up");
            filterButton.classList.remove("filter-down");
            filterSymbol.classList.add("filter-character-up");
            filterSymbol.classList.remove("filter-character-down");

            filterButtons.classList.add("d-none");
            filterButtons.classList.remove("d-flex");
        }
    });

    sortButton.addEventListener("click", e => {
        if (sortButton.classList.contains("sort-up")) {
            sortButton.classList.remove("sort-up");
            sortButton.classList.add("sort-down");
            sortSymbol.classList.remove("filter-character-up");
            sortSymbol.classList.add("filter-character-down");

            sortButtons.classList.remove("d-none");
            sortButtons.classList.add("d-flex");
        } else if (sortButton.classList.contains("sort-down")) {
            sortButton.classList.add("sort-up");
            sortButton.classList.remove("sort-down");
            sortSymbol.classList.add("filter-character-up");
            sortSymbol.classList.remove("filter-character-down");

            sortButtons.classList.add("d-none");
            sortButtons.classList.remove("d-flex");
        }
    });
}

function initSort() {
    //creates event listeners for sort buttons

    //sorting functions
    //sorts by date descending
    document.getElementById("sortDateDesc").addEventListener("click", e => {
        console.log("sorting date desc");
        if (e.target.checked) {
            //sort by date desc

            //contains the parent element
            parent = document.querySelector(".entry").parentNode.parentNode.parentNode;
            
            //bubble sort to rearrange dom
            sortDOMbyTime(entries, false, parent);
        }
    });
    //sorts by date ascending
    document.getElementById("sortDateAsc").addEventListener("click", e => {
        console.log("sorting date asc");
        if (e.target.checked) {
            //contains the parent element
            parent = document.querySelector(".entry").parentNode.parentNode.parentNode;
            
            //bubble sort to rearrange dom
            sortDOMbyTime(entries, true, parent);
        }
    });
    //sorts by rating descending
    document.getElementById("sortRatingDesc").addEventListener("click", e => {
        console.log("sorting rating desc");
        if (e.target.checked) {
            //contains the parent element
            parent = document.querySelector(".entry").parentNode.parentNode.parentNode;

            //bubble sort to rearrange dom
            sortDOMbyRating(entries, false, parent);
        }
    });
    //sorts by rating asc
    document.getElementById("sortRatingAsc").addEventListener("click", e => {
        console.log("sorting rating asc");
        if (e.target.checked) {
            //contains the parent element
            parent = document.querySelector(".entry").parentNode.parentNode.parentNode;

            //bubble sort to rearrange dom
            sortDOMbyRating(entries, true, parent);
        }
    });
}
function initFilter() {
    //creates event listeners for filter buttons


    //filters entries that are a restaurant
    document.getElementById("filterRestaurant").addEventListener("click", e => {
        if (e.target.checked) {
            //show entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].type == "Restaurant") {
                    //entry is a restaurant
                    entries[i].parent.classList.remove("d-none");
                }
            }
        } else {
            //hide entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].type == "Restaurant") {
                    //entry is a restaurant
                    entries[i].parent.classList.add("d-none");
                }
            }
        }
    });

    //filters entries that are a recipe
    document.getElementById("filterRezepte").addEventListener("click", e => {
        if (e.target.checked) {
            //show entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].type == "Recipe") {
                    //entry is a restaurant
                    entries[i].parent.classList.remove("d-none");
                }
            }
        } else {
            //hide entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].type == "Recipe") {
                    //entry is a restaurant
                    entries[i].parent.classList.add("d-none");
                }
            }
        }
    });

    //filters entries with a rating
    document.getElementById("filterWithBewertung").addEventListener("click", e => {
        if (e.target.checked) {
            //show entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].rating !== 0) {
                    //entry has a rating
                    entries[i].parent.classList.remove("d-none");
                }
            }
        } else {
            //hide entries with a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].rating !== 0) {
                    //entry has a rating
                    entries[i].parent.classList.add("d-none");
                }
            }
        }
    });
    //filters entries without a rating
    document.getElementById("filterWithoutBewertung").addEventListener("click", e => {
        if (e.target.checked) {
            //show entries without a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].rating === 0) {
                    //entry does not have a rating
                    entries[i].parent.classList.remove("d-none");
                }
            }
        } else {
            //hide entries without a rating
            for (i = 0; i < entries.length; i++) {
                if (entries[i].rating === 0) {
                    //entry does not have a rating
                    entries[i].parent.classList.add("d-none");
                }
            }
        }
    });
}

function init() {
    //generating objects for each page entry
    document.querySelectorAll(".entry").forEach(e => {
        //parse rating
        rating = e.querySelector(".entry-rating").innerText.trim();
        rating = (rating === "Keine Bewertung") ? 0 : parseInt(rating.slice(0, 1));

        //create entry object
        entries.push(
            {
                name: e.querySelector(".entry-name").innerText,
                rating: rating,
                timestamp: parseInt(e.querySelector(".entry-timestamp").innerText),
                parent: e.parentNode.parentNode,
                type: e.querySelector(".type").innerText
            }
        );
    });

    //create event listeners for page functionality
    initDrawers();
    initSort();
    initFilter();

    //sort list alphabetically
    parent = document.querySelector(".entry").parentNode.parentNode.parentNode;
    sortDOMbyName(entries, true, parent);
}