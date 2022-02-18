/* sort and filter code */
let entries = []

document.querySelectorAll(".entry").forEach(e => {
    entries.push(
        {
            name: e.querySelector(".entry-name").innerText,
            rating: e.querySelector(".entry-rating").innerText,
            timestamp: parseInt(e.querySelector(".entry-timestamp").innerText),
            parent: e.parentNode.parentNode
        }
    );
});

document.getElementById("filterWithBewertung").addEventListener("click", e => {
    if (e.target.checked) {
        //show entries with a rating
        for (i = 0; i < entries.length; i++) {
            if (entries[i].rating !== "Keine Bewertung") {
                //entry has a rating
                entries[i].parent.classList.remove("d-none");
            }
        }
    } else {
        //hide entries with a rating
        for (i = 0; i < entries.length; i++) {
            if (entries[i].rating !== "Keine Bewertung") {
                //entry has a rating
                entries[i].parent.classList.add("d-none");
            }
        }
    }
});

document.getElementById("filterWithoutBewertung").addEventListener("click", e => {
    if (e.target.checked) {
        //show entries without a rating
        for (i = 0; i < entries.length; i++) {
            if (entries[i].rating === "Keine Bewertung") {
                //entry does not have a rating
                entries[i].parent.classList.remove("d-none");
            }
        }
    } else {
        //hide entries without a rating
        for (i = 0; i < entries.length; i++) {
            if (entries[i].rating === "Keine Bewertung") {
                //entry does not have a rating
                entries[i].parent.classList.add("d-none");
            }
        }
    }
})


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
})