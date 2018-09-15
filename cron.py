import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
from collections import namedtuple
from soc import Soc
import time
import smtplib
import requests
from datetime import datetime


#Webreg doesn't run from 2:00am - 6:30am
d = datetime.now()
if d.hour in range(2, 6):
    exit()
elif d.hour is 6:
    if d.minute < 31:
        exit()


#Manually define the classes and sections in the lists below as strings.
Section = namedtuple('Section', ['number', 'index'])

MY_ADDRESS = os.environ.get('EMAIL_USER')
PASSWORD = os.environ.get('EMAIL_PASS')


#Define my_classes to be a dictionary with the course number being the key and the sections being the values
#Trying to switch to a different Intro to Ai section
#my_classes = { '440': ['02'],}
my_classes = {'133': ['94'],} #to test comment out real "my_classes" and check this class

soc = Soc()

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_mail(course_number):
    names, emails = get_contacts('/home/pi/SOC/mycontacts.txt') # read contacts
    message_template = read_template('/home/pi/SOC/message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.live.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(),COURSE_NUMBER=course_number)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Webreg-Script: Check the screenshot to see if you got in."

        # add the message body and screenshot to the email
        msg.attach(MIMEText(message, 'plain'))
        with open('screenshot.png', 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)
        # send the message via the server
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()


#Poll rutgers for open computer science courses and if they're open
#automagically register the user for the open class
def poll(subject, result=False):

    # get all the course data from SOC
    courses = soc.get_courses(subject)
    # build information about which courses/sections are currently open.
    open_indices = []
    if courses is not None:
        for course in courses:
            course_number = course['courseNumber']

            # remove leading zeroes
            if course_number.isdigit():
                course_number = str(int(course_number))

            #skip all courses not in list "my_classes"
            if course_number not in my_classes.keys():
                continue

            for section in course['sections']:
                section_number = section['number']
                if section_number.isdigit():
                    section_number = str(int(section_number))
                # section is open
                if section['openStatus']:
                    if section_number in my_classes[course_number]:
                        open_indices.append(section['index'])
                    else:
                        continue

        # This line is completely unnecessary but you shuold never delete beautiful list comprehensions
        #open_courses = [course for course, open_sections in iter(open_data.items()) if open_sections]

        #for debugging see app.py in sniper
        if result:
            return open_data

        if open_indices:
            print(open_indices)
            for index in open_indices:
                try:
                    options = Options()
                    options.add_argument('-headless')
                    driver = Firefox(firefox_options=options, executable_path='/usr/bin/firefox-esr')
                    print("HERE")
                    index_url = 'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection=92018&indexList=%s' % (index)
                    driver.get(index_url)
                    #time.sleep(1)

                    elem1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
                    elem1.send_keys(os.environ.get('WEBREG_USER'))
                    elem2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
                    elem2.send_keys(os.environ.get('WEBREG_PASS'))
                    elem2.send_keys(Keys.RETURN)

                    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'submit'))) 

                    button.click()
                    time.sleep(3)
                    driver.save_screenshot('screenshot.png')
                    send_mail(index_url)

                except Exception as e:
                    print(e)

            driver.quit()
            #https://developer.mozilla.org/en-US/Firefox/Headless_mode
            #https://blog.mozilla.org/fxtesteng/2012/07/12/how-to-webdriverwait/

# 198 - only care about CS classes
if __name__ == '__main__':
    poll(700)




