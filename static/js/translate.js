$(document).ready(function(){

    $("#translation").submit(function(e){
        $.ajax({
            type: "POST",
            url: "/translate",
            data: $("form").serialize()
        });
        e.preventDefault();
    });

});