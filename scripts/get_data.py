import requests
import json
import typer
import bs4
import time
import os

def get_animethemes_data():
    start_url = "https://api.animethemes.moe/anime?include=animethemes.animethemeentries.videos,animesynonyms,animethemes.song,images&page%5Bsize%5D=100"
    animes_data = []
    while start_url is not None:
        response = requests.get(start_url).json()
        animes_data.extend(response["anime"])

        json.dump(animes_data, open("scripts/raw_data/animethemes_data.json", "w"))
        start_url = response["links"]["next"]

    return animes_data

def get_myanimelist_data():
    base_url = "https://myanimelist.net/topanime.php"
    start_url = f"{base_url}?type=bypopularity"

    if os.path.exists("scripts/raw_data/myanimelist_data.json"):
        anime_data = json.load(open("scripts/raw_data/myanimelist_data.json"))

        rankings = [anime["rank"] for anime in anime_data]
        index = max(rankings)
        start_url += f"&limit={index}"
    else:
        index = 0
        anime_data = []

    
    while start_url is not None:
        table = None
        while table is None:
            response = requests.get(start_url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", {"class": "top-ranking-table"})
            if table is None:
                print(f"Error getting table in {start_url}")
                time.sleep(60)
            

        rows = table.find_all("tr", {"class": "ranking-list"})

        for row in rows:
            anime = {}
            anime["rank"] = int(row.find("td", {"class": "rank"}).text.strip())
            anime["title"] = row.find("div", {"class": "di-ib clearfix"}).text.strip()
            anime["popularity_score"] = float(row.find("div", {"class": "information di-ib mt4"}).text.strip().split("\n")[-1].replace("members", "").replace(",","").strip())
            quiality_score = row.find("td", {"class": "score ac fs14"}).text.strip()
            anime["quality_score"] = None if quiality_score == "N/A" else float(quiality_score)
            anime_data.append(anime)

        json.dump(anime_data, open("scripts/raw_data/myanimelist_data.json", "w"))

        start_url = base_url + soup.find("a", {"class": "link-blue-box next"}).attrs["href"]
        index += 50
        print(f"Saved {index} animes from myanimelist.net")



def get_main_anime_data():
    my_anime_list_data = get_myanimelist_data()
    print(f"Saved {len(my_anime_list_data)} animes from myanimelist.net")
    animes_data = get_animethemes_data()
    print(f"Saved {len(animes_data)} animes from animethemes.moe")

if __name__ == "__main__":
    typer.run(get_main_anime_data)