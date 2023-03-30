#all imports below
from urllib import response
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import filemaker_api as filemaker
import os
import datetime
from dotenv import load_dotenv



load_dotenv()
    
LTI_USER = os.getenv('LTI_USER')
LTI_PASS = os.getenv('LTI_PASS')

def get_browser():
    global browser
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return browser

def login(browser):
    browser.get('https://tms.languagetesting.com/Clientsite/Home.aspx')
    time.sleep(1)
    browser.find_element("id", "txtLoginID").send_keys(LTI_USER)
    browser.find_element("id", "txtPassword").send_keys(LTI_PASS)
    browser.find_element("id", "btnLogin").click()
    time.sleep(2)


def schedule_opi(record_response):

    firstname = record_response['response']['data'][0]['fieldData']['FirstName']
    lastname = record_response['response']['data'][0]['fieldData']['LastName']
    byuid = record_response['response']['data'][0]['fieldData']['BYUID']
    email = 'cls@byu.edu'
    language = record_response['response']['data'][0]['fieldData']['Language']
    language_other = record_response['response']['data'][0]['fieldData']['LanguageOther']
    if language == 'Other':
        language = language_other
    reason = record_response['response']['data'][0]['fieldData']['Reason']
    major = record_response['response']['data'][0]['fieldData']['Major']
    secondmajor = record_response['response']['data'][0]['fieldData']['SecondMajor']
    minor = record_response['response']['data'][0]['fieldData']['Minor']
    background = record_response['response']['data'][0]['fieldData']['PreviousExperience']
    if 'Mission' in background:
        background = 'RM'
    elif 'University' in background:
        background = 'Univ'
    testdate1 = record_response['response']['data'][0]['fieldData']['TestDate1']
    format_testdate1 = str.replace(testdate1, '/','')
    time1 = record_response['response']['data'][0]['fieldData']['Time1']
    time1 = datetime.datetime.strptime(time1, '%H:%M:%S')
    time1 = datetime.datetime.strftime(time1, "%I:%M %p")

    time2 = record_response['response']['data'][0]['fieldData']['Time2']
    time2 = datetime.datetime.strptime(time2, '%H:%M:%S')
    time2= datetime.datetime.strftime(time2, "%I:%M %p")

    testdate2 = record_response['response']['data'][0]['fieldData']['TestDate2']
    format_testdate2 = str.replace(testdate2, '/','')
    time3 = record_response['response']['data'][0]['fieldData']['Time3']
    time3 = datetime.datetime.strptime(time3, '%H:%M:%S')
    time3= datetime.datetime.strftime(time3, "%I:%M %p")

    time4 = record_response['response']['data'][0]['fieldData']['Time4']
    time4 = datetime.datetime.strptime(time4, '%H:%M:%S')
    time4= datetime.datetime.strftime(time4, "%I:%M %p")

    browser.find_element("xpath", "//a[@title='Register an individual to take an assessment']").click()
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_rbgSelectTest_0']").click()
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_btnSelectTest']").click()
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_rbgProctored_0']").click()
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_control2']").send_keys('Lang_Cert')
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_control3']").send_keys('RM')

    if 'CHIN' in language:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlLanguage']").send_keys('MAND')
    else:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlLanguage']").send_keys(language)

    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtFirstName']").send_keys(firstname)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtLastName']").send_keys(lastname)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtCandidateID']").send_keys(byuid)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtEmail']").send_keys(email)
    try:
        browser.find_element("xpath", "/html[1]/body[1]/form[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/div[1]/div[1]/table[1]/tbody[1]/tr[4]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/div[1]/select[1]").send_keys(reason)
    except:
        pass

    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_1_2']").send_keys(background)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_1_3']").send_keys(major)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_1_5']").send_keys(secondmajor)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_1_4']").send_keys(minor)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_1_6']").send_keys(Keys.TAB)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtdtMatch']").send_keys(format_testdate1)
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlHour']").send_keys(time1)
    if '15' in time1:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes']").send_keys('15')
    elif '30' in time1:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes']").send_keys('30')
    elif '45' in time1:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes']").send_keys('45')
    if "PM" in time1:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlAMPM']").send_keys('PM')

    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToHour']").send_keys(time2)
    if '15' in time2:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes']").send_keys('15')
    elif '30' in time2:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes']").send_keys('30')
    elif '45' in time2:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes']").send_keys('45')
    if "PM" in time2:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToAMPM']").send_keys('PM')

    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlHour2']").send_keys(time3)
    if '15' in time3:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes2']").send_keys('15')
    elif '30' in time3:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes2']").send_keys('30')
    elif '45' in time3:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlMinutes2']").send_keys('45')
    if "PM" in time3:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlAMPM2']").send_keys('PM')


    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToHour2']").send_keys(time4)
    if '15' in time4:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes2']").send_keys('15')
    elif '30' in time4:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes2']").send_keys('30')
    elif '45' in time4:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToMinutes2']").send_keys('45')
    if "PM" in time4:
        browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToAMPM2']").send_keys('PM')
    
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToAMPM']").send_keys(Keys.TAB)
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_txtdtMatch2']").send_keys(format_testdate2)

    #delete below after time format
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_ddlToAMPM']").click()

    browser.find_element("xpath", "//input[@id='ctl00_cphMain_ctl07_1_rfRetestOPI_0_1']").click()
    browser.find_element("xpath", "//select[@id='ctl00_cphMain_ctl07_1_ddlCandTimeZone_0']").send_keys('(UTC-07:00) Mountain')
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_btnSubmit']").click()
    try:
        time.sleep(2)
        browser.find_element("xpath", "//input[@id='ctl00_cphMain_btnThreeHrContinue']").click()
    except:
        pass
    time.sleep(2)


