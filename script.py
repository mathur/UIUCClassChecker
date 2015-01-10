import cookielib
import mechanize
import getpass
import re
import time
from twilio.rest import TwilioRestClient
from twilio_accnt import SID, TOKEN, PHONE


def getWebPage(subj, crse, user, password):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    br.open(
        'https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1')
    br.select_form(nr=0)
    br.form['inputEnterpriseId'] = user
    br.form['password'] = password
    br.submit()

    br.open(
        'https://ui2web1.apps.uillinois.edu/BANPROD1/bwskfcls.p_sel_crse_search')
    br.select_form(nr=1)
    br.form['p_term'] = ['120151']
    br.open(br.form.click())

    forms = br.forms()
    forms.next()
    focus = forms.next()
    focus.set_value([subj], nr=13)

    page = ''
    br.open(focus.click(name='SUB_BTN'))
    for f in br.forms():
        if f.get_value(nr=0) == '120151' and f.get_value(
                name='SEL_CRSE') == str(crse):
            page = br.open(f.click()).read()
    return page


def parsePage(page):
    section_strings = page.split('<TR>')
    sections = [[elem1[22:-5] for elem1 in re.findall(
        '<TD CLASS=\"dddefault\">(?!<A HREF).*</TD>', elem)] for elem in section_strings]
    sections = [elem for elem in sections if elem != []]
    return sections


def calculateSpots(sections):
    section_dict = {}
    for section in sections:
        if '<ABBR' in section[0]:
            if section[3][1] in section_dict:
                section_dict[section[3][1]] += int(section[11])
            else:
                section_dict[section[3][1]] = int(section[11])
        else:
            if section[2][1] in section_dict:
                section_dict[section[2][1]] += int(section[10])
            else:
                section_dict[section[2][1]] = int(section[10])
    min_spots = 999999
    for key in section_dict:
        if section_dict[key] < min_spots:
            min_spots = section_dict[key]
    return min_spots


def notify(number, course_string):
    ACCOUNT_SID = SID
    AUTH_TOKEN = TOKEN

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
        to=number,
        from_=PHONE,
        body=course_string,
    )

username = raw_input('Enterprise Username: ')
password = getpass.getpass('AD Password: ')
course_name = raw_input('Course Subject (Subj): ')
course_number = raw_input('Course Number (Crse): ')
phone_number = raw_input('Your Phone Number: ')
time_interval = raw_input('Time Interval (min): ')

while True:
    page = getWebPage(course_name, course_number, username, password)
    sections = parsePage(page)
    spots = calculateSpots(sections)
    if spots > 0:
        notify(phone_number, 'Your course({0} {1}) has an open spot!'.format(
            course_name, course_number))
        break
    print 'Spots: {0}'.format(spots)
    min_time_interval = int(time_interval) * 60
    time.sleep(min_time_interval)
