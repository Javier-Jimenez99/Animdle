import pandas as pd
import requests
import typer
from tqdm import tqdm

tqdm.pandas()


def authenticate(base_api_url, username, password):
    login_url = base_api_url + "api-token-auth/"

    response = requests.post(
        login_url,
        data={
            "username": username,
            "password": password,
        },
    )

    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception(response.content)


def post_request(row_data, url, auth_token):
    json_data = row_data.to_dict()
    response = requests.post(
        url,
        data=json_data,
        headers={
            # "Content-Type": "application/json",
            "Authorization": f"Token {auth_token}",
        },
    )
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise Exception(response.content)


def populate_anime(base_api_url, anime_data_path, auth_token):
    df_anime = pd.read_csv(anime_data_path)
    df_anime = df_anime.rename(
        columns={
            "id_anime": "id",
            "title_mal": "title",
            "image": "image_url",
        },
    )
    df_anime = df_anime.loc[
        :,
        [
            "id",
            "rank",
            "title",
            "popularity_score",
            "quality_score",
            "year",
            "season",
            "synopsis",
            "synonyms",
            "image_url",
            "hardcore",
        ],
    ]

    complete_url_api = base_api_url + "api/create-anime/"

    df_anime.progress_apply(
        post_request,
        axis=1,
        args=(complete_url_api, auth_token),
    )


def populate_theme(base_api_url, theme_data_path, auth_token):
    df_theme = pd.read_csv(theme_data_path)
    df_theme = df_theme.rename(
        columns={
            "id_theme": "id",
            "id_anime": "anime",
            "song": "title",
            "video_link": "video_url",
        },
    )
    df_theme = df_theme.loc[
        :,
        [
            "id",
            "anime",
            "title",
            "type",
            "spoiler",
            "nsfw",
            "video_url",
            "video_resolution",
        ],
    ]

    df_theme["anime"] = df_theme["anime"].astype(int)
    df_theme["video_resolution"] = df_theme["video_resolution"].astype(int)

    complete_url_api = base_api_url + "api/create-theme/"

    df_theme.progress_apply(post_request, axis=1, args=(complete_url_api, auth_token))


def populate_day(base_api_url, day_data_path, auth_token):
    df_day = pd.read_csv(day_data_path)
    df_day = df_day.rename(
        columns={
            "id_day": "id",
            "id_easy_opening": "easy_opening",
            "id_easy_ending": "easy_ending",
            "id_hardcore_opening": "hardcore_opening",
            "id_hardcore_ending": "hardcore_ending",
            "date": "date",
        },
    )
    df_day = df_day.loc[
        :,
        [
            "id",
            "easy_opening",
            "easy_ending",
            "hardcore_opening",
            "hardcore_ending",
            "date",
        ],
    ]

    df_day["easy_opening"] = df_day["easy_opening"].astype(int)
    df_day["easy_ending"] = df_day["easy_ending"].astype(int)
    df_day["hardcore_opening"] = df_day["hardcore_opening"].astype(int)
    df_day["hardcore_ending"] = df_day["hardcore_ending"].astype(int)

    complete_url_api = base_api_url + "api/create-day/"

    df_day.progress_apply(post_request, axis=1, args=(complete_url_api, auth_token))


def main(
    base_api_url: str = "http://localhost:8000/",
    username: str = "animdle",
    passwd: str = "S@l739567",
    anime_data_path: str = "scripts/parsed_data/animes.csv",
    theme_data_path: str = "scripts/parsed_data/themes.csv",
    day_data_path: str = "scripts/parsed_data/days.csv",
):
    if username is None:
        username = typer.prompt("Username")
    if passwd is None:
        passwd = typer.prompt("Password", hide_input=True)

    auth_token = authenticate(base_api_url, username, passwd)
    print("Authenticated successfully...")
    print("Populating animes table...")
    populate_anime(base_api_url, anime_data_path, auth_token=auth_token)
    print("Populating themes table...")
    populate_theme(base_api_url, theme_data_path, auth_token=auth_token)
    print("Populating days table...")
    populate_day(base_api_url, day_data_path, auth_token=auth_token)


if __name__ == "__main__":
    typer.run(main)
