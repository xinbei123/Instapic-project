"user-strict";

$(document).ready(function() {

    $('.hashBtn').on('click', function(evt) {

        evt.preventDefault();

        const photoId = $(evt.target).data('photo-id')
        const hashtagId = $(evt.target).data('hashtag-id')
    
        $.post(`/photos/${hashtagId}/hashtag.json`, function(results) {

            window.location.replace(`/photos/${hashtagId}/hashtag`)

    })
})

})