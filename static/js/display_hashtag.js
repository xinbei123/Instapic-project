"user-strict";

$(document).ready(function() {

    $('.hashBtn').on('click', function(evt) {

        const photoId = $(evt.target).data('photo-id')
        const hashtagId = $(evt.target).data('hashtag-id')
    
        $.post(`/photos/${hashtagId}/hashtag.json`, function(results) {

            const latestTagged = results[results.length-1];

            window.location.replace(`/photos/${hashtagId}/hashtag`)

    })
})

})