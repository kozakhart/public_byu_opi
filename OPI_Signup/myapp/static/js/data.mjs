$(document).on('submit', '#form_id',function(e){
    e.preventDefault();

    $.ajax({
        type:'POST',
        url:'/data',
        headers:{
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
        },
        data:{
            //'csrfmiddlewaretoken':csrftoken,
            // agree:$('#check_box').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            
        },
        success:function(){
            //const netid = document.getElementById('netid').value
            //alert('Your test schedule will be sent to your BYU school email when ready at ' + netid + '.byu.edu through Microsoft Outlook. Please click this link if you have any questions on how to access your account: https://microsoft.byu.edu/email.byu.edu.')
            //redirect page
            alert('it works');
        },
        error: function(){
            // alert(data.responseJSON.error);
        }
});
}); 
