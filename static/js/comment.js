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
            
                $('#commentId').prepend(`<li><i class="fas fa-user-circle fa-lg"></i>${latestComment.comment}</li>`);
            });

        $('#comment-form input[name="comment"]').val('');
    }

}

$('#comment-form').on('submit', showComment);
