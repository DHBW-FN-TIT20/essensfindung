/******** inititialize star-rating-svg *****************/
$("#rating_edit_rating").raty({
    starOff: '/static/img/icons8-star-32.png',
    starOn: '/static/img/icons8-star-32-filled.png',
    click: function(score, evt) {
        document.getElementById('rating_edit_rating_target').value = score;
    },
    score: function() {
        return document.getElementById('rating_edit_rating_target').value;
    }
});