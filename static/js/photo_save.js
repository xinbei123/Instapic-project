"user-strict";


$(document).ready(function() {

    $('.saveFav').on('click', function (evt) {

        evt.preventDefault(); 

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/save.json`, function(results) {

            console.log(results)

            const latestSavedPhoto = results[results.length-1];

            $('ul').prepend(`<li>${latestSavedPhoto.photo_url}</li>`)

        })
    })
})

// to do
// need to figure out how to redirect to the user profile page
// need to figure out how to let user not save the same photo multiple times