$(document).ready(function() {
    lookupSuggestion('');
});

$('#likes').click(function(){
    var catid;
    catid = $(this).attr('data-catid');
    $.get('/fungo/like_category', {category_id: catid}, function(data) {
        $('#like_count').html(data);
        $('#likes').hide();
    });
});

$('#suggestion').keyup(function (){
    lookupSuggestion($(this).val());
});

function lookupSuggestion(query) {
    $.get('/fungo/suggest_category', {suggestion: query}, function(data){
        $('#cats').html(data);
    });
};
