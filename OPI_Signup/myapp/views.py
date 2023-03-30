from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import get_template
from datetime import *
from .forms import OPIForm_Forms, SLATForm_Forms
from .models import OPIForm, SLATForm
import myapp.filemaker_api.filemaker_api as filemaker
import myapp.byu_api.byu_api as byu_api
import json
import myapp.google_api.service_account as google_calendar
import myapp.slack_api.slack as slack_message
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
import time
import myapp.box_api.box_api as box_api
from myapp.box_api.box_api import *
from django.core.files.storage import FileSystemStorage

def receipt(request):
    get_template('receipt.html')
    return render(request, 'receipt.html')

@staff_member_required
def index_data(request):
    token = filemaker.login()
    persons = []
    individual = []
    data = []   
    if request.method == 'POST':
        if 'search' in request.POST:
            input_data = {}
            select1 = (request.POST.get('search_select1', False))
            input1 = (request.POST.get('search_input1', False))
            
            select2 = (request.POST.get('search_select2', False))
            input2 = (request.POST.get('search_input2', False))

            select3 = (request.POST.get('search_select3', False))
            input3 = (request.POST.get('search_input3', False))

            if input1 != '' or input1 != False:
                input_data[select1] = input1
            if input2 != '' or input2 != False:
                input_data[select2] = input2
            if input3 != '' or input3 != False:
                input_data[select3] = input3
            print(select1, input1, select2, input2, select3, input3)
            token = filemaker.login()
            get_record = filemaker.adaptive_find_record(token, **input_data)
            filemaker.logout(token)
            data = []
            data.append('all_students')

            try:
                total = get_record[0]['response']['dataInfo']['returnedCount']
            except KeyError:
                return render(request, 'data.html')            
            print("total=", total)
            for i in range(0, total):
                print('i=', i)
                record = get_record[0]['response']['data'][i]['fieldData']
                print(record)
                for key, value in record.items():
                    value = str(value)
                    individual.append(value)
                persons.append(individual[:])
                individual.clear()   
                  
            context = {'data':data, 'person':persons}    
            return render(request, 'data.html', context)
        if 'approval' in request.POST:
            #add something to check if 0 need approval
            data.append('all_students')
            get_record = filemaker.need_approval(token)
            if get_record['messages'][0]['code'] == '0':
                total = len(get_record['response']['data'])
                for i in range(total):
                    record = get_record['response']['data'][i]['fieldData']
                    for key, value in record.items():
                        value = str(value)
                        individual.append(value)
                    persons.append(individual[:])
                    individual.clear()                    
                context = {'data':data, 'person':persons}    
                return render(request, 'data.html', context)
            return render(request, 'data.html')
            
        if 'update' in request.POST:
            list = []
            get_records = filemaker.get_all(token)
            total = len(get_records['response']['data'])
            print("total= " + str(total))

            for i in range(total):
                check_box = request.POST.get(f'check_box{i}', None)
                print(check_box) 
                if check_box == 'on':
                    print('checkbox on')
                    for j in range((i*28),28+(i*28)):
                        # print(request.POST.get(f'data{j}', None))
                        # print('data' + str(j))
                        if request.POST.get(f'data{j}', None) == "":
                            list.append('Empty')
                        else:
                            list.append(request.POST.get(f'data{j}', None))

                    print(list)
                    scores = list[0]
                    testscheduled = list[1]
                    agree = list[2]
                    entrydate = list[3]
                    entrytime = list[4]
                    firstname = list[5]
                    lastname = list[6]
                    byuid = list[7]
                    netid = list[8]
                    email = list[9]
                    reason = list[10]
                    language = list[11]
                    languageother = list[12]
                    previousexperience = list[13]
                    major = list[14]
                    secondmajor = list[15]
                    minor = list[16]
                    cometocampus = list[17]
                    cannotcome = list[18]
                    testdate1 = list[19]
                    testdate2 = list[20]
                    time1 = list[21]
                    time2 = list[22]
                    time3 = list[23]
                    time4 = list[24]
                    confirmemail = list[25]
                    phone = list[26]
                    emailsent = list[27]
                    query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language, EntryDate=entrydate)
                    record_id = query[0]['response']['data'][0]['recordId']
                    filemaker.edit_all_fields(scores, testscheduled, agree, entrydate, entrytime, firstname, lastname, byuid, netid, email, reason, language, languageother,
                    previousexperience,major,secondmajor,minor,cometocampus,cannotcome,testdate1,testdate2,time1,time2,time3,time4, confirmemail,phone,emailsent, token, record_id)
                    list.clear()
        if 'create_record' in request.POST:
            create_student_record(request, token)
        if 'delete' in request.POST:
            list = []
            get_records = filemaker.get_all(token)
            total = len(get_records['response']['data'])
            print("total= " + str(total))

            for i in range(total):
                check_box = request.POST.get(f'check_box{i}', None)
                print(check_box) 
                if check_box == 'on':
                    print('checkbox on')
                    for j in range((i*28),28+(i*28)):
                        if request.POST.get(f'data{j}', None) == "":
                            list.append('Empty')
                        else:
                            list.append(request.POST.get(f'data{j}', None))

                    print(list)
                    #region
                    scores = list[0]
                    testscheduled = list[1]
                    agree = list[2]
                    entrydate = list[3]
                    entrytime = list[4]
                    firstname = list[5]
                    lastname = list[6]
                    byuid = list[7]
                    netid = list[8]
                    email = list[9]
                    reason = list[10]
                    language = list[11]
                    languageother = list[12]
                    previousexperience = list[13]
                    major = list[14]
                    secondmajor = list[15]
                    minor = list[16]
                    cometocampus = list[17]
                    cannotcome = list[18]
                    testdate1 = list[19]
                    testdate2 = list[20]
                    time1 = list[21]
                    time2 = list[22]
                    time3 = list[23]
                    time4 = list[24]
                    confirmemail = list[25]
                    phone = list[26]
                    emailsent = list[27]
                    #endregion
                    query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language)
                    record_id = query[0]['response']['data'][0]['recordId']
                    print(record_id)
                    delete_record = delete(request, record_id, token)
                    list.clear()
        data.append('all_students')
        get_record = filemaker.get_all(token)
        total = len(get_record['response']['data'])
        for i in range(total):
            record = get_record['response']['data'][i]['fieldData']
            for key, value in record.items():
                value = str(value)
                individual.append(value)
            persons.append(individual[:])
            individual.clear()                    
        context = {'data':data, 'person':persons} 
        return render(request, 'data.html', context)
    else:
        data.append('all_students')
        get_record = filemaker.need_approval(token)
        if get_record['messages'][0]['code'] == '0':
            total = len(get_record['response']['data'])
            for i in range(total):
                record = get_record['response']['data'][i]['fieldData']
                for key, value in record.items():
                    value = str(value)
                    individual.append(value)
                persons.append(individual[:])
                individual.clear()                    
            context = {'data':data, 'person':persons}    
            return render(request, 'data.html', context)
        return render(request, 'data.html')

