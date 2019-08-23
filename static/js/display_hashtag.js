"user-strict";

$(document).ready(function() {

    $('.hashBtn').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')
        const hashtagId = $(evt.target).data('hashtag-id')
    
        $.post(`/photos/${hashtagId}/hashtag.json`, function(results) {

            console.log(results)

            window.location.replace(`/photos/${hashtagId}/hashtag`)

    })
})

})