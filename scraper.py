import concurrent.futures
import logging

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}


def scrape_hackernews():
    url = "https://news.ycombinator.com/jobs"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for row in soup.find_all("tr", attrs={'class':'athing'}):
            print (row)
            a = row.find("a")
            print (a)
            if a and "item?id=" in a.get("href", ""):
                offers.append({
                    "Source": "HackerNews",
                    "Titre": a.text.strip(),
                    "Entreprise": "N/A",
                    "Lien": "https://news.ycombinator.com/" + a["href"]
                })
    except Exception as e:
        print("Erreur HackerNews:", e)
    return offers


# def scrape_python_jobs():
#     url = "https://www.python.org/jobs/"
#     offers = []
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.text, "lxml")
#         for job in soup.select(".list-recent-jobs li"):
#             title = job.h2.text.strip()
#             company = job.find("span", class_="listing-company-name").text.strip()
#             link = "https://www.python.org" + job.h2.a["href"]
#             offers.append({
#                 "Source": "Python.org",
#                 "Titre": title,
#                 "Entreprise": company,
#                 "Lien": link
#             })
#     except Exception as e:
#         print("Erreur Python.org:", e)
#     return offers
#
#
# def scrape_jsremotely():
#     url = "https://jsremotely.com/"
#     offers = []
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.text, "lxml")
#         for div in soup.find_all("div", class_="job"):
#             a = div.find("a")
#             if a:
#                 title = a.text.strip()
#                 link = "https://jsremotely.com" + a["href"]
#                 offers.append({
#                     "Source": "JSRemotely",
#                     "Titre": title,
#                     "Entreprise": "N/A",
#                     "Lien": link
#                 })
#     except Exception as e:
#         print("Erreur JSRemotely:", e)
#     return offers
#
#
# def scrape_remotive():
#     url = "https://remotive.io/api/remote-jobs?category=software-dev"
#     offers = []
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         jobs = res.json()["jobs"]
#         for job in jobs:
#             offers.append({
#                 "Source": "Remotive",
#                 "Titre": job["title"],
#                 "Entreprise": job["company_name"],
#                 "Lien": job["url"]
#             })
#     except Exception as e:
#         print("Erreur Remotive:", e)
#     return offers
#
#
# def scrape_workingnomads():
#     url = "https://www.workingnomads.com/jobs"
#     offers = []
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.text, "lxml")
#         for li in soup.select("div#jobsboard > a"):
#             title = li.find("h3")
#             company = li.find("h4")
#             if title and company:
#                 offers.append({
#                     "Source": "WorkingNomads",
#                     "Titre": title.text.strip(),
#                     "Entreprise": company.text.strip(),
#                     "Lien": "https://www.workingnomads.com" + li["href"]
#                 })
#     except Exception as e:
#         print("Erreur WorkingNomads:", e)
#     return offers
#
#
# def scrape_authenticjobs():
#     url = "https://authenticjobs.com/"
#     offers = []
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.text, "lxml")
#         for job in soup.select(".job-listing"):
#             title_tag = job.find("h4")
#             company_tag = job.find("h5")
#             a_tag = job.find("a", href=True)
#             if title_tag and a_tag:
#                 offers.append({
#                     "Source": "AuthenticJobs",
#                     "Titre": title_tag.text.strip(),
#                     "Entreprise": company_tag.text.strip() if company_tag else "N/A",
#                     "Lien": "https://authenticjobs.com" + a_tag["href"]
#                 })
#     except Exception as e:
#         print("Erreur AuthenticJobs:", e)
#     return offers


def main():
    print("Scraping multi-sources en cours...\n")

    all_offers = []
    scrapers = [scrape_hackernews]#, scrape_python_jobs, scrape_jsremotely, scrape_remotive, scrape_workingnomads, scrape_authenticjobs]

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(scrape_hackernews)
    #     executor.submit(scrape_python_jobs)
    #     executor.submit(scrape_jsremotely)
    #     executor.submit(scrape_remotive)
    #     executor.submit(scrape_workingnomads)
    #     executor.submit(scrape_authenticjobs)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        offers = [executor.submit(f) for f in scrapers]

        for offer in offers:
            #print(offer.result())
            data = offer.result()
            all_offers.extend(data)

    print(all_offers)
    # all_offers = []
    # all_offers += scrape_hackernews()
    # all_offers += scrape_python_jobs()
    # all_offers += scrape_jsremotely()
    # all_offers += scrape_remotive()
    # all_offers += scrape_workingnomads()
    # all_offers += scrape_authenticjobs()

    df = pd.DataFrame(all_offers)
    df.to_csv("Data/jobs.csv", index=False, encoding="utf-8")

    print(f"\nFichier jobs.csv généré avec {len(df)} offres d'emploi.")
    logging.INFO(f"\nFichier jobs.csv généré avec {len(df)} offres d'emploi.")

    if not df.empty:
        print(df.head(10))


main()