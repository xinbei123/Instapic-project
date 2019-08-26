"use-strict";


function showComment(evt) {

    evt.preventDefault();

    const formValues = {
        comment: $('#comment-form input[name="comment"]').val(),
        photoId: $('#comment-form input[name="photoId"]').val()
    }


    if (formValues.comment) {

        $.post(
            `/photos/${formValues.photoId}/comments`,formValues,
            (comments) => {
                
                const latestComment = comments[comments.length - 1];
            
                $('#commentId').prepend(`<li>${latestComment.comment}</li>`);
            });

        $('#comment-form input[name="comment"]').val('');
        $('#commentMsg').html('Comments Saved!')
    }

}

$('#comment-form').on('submit', showComment);
