"user-strict";


$(document).ready(function() {

    $('.saveFav').on('click', function (evt) {

        const photoId = $(evt.target).data('photo-id')

        var url = $(this).data('target')
        location.replace(url);

        $.post(`/photos/${photoId}/save.json`, function(results) {

            console.log(results)
        })
    })
})

// in the callback function, need to display photo img based on photo_id
// show the image in user profile section