$(document).ready(function(){

    // show sidebar on load
    $("#sidebar").show();
    $("#nav_close").css({
        'color'  : '#F9E562',
        'cursor' : 'default'
    });

    // timestamper
    $("abbr.timeago").timeago();
});