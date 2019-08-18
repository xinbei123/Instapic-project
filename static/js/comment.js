"user strict";


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
            
                $('ul').prepend(`<li>${latestComment.comment}</li>`);
            });
    }

}

$('#comment-form').on('submit', showComment);
