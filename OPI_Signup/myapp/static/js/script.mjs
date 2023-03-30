$(document).on('submit', '#form_ajax',function(e){
    e.preventDefault();
 
    const today = new Date();
    const testdate1 = new Date(document.getElementById('testdate1').value)
    const testdate2 = new Date(document.getElementById('testdate2').value)
    
    const time1 = document.getElementById('time1').value
    const split_time1 = time1.split(':')
    const time1_hour = parseInt(split_time1[0])
    const time1_min = parseInt(split_time1[1])

    const time2 = document.getElementById('time2').value
    const split_time2 = time2.split(':')
    const time2_hour = parseInt(split_time2[0])
    const time2_min = parseInt(split_time2[1])

    const time3 = document.getElementById('time3').value
    const split_time3 = time3.split(':')
    const time3_hour = parseInt(split_time3[0])
    const time3_min = parseInt(split_time3[1])

    const time4 = document.getElementById('time4').value
    const split_time4 = time4.split(':')
    const time4_hour = parseInt(split_time4[0])
    const time4_min = parseInt(split_time4[1])

    var email;
    var confirm_email;
    const regex_email = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    let loader = document.getElementById("loader");
    loader.style.display = "inline-block";

    // email = document.getElementById('email').value
    // confirm_email = document.getElementById('confirm_email').value

    //validation for 3 hour time slots
    if (time2_hour < (time1_hour + 3)){
        document.getElementById("time1").scrollIntoView()
        alert('Please schedule a test for a three hour time slot.')
        loader.style.display = "none"
        return;
    }
    if ((time2_min < time1_min) && (time2_hour == (time1_hour + 3))){
        document.getElementById("time1").scrollIntoView()
        alert('Please schedule a test for a three hour time slot.')
        loader.style.display = "none"
        return;
    }

    if (time4_hour < (time3_hour + 3)){
        document.getElementById("time3").scrollIntoView()
        alert('Please schedule a test for a three hour time slot.')
        loader.style.display = "none"
        return;
    }
    if ((time4_min < time3_min) && (time4_hour == (time3_hour + 3))){
        document.getElementById("time3").scrollIntoView()
        alert('Please schedule a test for a three hour time slot.')
        loader.style.display = "none"
        return;
    }

    //Email validation
    // if (email != confirm_email){
    //     document.getElementById("email").scrollIntoView()
    //     alert("Your emails do not match.");
    //     return;
    // }
    // if (email.match(regex_email)){
    // }
    // else{
    //     document.getElementById("email").scrollIntoView()
    //     alert('Invalid email');
    //     return;
    // }

    //Phone validation
    const phone = document.getElementById('phone').value
    const regex_phone = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
    if (phone.match(regex_phone)){
    }
    else{
        document.getElementById("phone").scrollIntoView()
        alert('Invalid phone number');
        loader.style.display = "none"
        return;
    }


    //Validation for weekends
    if (testdate1.getDay() == 5 | testdate1.getDay() == 6) {
        document.getElementById("testdate1").scrollIntoView()
        alert("You cannot schedule on the weekend.");
        loader.style.display = "none"
        return;
    }
    if (testdate2.getDay() == 5 | testdate2.getDay() == 6) {
        document.getElementById("testdate2").scrollIntoView()
        alert("You cannot schedule on the weekend.");
        loader.style.display = "none"
        return;
    }

    //Tuesday devotional validation
        if ((testdate1.getDay() == 1) && (time1_hour == 8 | time1_hour == 9 | time1_hour == 10) && (time2_hour > 11 | (time2_hour == 11&& time2_min > 0))){
            document.getElementById("time1").scrollIntoView()
            alert('You cannot schedule during a devotional.')
            loader.style.display = "none"
            return;
        }
        if ((testdate2.getDay() == 1) && (time3_hour == 8 | time3_hour == 9 | time3_hour == 10) && (time4_hour > 11 | (time4_hour == 11 && time4_min > 0))){
            document.getElementById("time3").scrollIntoView()
            alert('You cannot schedule during a devotional.')
            loader.style.display = "none"
            return;
        }
        
    //if first month is before second month validation
    if (testdate1.getFullYear() > testdate2.getFullYear()){
        document.getElementById("testdate1").scrollIntoView()
        alert('Your first date must be before your second date. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return; 
    }

    if ((testdate1.getMonth() > testdate2.getMonth()) & (testdate1.getFullYear() >= testdate2.getFullYear())){
        document.getElementById("testdate1").scrollIntoView()
        alert('Your first date must be before your second date. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }
    if ((testdate1.getMonth() == testdate2.getMonth()) & (testdate1.getDate() > testdate2.getDate())){
        document.getElementById("testdate1").scrollIntoView()
        alert('Your first date must be before your second date. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }

    //cannot schedule before today
    if ((testdate1.getDate() < today.getDate() + 2) & (testdate1.getMonth() <= today.getMonth()) & (testdate1.getFullYear() == today.getFullYear())){

    // if ((testdate1.getDate() < today.getDate() + 13) & (testdate1.getMonth() <= today.getMonth()) & (testdate1.getFullYear() == today.getFullYear())){
        document.getElementById("testdate1").scrollIntoView()
        alert('Error 601: 1 Your first testing date must be at least 14 days from today. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }
    if ((today.getDate() > (testdate1.getDate())) & (today.getMonth() >= testdate1.getMonth()) & (testdate1.getFullYear() == today.getFullYear())){
        document.getElementById("testdate1").scrollIntoView()
        alert('Error 602: Your first testing date must be at least 14 days from today. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }
    // if ((today.getDate() > testdate2.getDate()) & (today.getMonth() >= testdate2.getMonth()) & (testdate2.getFullYear() == today.getFullYear())){
    //     document.getElementById("testdate2").scrollIntoView()
    //     alert('Your second testing date must be after your first date. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
    //     return;
    // }

    if ((testdate1.getDate() > testdate2.getDate()) & (testdate1.getMonth() >= testdate2.getMonth()) & (testdate2.getFullYear() == today.getFullYear())){
        document.getElementById("testdate2").scrollIntoView()
        alert('Error 603: Your second testing date must be after your first date. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }
    if ((testdate1.getDate() == testdate2.getDate()) & (testdate1.getMonth() == testdate2.getMonth()) & (testdate1.getFullYear() == testdate2.getFullYear())){
        document.getElementById("testdate1").scrollIntoView()
        alert('Error 604: Your testing dates must be on different days. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.')
        loader.style.display = "none"
        return;
    }

    var verified
    verified = document.getElementById('verified').value
    if (verified != "VERIFIED"){
        document.getElementById("verified").value=""
        document.getElementById("verified").scrollIntoView()
        alert('You have not verified your information.')
        loader.style.display = "none"
        return;
    }

    //Check to make sure that selections are not empty
    var reason
    reason = document.getElementById('reason').value
    if (reason == ""){
        document.getElementById("reason").scrollIntoView()
        alert('You have not provided a reason for taking an OPI.')
        loader.style.display = "none"
        return;
    }
    var reason_other
    reason_other = document.getElementById('reason_other').value
    if ((reason == "Other") && reason_other == "") {
        document.getElementById("reason_other").scrollIntoView()
        alert("Please provide a reason for taking the test. If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.")
        loader.style.display = "none"
        return;
    }
    //change this
    if ((reason != "Other") && (reason_other != "")){
        document.getElementById("reason_other").value="NA"
    }
    var language
    language = document.getElementById("language").value
    if (language == ""){
        document.getElementById("language").scrollIntoView()
        alert("Please specify the language for which you are requesting an OPI.")
        loader.style.display = "none"
        return;
    }
    var language_other
    language_other = document.getElementById("language_other")
    if ((language == "Other") && (language_other == "")){
        alert("Please specify the language for which you are requesting an OPI.")
        loader.style.display = "none"
        return;
    }
        $.ajax({
            type:'POST',
            url:'/create',
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data:{
                //'csrfmiddlewaretoken':csrftoken,
                agree:$('#agree').val(),
                firstname:$('#firstname').val(),
                lastname:$('#lastname').val(),
                byuid:$('#byuid').val(),
                netid:$('#netid').val(),
                email:$('#email').val(),
                reason:$('#reason').val(),
                reason_other:$('#reason_other').val(),
                language:$('#language').val(),
                language_other:$('#language_other').val(),
                experience:$('#experience').val(),
                major:$('#major').val(),
                second_major:$('#second_major').val(),
                minor:$('#minor').val(),
                graduate:$('#graduate').val(),
                scores:$('#scores').val(),
                come_to_campus:$('#come_to_campus').val(),
                cannot_come:$('#cannot_come').val(),
                testdate1:$('#testdate1').val(),
                time1:$('#time1').val(),
                time2:$('#time2').val(),
                testdate2:$('#testdate2').val(),
                time3:$('#time3').val(),
                time4:$('#time4').val(),
                confirm_email:$('#confirm_email').val(),
                phone:$('#phone').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                
            },
            success:function(){
                loader.style.display = "none"
                //const netid = document.getElementById('netid').value
                //alert('Your test schedule will be sent to your BYU school email when ready at ' + netid + '.byu.edu through Microsoft Outlook. Please click this link if you have any questions on how to access your account: https://microsoft.byu.edu/email.byu.edu.')
                //redirect page
                window.location.href = "/receipt"
        },
            error: function(data){
                loader.style.display = "none"
                document.getElementById("testdate1").scrollIntoView()
                alert(data.responseJSON.error + " If you believe that this message is a mistake or that the website is broken, please text 623-414-1835, or call CLS at 801-422-1201. Thank you for your patience.");
         }
    });
}); 
