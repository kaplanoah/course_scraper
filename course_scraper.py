import urllib2
import os
import re
import sys
import time

from bs4 import BeautifulSoup

from secret import base_path
from utils import is_next_link, is_course_title, backup
from csv_file import CsvFile


harvard_course_catalog_url = "https://coursecatalog.harvard.edu/icb/icb.do?keyword=CourseCatalog&panel=icb.pagecontent695860%3Arsearch%3Fcontext%3D%244%26coreToolId%3D14346%26fq_coordinated_semester_yr%3D%26fq_school_nm%3D%26keyword%3DCourseCatalog%26pageContentId%3Dicb.pagecontent695860%26pageid%3Dicb.page335057%26permissions%3D7%252C8%26q%3D%26remoteAddr%3D4.35.92.19%26requestId%3D660063%26siteId%3Dicb.site69201%26siteType%3D12%26sort%3Dcourse_title%2Basc%26start%3D50%26submit%3DSearch%26topicId%3Dicb.topic749225%26urlRoot%3Dcourse%244.harvard.edu%26userid%3D--------&pageid=icb.page335057&pageContentId=icb.pagecontent695860&view=search&viewParam_context=catalog&viewParam_coreToolId=14346&viewParam_fq_coordinated_semester_yr=&viewParam_fq_school_nm=&viewParam_keyword=CourseCatalog&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_permissions=7%2C8&viewParam_q=&viewParam_remoteAddr=4.35.92.19&viewParam_requestId=660063&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_sort=course_title+asc&viewParam_start=25&viewParam_submit=Search&viewParam_topicId=icb.topic749225&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_userid=--------&viewParam_context=catalog&viewParam_userid=--------&viewParam_keyword=CourseCatalog&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_topicId=icb.topic749225&viewParam_coreToolId=14346&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_remoteAddr=4.35.92.19&viewParam_permissions=7%2C8&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_requestId=661979"

html_path = '%s/harvard_courses.html' % base_path
csv_path = '%s/harvard_courses.csv'   % base_path


def populate_html_file():

    backup(html_path)

    f_html = open(html_path, 'w')

    while harvard_course_catalog_url:

        opened_course_catalog = urllib2.urlopen(harvard_course_catalog_url)

        course_catalog_soup = BeautifulSoup(opened_course_catalog.read(), 'html.parser')

        for course_tag in course_catalog_soup.findAll(is_course_title):
            f_html.write('%s\n' % str(course_tag))

        next_link_tag = course_catalog_soup.find(is_next_link)

        harvard_course_catalog_url = next_link_tag.get('href') if next_link_tag else None

    f_html.close()


def populate_csv_file():

    backup(csv_path)

    f_csv = CsvFile(csv_path, 'w')

    seen_courses = set()

    course_tags_soup = BeautifulSoup(open(html_path), 'html.parser')

    for course_tag in course_tags_soup.findAll('a'):

        displayed_course_information = course_tag.contents[0]

        department_and_level_regex = '[A-Zx0-9 \.\-]+'

        if re.match('%s \- ' % department_and_level_regex, displayed_course_information):
            department_and_level, title = displayed_course_information.split(' - ', 1)
        elif re.search(' \- %s($|\s)' % department_and_level_regex, displayed_course_information):
            title, department_and_level = displayed_course_information.rsplit(' - ', 1)
        else:
            title, department_and_level = displayed_course_information, ''

        url = course_tag.get('href')

        if (title, department_and_level) not in seen_courses:
            f_csv.add_row(title, department_and_level, url)

        seen_courses.add((title, department_and_level))

    f_csv.close()


populate_html_file()
populate_csv_file()
