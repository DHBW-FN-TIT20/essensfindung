/******** inititialize star-rating-svg *****************/
$("#rating_edit_rating").raty({
    starOff: 'https://cdn.jsdelivr.net/npm/raty-js@3.1.1/lib/images/star-off.png',
    starOn: 'https://cdn.jsdelivr.net/npm/raty-js@3.1.1/lib/images/star-on.png',
    click: function(score, evt) {
        document.getElementById('rating_edit_rating_target').value = score;
    },
    score: function() {
        return document.getElementById('rating_edit_rating_target').value;
    }
});