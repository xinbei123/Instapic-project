"user-strict";


$(document).ready(function() {

    $('.saveFav').on('click', function (evt) {

        const photoId = $(evt.target).data('photo-id')

        $.post(`/photos/${photoId}/save.json`, function(results) {

            console.log(results)
        })
    })
})