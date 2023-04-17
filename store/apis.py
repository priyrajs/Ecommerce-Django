from moodle import Moodle
import json
from . models import Course, Customer, MoodleSiteInfo
import requests

urls = MoodleSiteInfo.objects.all()
for url in urls:
    siteUrl = url.mdlSite
    siteUrl += "webservice/rest/server.php"
    siteToken = url.mdlToken


def get_mdl_userid(email):
    payload = {
        "wstoken":siteToken,
        "moodlewsrestformat":"json", #just to get response as json
        "wsfunction":"core_user_get_users",
        "criteria[0][key]":"email",
        "criteria[0][value]":email,
        }
    print(payload)
    r=requests.post(siteUrl, params=payload)
    jsonRetObj = json.loads(r.text)
    mdl_user = jsonRetObj.get('users')
    if type(jsonRetObj) == dict :
        return mdl_user[0].get('id')
    else:
        return 0


def mdl_create_user(instance,course,enrol):
    print(instance.name)
    name = instance.name.split(" ")
    fname = name[0]
    lname = name[1]
    #print(instance.name,fname,lname)
    email = instance.email
    password = "test@3Esoft"
    mdl_user_id = 0
    if(len(fname) > 0 or len(lname) > 0 or len(email) > 0 or len(password) > 0):
        
        payload = {
            "wstoken":siteToken,
            "moodlewsrestformat":"json", #just to get response as json
            "wsfunction":"core_user_create_users",
            "users[0][username]":email,
            "users[0][password]":password,
            "users[0][firstname]":fname,
            "users[0][lastname]":lname,
            "users[0][email]":email,
            }
        print(payload)
        r=requests.post(siteUrl, params=payload)
        print(r.text)
        jsonRetObj = json.loads(r.text)
        # print(type(jsonRetObj))
        # print(jsonRetObj[0])
        # print(jsonRetObj[0].get('id'))
        if type(jsonRetObj) == list:
            mdl_user_id = jsonRetObj[0].get('id')
            print(email)
            print(mdl_user_id)
            if(enrol):
                mdl_enrol_user(course,mdl_user_id)
        else:
            debuInfo = jsonRetObj.get('debuginfo')
            if "Username already exists" in debuInfo or "Email already exists" in debuInfo:
                mdl_user_id = get_mdl_userid(email)
                if(enrol):
                    mdl_enrol_user(course,mdl_user_id)

        Customer.objects.filter(email=email).update(mdl_user_id=mdl_user_id)


def mdl_enrol_user(course,mdl_user_id):
    print(mdl_user_id)
    mdl_course_id = course.mdl_course
    payload = {
        "wstoken":siteToken,
        "moodlewsrestformat":"json", #just to get response as json
        "wsfunction":"enrol_manual_enrol_users",
        "enrolments[0][userid]":mdl_user_id,
        "enrolments[0][courseid]":mdl_course_id,
        "enrolments[0][roleid]":5,
        }
    print(siteUrl)
    print(siteToken)
    print(payload)
    r=requests.post(siteUrl, params=payload)
    print(r.text)
    # jsonRetObj = json.loads(r.text)
    # if type(jsonRetObj) == list:
    #     mdl_user_id = jsonRetObj[0].get('id')
    # else:
    #     debuInfo = jsonRetObj.get('debuginfo')
    #     if "Username already exists" in debuInfo or "Email already exists" in debuInfo:
    #         mdl_user_id = get_mdl_userid(email)
    # Customer.objects.filter(email=email).update(mdl_user_id=mdl_user_id)