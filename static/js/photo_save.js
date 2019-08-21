"user-strict";


$(document).ready(function() {

    $('.saveFav').on('click', function (evt) {

        evt.preventDefault(); 

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/save.json`, function(results) {

            console.log(results)

            const latestSavedPhoto = results[results.length-1];

            window.location.replace(`/users/${results[0]['user_id']}`)

            $('div').prepend(`${latestSavedPhoto.photo_url}`)

        })
    })
})
