from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=')
soup = BeautifulSoup(html_text.text, 'lxml')
job = soup.find('li', class_='clearfix job-bx wht-shd-bx')
company_name = soup.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
skills = soup.find('span', class_ = 'srp-skills').text.replace(' ', '')

print('Company Name: ' + skills, end='')
print(', Required Skills: ' + skills)