@user_passes_test(lambda u: u.is_superuser)
def delete(request, record_id, token):
    filemaker.delete_record(record_id, token)

@user_passes_test(lambda u: u.is_superuser)
def create_student_record(request, token):
    now = datetime.now()

    sqldb_entry_date = date.today()

    entry_date = datetime.strftime(sqldb_entry_date, '%m-%d-%Y')
    entry_time = now.strftime("%H:%M:%S")
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    byuid = request.POST.get('byuid', None)
    netid = request.POST.get('netid', None)
    scores = None
    test_request = request.POST.get('test_request', None)
    approved = request.POST.get('approved', None)
    email_sent = request.POST.get('email_sent', None)
    reason = request.POST.get('reason', None)
    language = request.POST.get('language', None)
    language_other = request.POST.get('language_other', None)
    test_date1 = request.POST.get('test_date1', None)
    time1 = request.POST.get('time1', None)
    time2 = request.POST.get('time2', None)
    test_date2 = request.POST.get('test_date2', None)
    time3 = request.POST.get('time3', None)
    time4 = request.POST.get('time4', None)
    phone = request.POST.get('phone', None)
    experience = request.POST.get('experience', None)
    major = request.POST.get('major', None)
    second_major = request.POST.get('second_major', None)
    minor = request.POST.get('minor', None)
    come_to_campus = request.POST.get('come_to_campus', None)
    cannot_come = request.POST.get('cannot_come', None)
    email = netid + "@byu.edu"
    confirm_email = email
    scores = None

    sqldb_testdate1 = (request.POST.get('test_date1'))
    format_testdate1 = datetime.strptime(sqldb_testdate1, '%Y-%m-%d').date()
    testdate1 = datetime.strftime(format_testdate1, '%m-%d-%Y')
    
    sqldb_testdate2 = (request.POST.get('test_date2'))
    format_testdate2 = datetime.strptime(sqldb_testdate2, '%Y-%m-%d').date()
    testdate2 = datetime.strftime(format_testdate2, '%m-%d-%Y')

    record_id = filemaker.create_record(scores=scores, approved=approved, entry_date=entry_date, entry_time=entry_time, firstname=first_name, lastname=last_name, byuid=byuid,
                netid=netid, email=email, reason=reason, language=language, language_other=language_other, experience=experience, major=major, second_major=second_major, minor=minor, come_to_campus=come_to_campus,
                cannot_come=cannot_come, testdate1=testdate1, testdate2=testdate2, time1=time1, time2=time2, time3=time3, time4=time4, confirm_email=confirm_email, phone=phone, token=token)
    
