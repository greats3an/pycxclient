'''
# StudentCourses Module

    Gets the students' courses from the staticly generated webpage
'''
from . import session
from bs4 import BeautifulSoup


def LoadCourses():
    '''
        Requires user to be logged in beforehand
        Loads all courses with bs4
    '''
    response = session.get(
        'http://mooc1-1.chaoxing.com/visit/interaction'
    )
    soup = BeautifulSoup(response.text, 'lxml')
    courses_ul = soup.find_all('div', {'class': 'ulDiv'})[0].find_all('ul')[0]
    courses = []
    for course in courses_ul.find_all('li'):
        cover = course.find('div', {'class': 'Mcon1img'})
        description = course.find('div', {'class': 'Mconright'})
        if not (cover and description):
            continue
        cover = cover.find('a')
        courses.append({
            'url': 'http://mooc1-1.chaoxing.com' + cover.attrs['href'],
            'coverimage': cover.find('img').attrs['src'],
            'description': '\n'.join([
                p.text.strip() for p in description.find_all('p') if p.text.strip()
            ])
        })
    return courses