all_done = False
token = filemaker.login()
valid = filemaker.needs_scheduling(token)[1]
if valid is False:
    print('works')
    import sys
    sys.exit('No tests to schedule')

get_browser()
login(browser)
while all_done == False:
    try:
        field_name = 'TestScheduled'

        record_response = filemaker.needs_scheduling(token)[0]
        print(record_response['response']['data'][0]['recordId'])
        if record_response == None:
            all_done = True
        schedule_opi(record_response)
        data = 'Yes'
        filemaker.edit_record(field_name, data, token, record_response['response']['data'][0]['recordId'])

    except KeyError:
        print('KeyError')
        break
browser.quit()
filemaker.logout(token)



def get_score(first_name, last_name, db_byuid, db_netid, db_language, testdate1, testdate2):
    time.sleep(2)
    _datetime = datetime.datetime.now()
    to_year = _datetime.year
    to_day = _datetime.day
    to_month = _datetime.month
    
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_txtFirstName']").clear()
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_txtFirstName']").send_keys(first_name)

    browser.find_element("xpath", "//input[@id='ctl00_cphMain_txtLastName']").clear()
    browser.find_element("xpath", "//input[@id='ctl00_cphMain_txtLastName']").send_keys(last_name)

    browser.find_element("id", "ctl00_cphMain_txtFromDate").clear()
    browser.find_element("id", "ctl00_cphMain_txtFromDate").send_keys("1/1/{}".format(to_year - 2))

    browser.find_element("id", "ctl00_cphMain_txtToDate").clear()
    browser.find_element("id", "ctl00_cphMain_txtToDate").send_keys("{}/{}/{}".format(to_day, to_month, to_year))

    browser.find_element("xpath", "//input[@id='ctl00_cphMain_btnSearch']").click()
    time.sleep(2)
    counter = 2
    tens_counter = 0

    opi_score = ''
    wpt_score = ''
    final_score = '/'

    while True:
        try:
            id = browser.find_element("id", "ctl00_cphMain_gvTestRatings_ctl{}{}_lblCandidate".format(tens_counter, counter))
            language = browser.find_element("id", "ctl00_cphMain_gvTestRatings_ctl{}{}_lblLanguage".format(tens_counter, counter))
            test_type = browser.find_element("id", "ctl00_cphMain_gvTestRatings_ctl{}{}_lblTestType".format(tens_counter, counter))
            score = browser.find_element("id", "ctl00_cphMain_gvTestRatings_ctl{}{}_lblRating".format(tens_counter, counter))
            lti_test_date = browser.find_element("id", "ctl00_cphMain_gvTestRatings_ctl{}{}_lblTestTime".format(tens_counter, counter))
            counter += 2
            if counter == 10:
                counter = 0
                tens_counter += 1
            # opi score
            if (str(db_byuid) in id.text or db_netid in id.text) and (lti_test_date.text == testdate1 or lti_test_date.text == testdate2) and ('OPI' in test_type.text):
                opi_score = score.text
                #print(id.text, language.text, test_type.text, score.text)
            # latest wpt score
            elif (str(db_byuid) in id.text or db_netid in id.text) and ('WPT' in test_type.text):
                wpt_score = score.text            

        except:
            final_score = opi_score.strip() + final_score.strip()
            final_score = final_score.strip() + wpt_score.strip()
            final_score.strip()
            return final_score

