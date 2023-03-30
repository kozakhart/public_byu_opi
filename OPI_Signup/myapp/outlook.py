import win32com.client as win32
import csv
import requests
import time
from time import sleep
from datetime import datetime
import sys
import datefinder
import html
import myapp.filemaker_api.filemaker_api as filemaker


olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

def send_schedule(record_response):

    inbox = outlook.GetDefaultFolder(6).Folders("OPI Not Sent")
    donebox = outlook.GetDefaultFolder(6).Folders("OPI Sent")
    no_match = outlook.GetDefaultFolder(6).Folders("OPI Error")
    
    firstname = record_response['response']['data'][0]['fieldData']['FirstName']
    lastname = record_response['response']['data'][0]['fieldData']['LastName']
    language = record_response['response']['data'][0]['fieldData']['Language']
    testdate1 = record_response['response']['data'][0]['fieldData']['TestDate1']
    testdate2 = record_response['response']['data'][0]['fieldData']['TestDate2']
    email = record_response['response']['data'][0]['fieldData']['Email']


    format_testdate1 = datetime.strptime(testdate1, '%m/%d/%Y').date()
    testdate1 = datetime.strftime(format_testdate1, '%B %d, %Y')


    format_testdate2 = datetime.strptime(testdate2, '%m/%d/%Y').date()
    testdate2 = datetime.strftime(format_testdate2, '%B %d, %Y')

    messages = inbox.Items.Restrict("[Subject]='Test Schedule for {} {}'".format(firstname, lastname))          
    message = messages.Getfirst
    if message == None:
        message = messages.Getlast
    subject_content = message.Subject
    body_content = message.Body
    #convert both to strings
    subject_result = str(subject_content)
    body_result = str(body_content)
    if 'Monday' in body_result:
        start_index = body_result.index('Monday')
    elif 'Tuesday' in body_result:
        start_index = body_result.index('Tuesday')
    elif 'Wednesday' in body_result:
        start_index = body_result.index('Wednesday')
    elif 'Thursday' in body_result:
        start_index = body_result.index('Thursday')
    elif 'Friday' in body_result:
        start_index = body_result.index('Friday')
    elif 'Saturday' in body_result:
        start_index = body_result.index('Saturday') 

    date_string = body_result[start_index:start_index+60]
    print(date_string)
    subject_substr = 'Test Schedule for'
    if subject_substr in subject_result and firstname in body_result and lastname in body_result and language in body_result and (testdate1 in date_string or testdate2 in date_string): 
        mailItem = olApp.CreateItem(0)
        mailItem.Subject = 'OPI Test Date for {} {}'.format(firstname, lastname)
        #previously format 1
        mailItem.BodyFormat = 0
        
        matches = datefinder.find_dates(date_string)
        for match in matches:
            format_date = match.strftime('%B %d, %Y')
            format_time = match.strftime('%I:%M %p')

        mailItem.HTMLBody = """
        <HTML><BODY><p style="color:black;font-weight:normal;">{} {},<br><br>
        <span style="color:red; font-weight:bold;">PLEASE READ THE ENTIRE EMAIL</span><br><br>
        Your OPI has been scheduled for <mark style="color:red; font-weight:bold;">{} {} (Mountain Standard Time).</mark> Please arrive to <span style="color:red; font-weight:bold;">1141 JFSB</span> 5 to 10 minutes early. The HLC office (Humanities Learning Center) is located on the first floor of the JFSB in the north hallway. It may be helpful to set a reminder on your phone of this event as we may not notify you again before your test begins.<br><br>
        Remember that you can request the cancellation of your test up to <span style="color:red; font-weight:bold;">48 business hours</span> before this scheduled time (if you want to cancel a Monday or Tuesday test, you must let us know by the <span style="font-weight:bold;">Thursday</span> before). If you don’t cancel, fail to show up, or arrive late for the test, <span style="color:red; font-weight:bold;">you will be charged a no-show fee of US $60.</span> If you want to reschedule you MUST email us. Do NOT submit a second OPI signup form without notifying us or you will be charged $60.<br><br>
        As always, please remember that the HLC enforces the BYU Honor Code and its Dress and Grooming Standards. <span style="color:red; font-weight:bold;">Reminder to have access to your BYU ID.</span><br><br>
        Ratings for your test usually take about 2 weeks to be processed after completion of the test. <span style="font-weight:bold;">To receive your test scores, call or visit your respective <span style="color:red; font-weight:bold;">language department</span> or the Center for Language Studies.</span> We will then send you your scores through YMessage. We will <span style="color:red; font-weight:bold;">not</span> let you know when your rating is available; you will have to be proactive about contacting your language department or our office.<br><br>
        To receive your OPI, WPT, ALT, or ART scores, please reach out to your language department. Their information is listed below:<br><br>
        Spanish/Portuguese: 801-422-2837 or span-port@byu.edu<br>
        Japanese/Chinese/Korean/Arabic/Hebrew: 801-422-3396 or anel@byu.edu<br>
        French/Italian: 801-422-2209 or french_italian@byu.edu<br>
        German/Russian:  801-422-4923 or germ-list@byu.edu<br>
        All other languages: 801-422-1201 or cls@byu.edu<br><br> 
        Best,<br> 
        Eli J. Haun<br> 
        CLS Student Administrator<br> 
        Center for Language Studies<br> 
        cls.byu.edu<br> 
        </p></BODY></HTML>
        """.format(firstname, lastname, format_date, format_time)
        
        mailItem.To = f'<{email}>'
        mailItem.Sensitivity = 2
        mailItem.Send()
        message.Move(donebox)
        print('Message sent')
    else:
        message.Move(no_match)

def get_score(record_response):
    inbox = outlook.GetDefaultFolder(6).Folders("OPI Score")
    donebox = outlook.GetDefaultFolder(6).Folders("OPI Score Sent")
    messages = inbox.Items       
    message = messages.Getfirst
    if message == None:
        message = messages.Getlast
    subject_content = message.Subject
    editname = subject_content.split("Test Rating for ")
    fullname = editname[1]
    split_fullname = fullname.split(" ")
    firstname = split_fullname[0]
    lastname = split_fullname[1]