$(document).ready(function(){

	$("#translation [type='submit']").click(function(e){
		e.preventDefault();
		var data = $("form").serializedArray();
		$.ajax({
			type: "POST",
			url: "/translate",
			data: data
		});
	});

});