def create_slats(request):
    if request.method == 'POST':
        form = SLATForm_Forms(request.POST)

        firstname = (request.POST.get('firstname', False))
        lastname = (request.POST.get('lastname', False))
        byu_id = (request.POST.get('byuid', False))
        language = (request.POST.get('language', False))

        initial_date = (request.POST.get('thesis'))
        format_initial = datetime.strptime(initial_date, '%Y-%m-%d').date()
        thesis_date = datetime.strftime(format_initial, '%m-%d-%Y')

        transcript = request.FILES['transcript']
        opi_rating = request.FILES['opi']

        # print(transcript.size)
        # print(transcript.name)

        client = box_api.create_client()
        FileSystemStorage(location="/tmp").save(transcript.name, transcript)
        FileSystemStorage(location="/tmp").save(opi_rating.name, opi_rating)
        box_api.create_pdf(full_name=firstname + " " + lastname, byu_id=byu_id, language=language, thesis=thesis_date)
        files = []
        files.append("/tmp/" + transcript.name)
        files.append("/tmp/" + opi_rating.name)
        files.append("/tmp/" + f"{firstname} {lastname} Information.pdf")

        slat_folder = '185240535599'
        box_api.upload_files(client=client, student_name=firstname + " " + lastname + "(" + byu_id + ")", files=files, slat_folder=slat_folder)
        return render(request, 'slats_receipt.html', {'form': form})
    else:
        form = SLATForm_Forms()

    return render(request, 'slats.html', {'form': form})

def slats_receipt(request):
    get_template('slats_receipt.html')
    return render(request, 'slats_receipt.html')

