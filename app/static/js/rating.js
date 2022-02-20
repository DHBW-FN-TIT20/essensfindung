/* sort and filter code */

//contains objects corresponding to each entry on the page
let entries = []

//generating objects for each page entry
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

//filters entries with a rating
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

//filters entries without a rating
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
});

//sorting functions
//sorts by date descending
document.getElementById("sortDateDesc").addEventListener("click", e => {
    console.log("sorting date desc");
    if (e.target.checked) {
        //sort by date desc

        //contains the parent element
        parent = document.querySelector(".entry").parentNode.parentNode.parentNode;
        //contains a list of entires which are children of the parent element
        entryList = [];
        document.querySelectorAll(".entry").forEach(e => {
            entryList.push(e.parentNode.parentNode);
        });
        
        //bubble sort to rearrange dom
        let s, n = entries.length;
        do {
            s = false;
            for (i = 1; i < n; i++) {
                if (entries[i - 1].timestamp < entries[i].timestamp) {
                    parent.insertBefore(entries[i].parent, entries[i - 1].parent);
                    x = entries[i];
                    entries[i] = entries[i - 1];
                    entries[i - 1] = x;
                    s = true;
                }
            }
            n = n - 1;
        } while (s);
    }
});

//sorts by date ascending
document.getElementById("sortDateAsc").addEventListener("click", e => {
    console.log("sorting date asc");
    if (e.target.checked) {
        //contains the parent element
        parent = document.querySelector(".entry").parentNode.parentNode.parentNode;
        
        //bubble sort to rearrange dom
        let s, n = entries.length;
        do {
            s = false;
            for (i = 1; i < n; i++) {
                if (entries[i - 1].timestamp > entries[i].timestamp) {
                    parent.insertBefore(entries[i].parent, entries[i - 1].parent);
                    x = entries[i];
                    entries[i] = entries[i - 1];
                    entries[i - 1] = x;
                    s = true;
                }
            }
            n = n - 1;
        } while (s);
    }
});

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