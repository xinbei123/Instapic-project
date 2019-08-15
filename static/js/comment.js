"user strict";

function displayComment(results) {

    $('ul').prepend("<li>" + $('comment') + "</li>");
}

function showComment(evt) {
    evt.preventDefault();

    const formValues = {
        comment: $('#comment-form input[name="comment"]').val(),
        photoId: $('#comment-form input[name="photoId"]').val()
    }

    $.post(`/photos/${formValues.photoId}/comments`, formValues, displayComment);

}

// $('#comment-form').on('submit', showComment);

// $function() {

//     const $comment_text = $('comment-text');
//     const $comment_list = $('comment-list');

//     $('add-comment').on('click', function() {

//         evt.preventDefault();

//         const data = {
//             comment: $comment_text.val();

//         };

//         $.ajax({
//             type: 'POST',
//             url: '/photos/{photo.photo_id}/comments',
//             data: data,
//             success: function (newComment) {

//                 $comment_list.append('<li>' +  data.comment +'</li>')



//             }
//         })

//     })

}