def opi_form(request):
    if request.method == 'POST':
        form = OPIForm_Forms(request.POST)

        google_calendar.main()

        valid = True
        now = datetime.now()

        #region contains all request values
        sqldb_entry_date = date.today()
        entry_date = datetime.strftime(sqldb_entry_date, '%m-%d-%Y')

        entry_time = now.strftime("%H:%M:%S")
        agree = bool(request.POST.get('agree'))
        firstname = (request.POST.get('firstname', False))
        lastname = (request.POST.get('lastname', False))
        byuid = (request.POST.get('byuid', False))
        print(f'Student {byuid} has attempted to to submit a test request.')
        netid = (request.POST.get('netid', False))
        email = (request.POST.get('email', False))
        reason = (request.POST.get('reason', False))
        print('This is a reason test-', reason)
        reason_other= (request.POST.get('reason_other', False))
        language = (request.POST.get('language', False))
        language_other = (request.POST.get('language_other', False))
        experience = (request.POST.get('experience', False))
        major = (request.POST.get('major', False))
        second_major= (request.POST.get('second_major', False))
        minor = (request.POST.get('minor', False))
        scores = 'None'
        come_to_campus = (request.POST.get('come_to_campus', False))
        cannot_come = (request.POST.get('cannot_come', False))
        time1 = (request.POST.get('time1'))
        time2 = (request.POST.get('time2'))
        time3 = (request.POST.get('time3'))
        time4 = (request.POST.get('time4'))
        confirm_email = (request.POST.get('confirm_email', False))
        phone = (request.POST.get('phone', False))
        
        finished_date = datetime.strptime(request.POST['testdate1'], '%Y-%m-%d')

        sqldb_testdate1 = (request.POST.get('testdate1'))
        format_testdate1 = datetime.strptime(sqldb_testdate1, '%Y-%m-%d').date()
        testdate1 = datetime.strftime(format_testdate1, '%m-%d-%Y')
        
        finished_date_2 = datetime.strptime(request.POST['testdate2'], '%Y-%m-%d')

        sqldb_testdate2 = (request.POST.get('testdate2'))
        format_testdate2 = datetime.strptime(sqldb_testdate2, '%Y-%m-%d').date()
        testdate2 = datetime.strftime(format_testdate2, '%m-%d-%Y')

        if finished_date.weekday() == 1:
            if time2 == '11:00':
                time2 = '10:30'
        if finished_date_2.weekday() == 1:
            if time4 == '11:00':
                time4 = '10:30'
        #endregion

        f = open(os.path.abspath("myapp/google_api/events.json"))
        data = json.load(f)
        k = 0
        for i in data:
            if testdate1 == data[k]['Date']:
                print(testdate1, i, 'first')
                response = JsonResponse({"error": "The testing center is closed on " + data[k]['Date']})
                response.status_code = 403
                valid == False
                return response
            if testdate2 == data[k]['Date']:
                print(testdate2, i, 'second')
                response = JsonResponse({"error": "The testing center is closed on " + data[k]['Date'] + '. Please schedule for a different day.'})
                response.status_code = 403
                valid == False
                return response
            k += 1

        token = byu_api.login()
        valid_student = byu_api.get_byuid(token, byuid, netid, valid)
        if language != "Other":
            valid_classes = byu_api.get_classes(token, byuid, language, valid, reason)
        logout = byu_api.logout(token)
        if (language == "Other" and valid_student == True) or (valid_student == True and valid == True and valid_classes == True):
            #new_OPIForm.save()
            token = filemaker.login()
            try:
                test = filemaker.find_record('BYUID', byuid, token)
                print(test['response']['data'][0]['fieldData']['Language'])
                if test['messages'][0]['code'] == '0':
                    if test['response']['data'][0]['fieldData']['Language'] in language:
                        response = JsonResponse({"error": "You have already submitted a test request for your requested language. If you would like to rescedule, please call or email the Center for Language Studies."})
                        response.status_code = 403
                        return response
            except KeyError:
                #this student is clear to submit a test request
                pass

            email = netid + '@byu.edu'
            confirm_email = email
            success = 'Sent for ' + firstname
            if language == 'Other':
                approved = 'No'
            elif '4' in reason or reason == 'Language Certificate':
                approved = 'Yes'
            else:
                approved = 'No'
            record_id = filemaker.create_record(scores, approved, entry_date, entry_time, firstname, lastname, byuid,
            netid, email, reason, language, language_other, experience, major, second_major, minor, come_to_campus,
            cannot_come, testdate1, testdate2, time1, time2, time3, time4, confirm_email, phone, token)
            filemaker.logout(token)

            #send slack message if applicable
            if reason == 'Individual Request' or \
            'FLAS' in reason or \
            'Study Abroad' in reason or \
            'CLS_Instructor' in reason or \
            'LaSER' in reason or \
            'MAPL' in reason or \
            'Research' in reason or \
            'Dual Immersion' in reason or \
            'Program Applicant' in reason or \
            'SLaT' in reason or \
            'LSR' in reason or \
            'Research' in reason or \
            language == 'Other': 
                if firstname == 'test' or firstname == 'Test' or lastname == 'Person' or lastname == 'person':
                    pass
                elif language == 'Other':
                    slack_str = f'A student requires your assistence. \nReason: Other Language \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)                    
                elif come_to_campus == 'No':
                    slack_str = f'A student cannot come to campus to take their OPI test and requires your attention. \nReason: {cannot_come} \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)
                else:
                    slack_str = f'A student has sent in an OPI request that requires your attention. \nReason: {reason} \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)

            return HttpResponse(success)
        else:
            print('it faileeeedddd')
            response = JsonResponse({"error":"There was an error submitting your request."})
            if not valid_student:
                response = JsonResponse({"error": "Your BYU student information is incorrect. Please verify your BYU ID and NET ID."})
            if not valid_classes:
                response = JsonResponse({"error": "You have not yet completed the required language courses to qualify for the OPI. Please verify your course selection. Additionally, students often put the incorrect reason for taking the test. For example, sometimes students enter 'Language Certificate', when really they should be putting their seminar class as the reason for taking the OPI test."})
            response.status_code = 403
            return response
    else:
        form = OPIForm_Forms()
    
    return render(request, 'opi_form.html', {'form': form})
