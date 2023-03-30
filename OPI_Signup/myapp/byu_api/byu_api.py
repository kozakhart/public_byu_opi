#from msilib.schema import Error
from urllib import response
import requests
from requests.structures import CaseInsensitiveDict
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

def check_token():
    base_path = Path(__file__).parent
    file_path = (base_path / "../byu_api/byu_token.json").resolve()
    with open(file_path, "r") as json_token:
        json_token = json.load(json_token)
        token = json_token[0]['token']
    url = f'https://api.byu.edu:443/byuapi/students/v3/'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    response_API = requests.get(url, headers=headers, verify=False)
    print(response_API.status_code)
    if response_API.status_code == 200:
        return token
    else:
        return False

def login():
    BYU_PRODUCTION_ID = os.getenv('BYU_PRODUCTION_ID')
    BYU_PRODUCTION_SECRET = os.getenv('BYU_PRODUCTION_SECRET')
    check = check_token()
    if check:
        token = check
        print("token= " + token)
        return token
    base_path = Path(__file__).parent
    file_path = (base_path / "../byu_api/byu_token.json").resolve()

    url = 'https://api.byu.edu:443/token/'
    data = {'grant_type': 'client_credentials'}
    client_id = BYU_PRODUCTION_ID
    client_secret = BYU_PRODUCTION_SECRET
    print(client_id, client_secret)
    response_API = requests.post(url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret)).json()
    print(response_API)
    token = response_API['access_token']
    print(token)
    with open(file_path, "w") as outfile:
        list = []
        dic = {'token':token}
        list.append(dic)
        jsonString = json.dumps(list)
        outfile.write(jsonString)
        outfile.close()
    return token

def get_byuid(token, byu_id, net_id, valid):
    url = f'https://api.byu.edu:443/byuapi/students/v3/?byu_ids={byu_id}&field_sets=basic'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    response_API = requests.get(url, headers=headers, verify=False)
    response_json = response_API.json()
    print(response_API.status_code)
    if response_API.status_code == 200:
        api_net_id = response_json['values'][0]['basic']['net_id']['value']
        if api_net_id != net_id:
            valid = False
            return valid
        valid = True
    else:  
        print('byuid not valid')
        valid = False
        return valid
    return valid

def get_classes(token, byu_id, language, valid, reason):
    url = f'https://api.byu.edu:443/byuapi/students/v3/{byu_id}/enrolled_class_grades/'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    response_API = requests.get(url, headers=headers, verify=False).json()
    x = True
    counter = 0
    transcript = []
    dic = {}
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
        'Research' in reason: 
        #send notification to Mariah
        valid = True
        return valid
    while x == True:
        try:
            teaching_area = response_API['values'][counter]['teaching_area']['value']
            course_number = response_API['values'][counter]['course_number']['value']
            if reason != 'Language Certificate' and ((reason == teaching_area + ' ' + course_number) or (reason in (teaching_area + ' ' + course_number))):
                print(teaching_area + ' ' + course_number)
                print('student qualifies for seminar')
                valid = True
                return valid
            grade = response_API['values'][counter]['grade']['value']
            counter += 1

            print(teaching_area, course_number, grade)
            if teaching_area in language or teaching_area == 'SCAND' or teaching_area == 'ANTHR' or teaching_area == 'IHUM':
                dic = {'teaching_area': teaching_area, 'course_number': course_number, 'grade': grade}
                transcript.append(dic)
                split_reason = reason.split(" ")
                if teaching_area in reason and split_reason[1] in course_number:
                    print(teaching_area + ' ' + course_number)
                    valid = True
                    return valid
        except IndexError:
            x = False
        except KeyError:
            print('key')
            valid = False
            return valid
    base_path = Path(__file__).parent
    file_path = (base_path / "../byu_api/required_courses.json").resolve()
    print(transcript)
    if reason == 'Language Certificate':
        with open(file_path, "r") as required_courses:
            i = 0 
            required_courses = json.load(required_courses)

            # find correct course index
            while i <= 20:
                if language == required_courses[i]['Area']:
                    break
                i += 1

            lang_index = i
            req_lang = required_courses[lang_index]['Language']
            req_civ = required_courses[lang_index]['Civ/Culture']
            req_lit = required_courses[lang_index]['Literature']

            applicable_courses = []
            passed_reqs = 0

            for k in req_lang.values():
                for grade in transcript:
                    if grade['course_number'] in k:
                        applicable_courses.append(grade['course_number'])
                        passed_reqs += 1
            for k in req_civ.values():
                for grade in transcript:
                    if grade['course_number'] in k:
                        applicable_courses.append(grade['course_number'])
                        passed_reqs += 1
            for k in req_lit.values():
                for grade in transcript:
                    if grade['course_number'] in k:
                        applicable_courses.append(grade['course_number'])
                        passed_reqs += 1
            if passed_reqs >= 3:
                applicable_courses = list(set(applicable_courses))
                print(applicable_courses)
                if len(applicable_courses) >= 3:
                    valid = True
                else:
                    valid = False
            else:
                valid = False
    if reason != 'Language Certificate':
        valid = False
    print(valid)
    return valid

def logout(token):
    BYU_PRODUCTION_ID = os.getenv('BYU_PRODUCTION_ID')
    BYU_PRODUCTION_SECRET = os.getenv('BYU_PRODUCTION_SECRET')

    url = f'https://api.byu.edu:443/revoke/'
    data = {'token:': token}
    client_id = BYU_PRODUCTION_ID
    client_secret = BYU_PRODUCTION_SECRET
    response_API = requests.post(url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    if response_API.status_code == 200:
        print('Token successfully revoked')
        print(response_API.status_code)
    else:
        print('Token unsuccessfully revoked')

def get_byuid2(token, byu_id):
    url = f'https://api.byu.edu:443/byuapi/students/v3/{byu_id}/enrolled_class_grades/'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    response_API = requests.get(url, headers=headers, verify=False).json()

    x = True
    counter = 0
    transcript = []
    dic = {}
    while x == True:
        try:
            teaching_area = response_API['values'][counter]['teaching_area']['value']
            course_number = response_API['values'][counter]['course_number']['value']
            grade = response_API['values'][counter]['grade']['value']
            print(teaching_area, course_number, grade)
        except IndexError:
            print('index')
            x = False
        except KeyError:
            print('key')
            valid = False
            return valid
        counter += 1
    return response_API
