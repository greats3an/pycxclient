'''
# StudentCourses Module

    Gets the students' courses from the staticly generated webpage
'''
from .. import session
from bs4 import BeautifulSoup
import logging

def LoadCourses() -> list:
    '''
        Requires user to be logged in beforehand
        Loads all courses with `bs4`,retruns them in a `list` of `dict`
    '''
    logging.debug('Loading all courses of user %s' % session.cookies.get('uname'))
    response = session.get(
        'http://mooc1-1.chaoxing.com/visit/interaction'
    )    
    soup = BeautifulSoup(response.text, 'lxml')
    courses_ul = soup.find_all('div', {'class': 'ulDiv'})[0].find_all('ul')[0]
    courses = []
    for course in courses_ul.find_all('li'):
        cover = course.find('div', {'class': 'Mcon1img'})
        info = course.find('div', {'class': 'Mconright'})
        if not (cover and info):
            continue
        cover = cover.find('a')
        courses.append({
            'title':info.find('h3').find('a').attrs['title'],
            'url': 'http://mooc1-1.chaoxing.com' + cover.attrs['href'],
            'coverimage': cover.find('img').attrs['src'],
            'description': [
                p.text.strip() for p in info.find_all('p') if p.text.strip()
            ]
        })
    return courses
