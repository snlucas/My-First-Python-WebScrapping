from bs4 import BeautifulSoup

with open('index.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    skills = soup.find_all('div', class_='skills')

    for skill in skills:
        print(skill.h3.text)
