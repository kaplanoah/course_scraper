def is_next_link(tag):
    return (tag.name == 'a' and
           tag.parent.get('class') and
           'prevnext' in tag.parent.get('class') and
           'next' in tag.contents[0])

def is_course_title(tag):
    return (tag.name == 'a' and
           tag.parent.get('class') and
           'course_title' in tag.parent.get('class'))
