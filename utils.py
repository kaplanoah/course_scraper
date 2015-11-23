import time
import os

from shutil import copyfile
from secret import base_path


def is_next_link(tag):
    return (tag.name == 'a' and
           tag.parent.get('class') and
           'prevnext' in tag.parent.get('class') and
           'next' in tag.contents[0])

def is_course_title(tag):
    return (tag.name == 'a' and
           tag.parent.get('class') and
           'course_title' in tag.parent.get('class'))

def backup(path):
    backup_directory = '%s/backup' % base_path

    extention_dot_index = path.rfind('.')
    last_slash_index = path.rfind('/')

    backup_path = '%s%s_%s%s' % (
        backup_directory,
        path[last_slash_index:extention_dot_index],
        int(time.time()),
        path[extention_dot_index:]
    )

    copyfile(path, backup_path)