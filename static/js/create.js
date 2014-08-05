$(document).ready(function(){

    // show sidebar on load
    $("#sidebar").show();
    $("#nav_close").css({
        'color'  : '#F9E562',
        'cursor' : 'default'
    });

    // height of form
    var window_height = $(window).height();
    var input_height = window_height-350;
    $("#create textarea").css('height', input_height);


    // timestamper
    $("abbr.timeago").timeago();
});