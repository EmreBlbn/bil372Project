$('#search_box').keyup(function (key) {
    var key_value=key.which;
    if(key_value != ""){
        $.ajax({
                url: "/search_patient",
                data: {text:key_value},
                type: 'POST',
                success: function (data) {
                	var parse="";
					for(var i=0;data.length;i++){
						var obj=data.query[i];
						parse+="<p> patient id:"+obj.id+", "+"obj name: "+ obj.name+"</p><br>";
					}
                    $('#search-result').html(parse);
                }
            }
        );
    }

});
