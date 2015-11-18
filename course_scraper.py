import urllib2
from bs4 import BeautifulSoup
import re
import sys

harvard_course_catalog_url = "https://coursecatalog.harvard.edu/icb/icb.do?keyword=CourseCatalog&panel=icb.pagecontent695860%3Arsearch%3Fcontext%3D%244%26coreToolId%3D14346%26fq_coordinated_semester_yr%3D%26fq_school_nm%3D%26keyword%3DCourseCatalog%26pageContentId%3Dicb.pagecontent695860%26pageid%3Dicb.page335057%26permissions%3D7%252C8%26q%3D%26remoteAddr%3D4.35.92.19%26requestId%3D660063%26siteId%3Dicb.site69201%26siteType%3D12%26sort%3Dcourse_title%2Basc%26start%3D50%26submit%3DSearch%26topicId%3Dicb.topic749225%26urlRoot%3Dcourse%244.harvard.edu%26userid%3D--------&pageid=icb.page335057&pageContentId=icb.pagecontent695860&view=search&viewParam_context=catalog&viewParam_coreToolId=14346&viewParam_fq_coordinated_semester_yr=&viewParam_fq_school_nm=&viewParam_keyword=CourseCatalog&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_permissions=7%2C8&viewParam_q=&viewParam_remoteAddr=4.35.92.19&viewParam_requestId=660063&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_sort=course_title+asc&viewParam_start=25&viewParam_submit=Search&viewParam_topicId=icb.topic749225&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_userid=--------&viewParam_context=catalog&viewParam_userid=--------&viewParam_keyword=CourseCatalog&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_topicId=icb.topic749225&viewParam_coreToolId=14346&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_remoteAddr=4.35.92.19&viewParam_permissions=7%2C8&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_requestId=661979"

csv_path = '%s/harvard_courses.csv' % sys.path[0]
delimiter = '|'

def is_next_link(tag):
    return (tag.name == 'a' and
           tag.parent.get('class') and
           'prevnext' in tag.parent.get('class') and
           'next' in tag.contents[0])

f = open(csv_path, 'w')

while harvard_course_catalog_url:

    opened_url = urllib2.urlopen(harvard_course_catalog_url)

    all_courses_soup = BeautifulSoup(opened_url.read(), 'html.parser')

    courses = [a for a in all_courses_soup.findAll('a') if
        (a.parent.get('class') and 'course_title' in a.parent.get('class'))]

    for course in courses:

        displayed_course_information = course.contents[0]

        try:
            department_and_level, title = displayed_course_information.split(' - ', 1)
        except ValueError as e:
            if 'need more than 1 value to unpack' not in e.message:
                raise e
            department_and_level, title = '', displayed_course_information

        assert delimiter not in title

        url = course.get('href')

        f.write(title                + delimiter)
        f.write(department_and_level + delimiter)
        f.write(url                  + '\n')

    next_link_tag = all_courses_soup.find(is_next_link)

    harvard_course_catalog_url = next_link_tag.get('href') if next_link_tag else None

f.close()

