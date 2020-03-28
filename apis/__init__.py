'''
# apis Module

    Set your own requests.Session via `apis.session = `
'''
from requests import Session
session = Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
})
# Update anti-scrapper agent
