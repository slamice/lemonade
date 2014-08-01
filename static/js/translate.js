$(document).ready(function(){

    // toggle sidebar
    $("#nav_open").click(function(){
        $("#sidebar").toggle('slide', 500);
    });

    $("#nav_close").click(function(){
        $("#sidebar").toggle('slide', 500);
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
        var cat_width = $("#cat").width();
        $("#cat").animate({left: width-cat_width}, 1000);
    });

    // save commit + prevent refresh
    $("#translation").submit(function(e){
        $.ajax({
            type: "POST",
            url: "/translate",
            data: $("form").serialize()
        });
        e.preventDefault();
        $("input[name*='message']").val('');
    });
});