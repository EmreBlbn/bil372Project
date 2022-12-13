$(document).ready(function () {
        $(".delete-form").on("submit",function (event) {
           $.ajax({
               data:$(this).serialize(),
               type:'GET',
               url:'/delete_user'
           }).done(function (data) {
               $(this).remove()
           });
           event.preventDefault()
        });

    });