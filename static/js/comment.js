"user strict";

function displayComment(results) {

    const formInput = $('comment').val();

    $('ul').prepend(formInput);
}

function showComment(evt) {
    evt.preventDefault();

    // const formValues = $('#comment-form').serialize();
    const formValues = {
        comment: $('#comment-form input[name="comment"]').val(),
        photoId: $('#comment-form input[name="photoId"]').val()
    }

    $.post(`/photos/${formValues.photoId}/comments`, formValues, displayComment);

}

$('#comment-form').on('submit', showComment);
