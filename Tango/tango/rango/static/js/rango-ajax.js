/* This piece of JQuery/JavaScript will add an event handler to the element with id #likes , i.e. the
button. When clicked, it will extract the category ID from the button element, and then make
an AJAX GET request which will make a call to /rango/like/ encoding the category_id in the
request. If the request is successful, then the HTML element with ID like_count (i.e. the <strong>
) is updated with the data returned by the request, and the HTML element with ID likes (i.e. the
<button> ) is hidden.
There is a lot going on here, and getting the mechanics right when constructing pages with AJAX
can be a bit tricky. Essentially, an AJAX request is made given our URL mapping when the button is
clicked. This invokes the like_category view that updates the category and returns the new number
of likes. When the AJAX request receives the response, it updates parts of the page, i.e. the text and
the button. The #likes button is hidden.
*/
$('#likes').click(function() {
    var catid;
    catid = $(this).attr('data=catid');
    $.get('/rango/like', {category_id : catid}, function(data) {
        $('#like_count').html(data);
            $('#likes').hide();
    });
});
$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/rango/suggest/', {suggestion: query}, function(data){
        $('#cats').html(data);
    });
});

$('.rango-add').click(function(){
    var catid = $(this).attr("data-catid");
    var url = $(this).attr("data-url");
    var title = $(this).attr("data-title");
    var me = $(this)
    $.get('/rango/add/', {category_id: catid, url: url, title: title}, function(data){
                   $('#pages').html(data);
                   me.hide();
               });
    });

});