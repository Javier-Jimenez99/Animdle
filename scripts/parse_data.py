import json

import pandas as pd
import typer
from fuzzywuzzy import fuzz


def parse_at_data(anime_themes_json):
    animes_parsed = []
    anime_themes_parsed = []
    for anime in anime_themes_json:
        anime = anime.copy()
        if "animethemes" in anime.keys():
            for anime_theme in anime["animethemes"]:
                if len(anime_theme["animethemeentries"]) > 0:
                    at = {"type": anime_theme["type"], "id_theme": anime_theme["id"]}
                    at["id_anime"] = anime["id"]
                    if "song" in anime_theme.keys() and anime_theme["song"] is not None:
                        at["song"] = anime_theme["song"]["title"]
                    anime_theme_entry = anime_theme["animethemeentries"][0]
                    at["spoiler"] = anime_theme_entry["spoiler"]
                    at["nsfw"] = anime_theme_entry["nsfw"]

                    if (
                        "videos" in anime_theme_entry.keys()
                        and len(anime_theme_entry["videos"]) > 0
                    ):
                        video = anime_theme_entry["videos"][0]
                        at["video_link"] = video["link"]
                        at["video_resolution"] = video["resolution"]

                    anime_themes_parsed.append(at)

            anime.pop("animethemes")

        if "animesynonyms" in anime.keys():
            anime["synonyms"] = []
            for anime_synonym in anime["animesynonyms"]:
                anime["synonyms"].append(anime_synonym["text"])

            anime.pop("animesynonyms")

        anime["image"] = anime["images"][0]["link"]
        anime.pop("images")
        anime["id_anime"] = anime.pop("id")

        animes_parsed.append(anime)

    return animes_parsed, anime_themes_parsed


def max_ration_index(x, col):
    ratios = []
    for i in col:
        ratios.append(fuzz.ratio(x, i))

    return ratios.index(max(ratios))


def fuzzy_merge(row, df2):
    index = max_ration_index(row["title_parsed"], df2["title_parsed"])
    df2_row = df2.iloc[index]
    df2_row = df2_row.rename({"title_parsed": "title_matched", "title": "title_at"})

    row = row.rename({"title": "title_mal"})

    return pd.concat([row, df2_row], axis=0)


def merge_data(df_mal, df_at_animes):
    df_mal["title_parsed"] = df_mal["title"].str.lower()

    df_at_animes = df_at_animes.rename(columns={"name": "title"})
    df_at_animes["title_parsed"] = df_at_animes["title"].str.lower()

    # view final DataFrame
    df_merged = df_mal.merge(df_at_animes, on="title_parsed", suffixes=("_mal", "_at"))
    df_merged["title_matched"] = df_merged["title_parsed"]

    not_merged = df_mal[~df_mal["title_parsed"].isin(df_merged["title_parsed"])]

    fix_merge = not_merged.apply(lambda x: fuzzy_merge(x, df_at_animes), axis=1)

    df_merged = pd.concat([df_merged, fix_merge])
    df_anime_merged = df_merged.drop_duplicates(subset=["id_anime"], keep="first")

    return df_anime_merged


def select_animethemes(
    df_anime_themes,
    theme_type="OP",
    min_days_diff=5,
    max_days_diff=240,
    maximum_days=1080,
):
    anime_themes = df_anime_themes.copy()
    anime_themes = anime_themes[anime_themes["type"] == theme_type]
    anime_themes["used"] = False

    days = []
    for day in range(maximum_days):
        if day == 0:
            not_valid_animes = []
        else:
            not_valid_animes = days[-min(min_days_diff, len(days)) :]

        animes_themes_to_sample = anime_themes[
            ~anime_themes["id_anime"].isin(not_valid_animes) & ~anime_themes["used"]
        ]

        sampled_row = animes_themes_to_sample.sample(1)

        anime_themes.loc[sampled_row.index, "used"] = True
        days.append(sampled_row["id_theme"].values[0])

        if day > max_days_diff:
            id_theme = days[-max_days_diff]
            anime_themes.loc[anime_themes["id_theme"] == id_theme, "used"] = False

    return days


def main(
    path_mal_csv: str = typer.Argument(
        "./scripts/raw_data/myanimelist_data.json",
        help="Path to the My Anime List csv data",
    ),
    path_at_csv: str = typer.Argument(
        "./scripts/raw_data/animethemes_data.json",
        help="Path to the AnimetThemes csv data",
    ),
    path_out: str = typer.Argument(
        "./scripts/parsed_data", help="Path to the output folder"
    ),
    start_date: str = typer.Option(
        None,
        help="Start date of the challenge, if provided, it will be the current date",
    ),
):
    with open(path_at_csv, "r") as f:
        anime_themes_json = json.load(f)
    animes_parsed, anime_themes_parsed = parse_at_data(anime_themes_json)
    df_at_animes = pd.DataFrame(animes_parsed)
    df_anime_themes = pd.DataFrame(anime_themes_parsed)

    with open(path_mal_csv, "r") as f:
        my_anime_list = json.load(f)
    df_mal = (
        pd.DataFrame(my_anime_list)
        .sort_values("popularity_score", ascending=False)
        .head(500)
    )

    df_anime = merge_data(df_mal, df_at_animes)

    # Filter out anime themes that are not in the top 500
    df_anime_themes = df_anime_themes[
        df_anime_themes["id_anime"].isin(df_anime["id_anime"])
    ]

    df_anime["hardcore"] = df_anime["rank"] >= 200

    df_anime_easy = df_anime[~df_anime["hardcore"]]
    df_anime_hardcore = df_anime[df_anime["hardcore"]]

    df_anime_themes_easy = df_anime_themes[
        df_anime_themes["id_anime"].isin(df_anime_easy["id_anime"])
    ]

    df_anime_themes_hardcore = df_anime_themes[
        df_anime_themes["id_anime"].isin(df_anime_hardcore["id_anime"])
    ]

    sampled_easy_openings = select_animethemes(
        df_anime_themes_easy, theme_type="OP", min_days_diff=10
    )
    sampled_easy_endings = select_animethemes(
        df_anime_themes_easy, theme_type="ED", min_days_diff=10
    )

    sampled_hardcore_openings = select_animethemes(
        df_anime_themes_hardcore, theme_type="OP", min_days_diff=10
    )
    sampled_hardcore_endings = select_animethemes(
        df_anime_themes_hardcore, theme_type="ED", min_days_diff=10
    )

    dict_days = {
        "easy_openings": sampled_easy_openings,
        "hardcore_openings": sampled_hardcore_openings,
        "easy_endings": sampled_easy_endings,
        "hardcore_endings": sampled_hardcore_endings,
    }

    df_days = pd.DataFrame(dict_days)
    df_days.index.name = "id_day"
    df_days = df_days.reset_index()

    if start_date is None:
        start_date = pd.Timestamp.now()
    else:
        start_date = pd.Timestamp(start_date)

    start_date = start_date.floor("D")

    df_days["date"] = pd.date_range(start_date, periods=len(df_days), freq="D")

    df_days.to_csv(f"{path_out}/days.csv", index=False)

    df_anime.to_csv(f"{path_out}/animes.csv", index=False)

    df_anime_themes.to_csv(f"{path_out}/themes.csv", index=False)


if __name__ == "__main__":
    typer.run(main)
