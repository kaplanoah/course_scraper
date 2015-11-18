import urllib2
from bs4 import BeautifulSoup
import re
from secret import harvard_course_catalog_url

opened_url = urllib2.urlopen(harvard_course_catalog_url)

all_courses_soup = BeautifulSoup(opened_url.read(), 'html.parser')

courses = [a for a in all_courses_soup.findAll('a') if
    (a.parent.get('class') and 'course_title' in a.parent.get('class'))]

for course in courses:

    department_and_level, title = course.contents[0].split(' - ')
    url = course.get('href')

    print title
    print department_and_level
    print url