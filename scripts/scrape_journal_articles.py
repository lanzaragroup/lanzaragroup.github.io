from bs4 import BeautifulSoup
import json
import requests
from collections import Counter
import re

URL = "http://research.physics.berkeley.edu/lanzara/publications.html"

def extract_year_from_tag(tag):
    try:
        if tag.name == "h4":
            return int(tag.text)

    except:
        pass

HARD_SKIP = {
    "energy excitations in graphite: ",
    "1132-1133",
}

def extract_publication(tag, year):
    desc = list(tag.descendants)

    if len(desc) <= 1:
        return None

    if tag.name != "p":
        return None

    title_tags = ["strong"]
    if year < 2007:
        title_tags = ["b", "font"]
    if year < 2001:
        title_tags = ["strong", "b"]
    if year < 2000:
        title_tags = ["span"]

    title = [d.text for d in desc if d.name in title_tags][0]
    authors = [str(d) for d in desc if d.name is None and Counter(str(d))[","] > 1]
    if not len(authors):
        authors = [str(d) for d in desc if "Lanzara" in str(d)]

    try:
        authors = authors[0]
    except:
        authors = ""

    authors = [re.sub("\s+", " ", a.strip()) for a in authors.split(",")]

    journal_info = tag.find("a")
    if journal_info:
        href = journal_info.get("href")
        journal_info = journal_info.text
    else:
        href = "#"
        journal_info = ""

    return {
        "title": re.sub("\s+", " ", title),
        "authors": authors,
        "year": year,
        "href": href,
        "journal": re.sub("\s+", " ", journal_info),
    }

if __name__ == "__main__":
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "lxml")
    center = soup.find(id="centerDoc")

    current_year = 2018

    papers = []
    for tag in list(center):
        if not tag.name:
            continue

        extracted_year = extract_year_from_tag(tag)
        if extracted_year:
            print(f"YEAR: {extracted_year}")
            current_year = extracted_year

        else:
            try:
                if [x for x in HARD_SKIP if x in str(tag)]:
                    print("Skipping")
                    continue

                pub = extract_publication(tag, current_year)
                if pub:
                    papers.append(pub)
            except Exception as e:
                print("\n\n")
                print(tag, current_year)
                continue

    with open("papers.json", "w+") as f:
        json.dump(papers, f, indent=2)
