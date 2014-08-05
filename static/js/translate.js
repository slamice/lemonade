$(document).ready(function(){

    // edit height of editor
    var window_height = $(window).height();
    var source_height = $("#source-text").height();
    var footer_height = $("#footer").height();
    $("#translation textarea").css({
        "height"     : source_height-footer_height,
        "min-height" : window_height-footer_height-200
    });

    // timestamper
    $("abbr.timeago").timeago();

    // toggle sidebar
    $("#nav_open").click(function(){
        $("#sidebar").toggle('slide', 500);
        $("#overlay").show().animate({
            opacity: 1
        }, 150);
    });

    $("#nav_close").click(function(){
        $("#sidebar").toggle('slide', 500);
        $("#overlay").animate({
            opacity: 0
        }, 150, function(){
            $(this).hide();
        });
    });

    // focus on textarea + move cursor to end of text
    var el = $("#translation textarea").get(0);
    var elemLen = el.value.length;

    el.selectionStart = elemLen;
    el.selectionEnd = elemLen;
    el.focus();

    // magicat!
    $("#cat-button").click(function(e){
        e.preventDefault();
        var width = $(window).width();
        var cat_width = $("#cat img").width();
        var duration = 10000; // 10 seconds

        $("#cat").animate({
            left: width+cat_width
        }, {
            duration : duration,
            easing   : 'linear',
            complete : function() {
                $('#cat').css('left', cat_width * -1);
            }
        });
    });

    // save commit + prevent refresh
    $("#translation").submit(function(e){
        $.ajax({
            type : "POST",
            url  : "/translate",
            data : $("form").serialize()
        });
        e.preventDefault();
        $("input[name*='message']").val('');
    });
});