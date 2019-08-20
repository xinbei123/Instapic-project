"user-strict";
$('.far').click(function() {
    $(this).toggleClass('fas');

});


// $(document).ready(function(){

//     $('#like-form').on('submit', function(evt) {

//         evt.preventDefault();

//         photoId = $('#like-form button[name="likeBtn"]').val()
//         console.log(photoId)

//         $.post(`/photos/${photoId}/likes`, {photoId}, function(results) {
//             // alert('yes')

//             // for (let result of results) {

//         

//                 $('i').html(results[0]['num_like'])    
//             // };
//         })
//     });

// })


$(document).ready(function() {

    $('.upvote').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/like.json`, function(results) {

            console.log(results)

            $(evt.target).html(results.num_like)
        
        })

    }) 
})










