"user-strict";

//Ajax post request for like button
$(document).ready(function() {

    $('.upvote').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/like.json`, function(results) {

            $(evt.target).html(results.num_like)
        
        });

    }); 
});

//Ajax post request for unlike button
$(document).ready(function() {

    $('.downvote').on('click', function(evt) {

        const photoid = $(evt.target).data('photo-id')

        $.post(`/photos/${photoid}/dislike.json`, function(results) {

            $('#likeBtn').html(results.num_like)
        })

    })
})








