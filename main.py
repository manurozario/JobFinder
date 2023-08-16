from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

## UNCOMMNET IF YOU WANT TO INPUT YOUR OWN PARAMETERS BUT COMMENT OUT THE ARRAY BELOW##
# unfamiliar_skills = []
# print('Put some skills that you are not familiar with. Type x if none or done.')

# while True:
#     unfamiliar_skill = input('>').lower()
#     if unfamiliar_skill == 'x':
#         break
#     unfamiliar_skills.append(unfamiliar_skill)

# print(f'Filtering out {unfamiliar_skills}...')

unfamiliar_skills = ['api', 'hadoop']


def find_jobs():
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(f'job_updates.txt', 'a') as f:
        f.write(f'----Update Date and Time: {dt_string}----\n\n')

    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find(
                'h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.strip().lower()
            more_info = job.header.h2.a['href']
            check = 0
            for u_skill in unfamiliar_skills:
                if u_skill not in skills:
                    check = 1
                else:
                    check = 0
                    break

            if check == 1:
                with open(f'job_updates.txt', 'a') as f:
                    f.write(f'Company Name: {company_name.strip()}\n')
                    f.write(f'Requiered Skills: {skills.strip()}\n')
                    f.write(f'Link: {more_info}\n\n')
    print(f'File updated: job_updates.txt')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10  # adjust minutes here if desried
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
