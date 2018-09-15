from collections import namedtuple
from fake_useragent import UserAgent
import requests
from datetime import datetime
import time

class Soc:
    """ Communicates with Rutgers SOC """
    def __init__(self, campus='NB', semester='92018', level='U'):
        """ We always use certain parameters"""
        self.base_url = 'http://sis.rutgers.edu/oldsoc'
        self.params = {
            'campus': campus,
            'semester': semester,
            'level': level,
        }

        # Spoof the user agent for good measure
        #ua = UserAgent() str(ua.random)

	#Found out spoofing an api is a bad idea. Its an api its there for a reason.
	#Allowing rutgers to fingerprint non-randomized User-Agent and IP address lets 
        #RU security/load-balancer know you're not malicious. 
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        #https://github.com/oss/socindex
    # url = 'http://sis.rutgers.edu/soc/courses.json?subject=198&semester=92018&campus=NB&level=U'
    # r = requests.get(url, headers=header) 
    # if r.status_code == requests.codes.ok:
    #     courses = r.json()
    # else:
    #     raise Exception ('You made an invalid request %s: %s' % (r.status_code, r.text))
    def query(self, resource, params):
        """Queries the given resource (a string) with the given parameters.
        For example self.query('/api/subjects.json', { 'keyword': 'Computer Science' })"""
        params.update(self.params)
        try:
            r = requests.get(self.base_url + resource, params=params, headers=self.headers) #to enable loop indent this line 4 spaces and uncomment everything else

            if r.status_code == requests.codes.ok:
                print("SUCCESS - Date/Time: " + str(datetime.now()) + " ---  Status code: "+ str(r.status_code))
                return r.json()
            else:
                print("\nFAILURE - Date/Time: " + str(datetime.now()) + " ---  Status code: "+ str(r.status_code) + " ---  Message:  "+str(r.text) + "\n")
        except Exception as e: 
            print("\n")
            print(e)
            print("\n")

    def get_subjects(self, **kwargs):
        """ Gives you a list of subjects (departments) """
        return self.query('/subjects.json?', params=kwargs)

    def get_courses(self, subject):
        """ Gives you a list of courses in a department """
        return self.query('/courses.json?', params={'subject': subject})
