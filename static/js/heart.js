"user-strict";


$(document).ready(function(){

    $('#like-form').on('submit', function(evt) {

        evt.preventDefault();

        $.post('/photos', {'submit': true}, function(results) {

            for (let result of results) {

                $('.far').click(function() {
                    $(this).toggleClass('fas');

                });


                $('i').html(`${result['num_like']}`)

            }

        });
    })
});