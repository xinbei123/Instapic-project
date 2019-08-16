"user-strict";

$(document).ready(function(){
    // Defining the local dataset
    var hashtags = ['cat', 'kitten'];
    
    // Constructing the suggestion engine
    var hashtags = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: hashtags
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
});

function showHashtag(evt) {

    evt.preventDefault();

    const formValues = {
        hashtag: $('#hashtag-form input[name="hashtag"]').val()
    }

    if (formValues.hashtag) {
        
    }
}