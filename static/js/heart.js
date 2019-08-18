"user-strict";


$(document).ready(function(){

    $('#like-form').on('submit', function(evt) {

        evt.preventDefault();

        photoId = $('#like-form button[name="likeBtn"]').val()
        console.log(photoId)

        $.post(`/photos/${photoId}/likes`, {photoId}, function(results) {
            // alert('yes')

            // for (let result of results) {

                // $('.far').click(function() {
                //     $(this).toggleClass('fas');

                // });

                $('i').html(results[0]['num_like'])    
            // };
        })
    });

})



