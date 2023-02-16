import requests
from json import dump
from time import time, sleep
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

error = []

def fetch_ids(limit=-1):
    print("Downloading...")
    response = requests.get("http://typeracerdata.com/texts")
    print("... Done")

    print("Obtaining IDs...")
    soup = BeautifulSoup(response.text, "html.parser")
    text_ids = [int(str(a).split("id=")[1].split("\">")[0]) for a in soup.find_all("a", href=lambda x : x and x.startswith("/text?id=")) if a != None]
    print("... Done")

    if limit >= 0 and limit < len(text_ids):
        text_ids = text_ids[0:limit]
    
    return text_ids

def scraper(id, delay=6):
    response = requests.get("https://data.typeracer.com/pit/text_info?id={}".format(id))
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        text = soup.find("div", class_="fullTextStr").text
        origin = soup.find("div", class_="fullTextStr").next_sibling.next_sibling.text.split()
        _by_idx = origin.index("by")
        title = " ".join(origin[1:_by_idx - 1])
        _type = origin[_by_idx - 1]
        author = " ".join(origin[_by_idx + 1:len(origin)])
        print("Done for id:", id)
        return {"id" : id, "text" : text, "title" : title, "type" : _type, "author" : author, "len" : len(text)}
    except:
        print("Failure on id:", id, soup.text)
        error.append(id)
        sleep(delay)
        return scraper(id)

if __name__ == "__main__":
    text_ids = fetch_ids()

    tic = time()
    with ThreadPoolExecutor(max_workers=2) as p:
        data = list(p.map(scraper, text_ids))
    toc = time()
    
    data.sort(key=lambda _dict : _dict["len"])
    fp = open("texts.json", "w")
    dump(data, fp, separators=(",", ": "), indent=4)

    elapsed_sec = round(toc - tic, 1)
    elapsed_min = round(elapsed_sec / 60, 1)
    elapsed_hour = round(elapsed_min / 60, 1)
    txt_per_min = round(len(text_ids) / elapsed_min 
        if elapsed_min > 0 
        else 0.05, 1)
    txt_per_hour = round(txt_per_min * 60, 1)

    with open("log.txt", "w") as f:
        f.write(f"Fetched {len(text_ids)} texts in {elapsed_min} min | {elapsed_hour} h ({txt_per_min}/min | {txt_per_hour}/h)\n")
        f.write(f"Failed {len(error)} times (was fixed)")

    print(f"\nFetched {len(text_ids)} texts in {elapsed_sec} s | {elapsed_min} min | {elapsed_hour} h")
    print("See log.txt for more info")
