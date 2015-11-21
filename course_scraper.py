import urllib2
from bs4 import BeautifulSoup
from utils import is_next_link, is_course_title
import re
import sys
from csv_file import CsvFile

harvard_course_catalog_url = "https://coursecatalog.harvard.edu/icb/icb.do?keyword=CourseCatalog&panel=icb.pagecontent695860%3Arsearch%3Fcontext%3D%244%26coreToolId%3D14346%26fq_coordinated_semester_yr%3D%26fq_school_nm%3D%26keyword%3DCourseCatalog%26pageContentId%3Dicb.pagecontent695860%26pageid%3Dicb.page335057%26permissions%3D7%252C8%26q%3D%26remoteAddr%3D4.35.92.19%26requestId%3D660063%26siteId%3Dicb.site69201%26siteType%3D12%26sort%3Dcourse_title%2Basc%26start%3D50%26submit%3DSearch%26topicId%3Dicb.topic749225%26urlRoot%3Dcourse%244.harvard.edu%26userid%3D--------&pageid=icb.page335057&pageContentId=icb.pagecontent695860&view=search&viewParam_context=catalog&viewParam_coreToolId=14346&viewParam_fq_coordinated_semester_yr=&viewParam_fq_school_nm=&viewParam_keyword=CourseCatalog&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_permissions=7%2C8&viewParam_q=&viewParam_remoteAddr=4.35.92.19&viewParam_requestId=660063&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_sort=course_title+asc&viewParam_start=25&viewParam_submit=Search&viewParam_topicId=icb.topic749225&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_userid=--------&viewParam_context=catalog&viewParam_userid=--------&viewParam_keyword=CourseCatalog&viewParam_siteId=icb.site69201&viewParam_siteType=12&viewParam_topicId=icb.topic749225&viewParam_coreToolId=14346&viewParam_urlRoot=coursecatalog.harvard.edu&viewParam_remoteAddr=4.35.92.19&viewParam_permissions=7%2C8&viewParam_pageContentId=icb.pagecontent695860&viewParam_pageid=icb.page335057&viewParam_requestId=661979"

csv_path = '%s/harvard_courses.csv' % sys.path[0]

f = CsvFile(csv_path, 'w')

while harvard_course_catalog_url:

    opened_url = urllib2.urlopen(harvard_course_catalog_url)

    all_courses_soup = BeautifulSoup(opened_url.read(), 'html.parser')

    courses = all_courses_soup.findAll(is_course_title)

    for course in courses:

        displayed_course_information = course.contents[0]

        has_department_and_level = re.match('[A-Z0-9. ]+ - ?', displayed_course_information)

        if has_department_and_level:
            department_and_level, title = displayed_course_information.split(' - ', 1)
        else:
            department_and_level, title = '', displayed_course_information

        url = course.get('href')

        f.add_row(title, department_and_level, url)

    next_link_tag = all_courses_soup.find(is_next_link)

    harvard_course_catalog_url = next_link_tag.get('href') if next_link_tag else None

f.close()
