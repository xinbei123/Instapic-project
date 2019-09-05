"use-strict";

$(document).ready(function() {

    $('#logoutBtn').on('click', function(evt) {

        evt.preventDefault();

        console.log(evt)

        setTimeout(function() {
            window.location.replace("/logout")
        }, 3000)

    });

})



