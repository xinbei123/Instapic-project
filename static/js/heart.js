"use-strict";

$(document).ready(function() {

    $('.upvote').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/like.json`, function(results) {

            $(evt.target).html(results.num_like)
        
        });

    }); 

    $('.downvote').on('click', function(evt) {

        const photoid = $(evt.target).data('photo-id')

        $.post(`/photos/${photoid}/dislike.json`, function(results) {

            $(evt.target).html(results.num_dislike)
        })

    })

});








