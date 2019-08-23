"user-strict";

$(document).ready(function(){

    $.get('/hashtag.json', function (results) {

        hashtag_array = []

        for (let result of results){

            hashtag_array.push(result['hashtag'])

        }

        var hashtags = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            local: hashtag_array
        });
        
        // Initializing the typeahead
        $('.typeahead').typeahead({
            hint: true,
            highlight: true, 
            minLength: 1 
        },
        {
            name: 'hashtags',
            source: hashtags
        });
    })
    
});













