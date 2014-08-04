$(document).ready(function(){

    // show sidebar on load
    $("#sidebar").show();
    $("#nav_close").css({
        'color'  : '#F9E562',
        'cursor' : 'default'
    });

    // scoots over on mouseover--fix this
    // $(".commit-log").mouseover(function() {
    //     $(this).animate({margin: "35px 30px"});
    // });

    // $(".commit-log").mouseout(function() {
    //     $(this).animate({margin: "35px 0px"});
    // });

    // timestamper
    $("abbr.timeago").timeago();
});