"use-strict";


$(document).ready(function() {

    $('.fa-sign-out-alt').on('click', function(evt) {

        evt.preventDefault();

        setTimeout(function() {

            window.location.replace("/logout")});


    });

})



