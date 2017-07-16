from bs4 import BeautifulSoup
from requests import get
import subprocess
import os 

def get_search_page_9_torrent(search):
    search = search.replace(" ", "-")
    url = f"http://www.torrent9.cc/search_torrent/{search}.html"
    page = get(url)
    return page

def get_torrent_page(searchPage):
    soup = BeautifulSoup(searchPage.content, 'html.parser')
    td = soup.find_all('td')
    list_a = []
    list_lien = []
    for elem in td:
        lien = elem.find_all('a')
        list_a.append(lien)
    for elem in list_a:
        for sub_elem in elem:
            lien = sub_elem.get('href')
            list_lien.append(lien)
    return list_lien  

def filter_link(list_lien, filtre):
    list_filtrer = []
    for lien in list_lien:
        if filtre in lien:
            list_filtrer.append(lien)
    return list_filtrer 

def dl_lien_torrent(url_page):
    page = get(url_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    dowloads_links = soup.find_all('a', class_='download')
    for elem in dowloads_links:
        dowload_link = elem.get("href")
        if 'get_torrent' in dowload_link:
            return dowload_link 
    return 'Lien de telechargement non trouver'

def create_torrent_dl_text_file(list_lien):
    with open("lien_torrent", "w") as f:
        for elem in list_lien:
            f.write(elem + "\n")

def dl_with_aria2c(file_name):
    os.mkdir("dl")
    os.chdir("dl")
    command = f"aria2c -i ../{file_name}"
    subprocess.call(command, shell=True)

def main():
    pre_url = "http://www.torrent9.cc"
    list_dl = []
    p = get_search_page_9_torrent("American God")
    list_lien = get_torrent_page(p)
    list_lien = filter_link(list_lien, "vostfr")
    for lien in list_lien.reverse():
        list_dl.append(pre_url + dl_lien_torrent(pre_url + lien))
    create_torrent_dl_text_file(list_dl)
    dl_with_aria2c("lien_torrent")

if __name__ == "__main__":
    main()


