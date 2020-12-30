// My test
$(document).ready(function() {
    //JQuery code to be added in here.
    $('#about-btn').click(function(event) {
        alert('YOu clicked the button')
    })
    $('p').hover( function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'blue');
    });
    $('#about-btn').click( function(event) {
        msgstr = $('#msg').html()
        msgstr = msgstr + 'ooo'
        $('#msg').html(msgstr)
    });
})