"user-strict";

// $('.far').click(function() {
//     $(this).toggleClass('fas');

// });


$(document).ready(function() {

    $('.upvote').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/like.json`, function(results) {

            console.log(results)

            $(evt.target).html(results.num_like)
        
        })

    }) 
})










