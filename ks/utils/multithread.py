'''
https://stackoverflow.com/questions/25373167/multithreading-in-python-beautifulsoup-scraping-doesnt-speed-up-at-all
'''
import urllib2
import csv
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

def crawlToCSV(URLrecord):
    OpenSomeSiteURL = urllib2.urlopen(URLrecord)
    Soup_SomeSite = BeautifulSoup(OpenSomeSiteURL, "lxml")
    OpenSomeSiteURL.close()

    tbodyTags = Soup_SomeSite.find("tbody")
    trTags = tbodyTags.find_all("tr", class_="result-item ")

    placeHolder = []

    for trTag in trTags:
        tdTags = trTag.find("td", class_="result-value")
        tdTags_string = tdTags.string
        placeHolder.append(tdTags_string)

    return placeHolder


if __name__ == "__main__":
    fileName = "SomeSiteValidURLs.csv"
    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
    with open(FileName, "rb") as f:
        results = pool.map(crawlToCSV, f)  # results is a list of all the placeHolder lists returned from each call to crawlToCSV
    with open("Output.csv", "ab") as f:
        writeFile = csv.writer(f)
        for result in results:
            writeFile.writerow(result)