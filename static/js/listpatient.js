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
						parse+="<p> p id:"+obj.p_id+", "+"obj name: "+ obj.p_name+", "+"obj tc: "+ obj.p_tc+"</p><br>";
					}
                    $('#search-result').html(parse);
                }
            }
        );
    }

});
