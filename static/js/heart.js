"use-strict";

//Ajax post request for thumbsup/thumbsdown button
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

            console.log(results)

            $(evt.target).html(results.num_dislike)
        })

    })

});








