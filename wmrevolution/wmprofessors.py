import requests
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

RMPROFESSOR_URL = u'http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=269&pageNo='
EVEN_PROFESSORS = u'entry even vertical-center'
ODD_PROFESSORS = u'entry odd vertical-center'
LAST_PAGE = 57

PROFESSOR_FIELDS = [
    u'profName',
    u'profDept',
    u'profRatings',
    u'profAvg',
    u'profEasy',
    u'profHot'
]


def grab_professors(last_page=LAST_PAGE):

    professors = []
    for page_number in xrange(1, last_page):
        soup = BeautifulSoup(_grab_html(page_number))

        professors += map(_grab_professor,
                          soup.find_all(u'div', {u'class': EVEN_PROFESSORS}))
        professors += map(_grab_professor,
                          soup.find_all(u'div', {u'class': ODD_PROFESSORS}))
    return professors


def _grab_html(page_number):
    try:
        page = requests.get(RMPROFESSOR_URL + unicode(page_number))
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        # http request to course list page failed
        raise BadRequestError(
            unicode(page.status_code) + u"can't access page number" + unicode(page_number))
    return page.text


def _grab_professor(professor_data):
    fields = professor_data.find_all(u'div', {u'class': PROFESSOR_FIELDS})
    href = fields[0].a[u'href']
    fields = map(lambda f: f.string.strip(), fields)
    professor = dict(zip(PROFESSOR_FIELDS, fields))
    professor[u'href'] = href
    return professor
