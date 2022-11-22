
from bs4 import BeautifulSoup
from extractor.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(f"{base_url}{keyword}")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})

    if pagination == None:
        return 1

    all_pages = pagination.select("div button")
    pages_from2 = pagination.select("div a")
    all_pages = all_pages + pages_from2

    count = len(all_pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print(final_url)
        driver.get(final_url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        
        for job in jobs:
            zone = job.find("div", class_='mosaic-zone')
            if zone == None:
                anchor = job.select_one("h2 a")
                position = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                region = job.find("div", class_="companyLocation")

                job_data = {
                    "link": f'https://kr.indeed.com{link}'.replace(",", " "),
                    "company": company.string.replace(",", " "),
                    "region": region.string.replace(",", " "),
                    "position": position.replace(",", " ")
                }
                results.append(job_data)
    return results