from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?&term="

    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Cant request Website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchor = post.find_all('a')[1]
                link = anchor['href']
                company, kind, region = anchor.find_all(
                    'span', class_="company")
                position = anchor.find('span', class_='title')
                job_data = {
                    "link": f"http://weworkremotely.com{link}".replace(",", " "),
                    "company": company.string.replace(",", " "),
                    "region": region.string.replace(",", " "),
                    "position": position.string.replace(",", " ")
                }
                results.append(job_data)
        return results

