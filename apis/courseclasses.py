'''
# CourseClasses Module

    Gets all classes with in the course
'''
from . import session
from bs4 import BeautifulSoup


def LoadClasses(course_url):
    '''
        Requires user to be logged in beforehand
        Loads all tasks in courses with bs4
    '''
    response = session.get(
        course_url
    )
    soup = BeautifulSoup(response.text, 'lxml')
    timeline = soup.find('div', {'class': 'timeline'})
    tasks = {}
    for units in timeline.find_all('div', {'class': 'units'}):
        title = units.find('h2').text.replace(
            '\n', ' ').replace('\t', '').strip()
        tasks[title] = []
        for subunits in units.find_all('div', {'class': 'leveltwo'}):
            chapter = subunits.find('span', {'class': 'chapterNumber'})
            article = subunits.find('span', {'class': 'articlename'})
            tasks[title].append({
                'chapter': chapter.text,
                'url': 'https://mooc1-1.chaoxing.com' + article.find('a').attrs['href'],
                'knowledge_url': ''.join([
                    'https://mooc1-1.chaoxing.com/knowledge/cards?',
                    article.find('a').attrs['href']
                        .replace('/mycourse/studentstudy?', '')
                        .replace('chapterId', 'knowledgeid')
                        .replace('courseId','courseid')
                ]),
                'title': article.find('a').attrs['title']
            })

    return tasks
