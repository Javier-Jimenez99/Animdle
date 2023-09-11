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
    df_anime_themes_easy,
    df_anime_themes_hardcore,
    date_start=None,
    min_days_diff=10,
    max_days_diff=240,
    maximum_days=1080,
):
    df_anime_themes_easy["used"] = False
    df_anime_themes_hardcore["used"] = False

    df_ed_easy = df_anime_themes_easy[df_anime_themes_easy["type"] == "ED"]
    df_ed_hardcore = df_anime_themes_hardcore[df_anime_themes_hardcore["type"] == "ED"]

    df_op_easy = df_anime_themes_easy[df_anime_themes_easy["type"] == "OP"]
    df_op_hardcore = df_anime_themes_hardcore[df_anime_themes_hardcore["type"] == "OP"]

    days = []
    used_animes = []
    for day in range(maximum_days):
        if day == 0:
            not_valid_animes = []
        else:
            not_valid_animes = used_animes[-4 * min_days_diff :]

        day_row = {}
        for name, df in {
            "easy_endings": df_ed_easy,
            "hardcore_endings": df_ed_hardcore,
            "easy_openings": df_op_easy,
            "hardcore_openings": df_op_hardcore,
        }.items():
            animes_themes_to_sample = df[
                ~df["id_anime"].isin(not_valid_animes) & ~df["used"]
            ]

            sampled_row = animes_themes_to_sample.sample(1)

            df.loc[sampled_row.index, "used"] = True

            day_row[name] = sampled_row["id_theme"].values[0]

            used_animes.append(sampled_row["id_anime"].values[0])

            if day > max_days_diff:
                id_theme = days[-max_days_diff][name]
                df.loc[df["id_theme"] == id_theme, "used"] = False

        days.append(day_row)

    df_days = pd.DataFrame(days)
    df_days.index.name = "id_day"
    df_days = df_days.reset_index()

    if date_start is None:
        date_start = pd.Timestamp.now()
    else:
        date_start = pd.Timestamp(date_start)

    date_start = date_start.floor("D")

    df_days["date"] = pd.date_range(date_start, periods=len(df_days), freq="D")

    return df_days


def test_data(df_anime, df_theme, df_day):
    assert (
        len(df_anime) == df_anime["id_anime"].nunique()
    ), "There are duplicated anime ids"
    assert (
        len(df_theme) == df_theme["id_theme"].nunique()
    ), "There are duplicated theme ids"
    assert len(df_day) == df_day["id_day"].nunique(), "There are duplicated day ids"

    assert (
        df_theme["id_anime"].isin(df_anime["id_anime"]).all()
    ), "There are themes that are not in the animes"

    assert (
        df_day["easy_openings"].isin(df_theme["id_theme"]).all()
    ), "There are easy openings that are not in the themes"
    assert (
        df_day["easy_endings"].isin(df_theme["id_theme"]).all()
    ), "There are easy endings that are not in the themes"
    assert (
        df_day["hardcore_openings"].isin(df_theme["id_theme"]).all()
    ), "There are hardcore openings that are not in the themes"
    assert (
        df_day["hardcore_endings"].isin(df_theme["id_theme"]).all()
    ), "There are hardcore endings that are not in the themes"


def animes_to_json(df_anime, save_path):
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

    df_anime["created_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    df_anime["updated_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    df_anime["synonyms"] = df_anime["synonyms"].astype(str).fillna("[]")
    df_anime["synopsis"] = df_anime["synopsis"].fillna("")

    dict_animes = df_anime.to_dict(orient="records")

    dict_result = []
    for anime in dict_animes:
        dict_result.append({"model": "api.anime", "pk": anime["id"], "fields": anime})

    with open(save_path, "w") as f:
        json.dump(dict_result, f, indent=4)


def themes_to_json(df_theme, save_path):
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
    df_theme["created_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    df_theme["updated_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    dict_themes = df_theme.to_dict(orient="records")

    dict_result = []
    for theme in dict_themes:
        dict_result.append({"model": "api.theme", "pk": theme["id"], "fields": theme})

    with open(save_path, "w") as f:
        json.dump(dict_result, f, indent=4)


def days_to_json(df_day, save_path):
    df_day = df_day.rename(
        columns={
            "id_day": "id",
            "easy_openings": "opening",
            "easy_endings": "ending",
            "hardcore_openings": "hardcore_opening",
            "hardcore_endings": "hardcore_ending",
            "date": "date",
        },
    )

    df_day["opening"] = df_day["opening"].astype(int)
    df_day["ending"] = df_day["ending"].astype(int)
    df_day["hardcore_opening"] = df_day["hardcore_opening"].astype(int)
    df_day["hardcore_ending"] = df_day["hardcore_ending"].astype(int)
    df_day["date"] = df_day["date"].dt.strftime("%Y-%m-%d")
    df_day["created_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    df_day["updated_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    dict_days = df_day.to_dict(orient="records")

    dict_result = []
    for day in dict_days:
        dict_result.append({"model": "api.day", "pk": day["id"], "fields": day})

    with open(save_path, "w") as f:
        json.dump(dict_result, f, indent=4)


def main(
    path_mal_csv: str = typer.Argument(
        "./api/scripts/raw_data/myanimelist_data.json",
        help="Path to the My Anime List csv data",
    ),
    path_at_csv: str = typer.Argument(
        "./api/scripts/raw_data/animethemes_data.json",
        help="Path to the AnimetThemes csv data",
    ),
    path_out: str = typer.Argument(
        "./api/scripts/parsed_data", help="Path to the output folder"
    ),
    date_start: str = typer.Option(
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
        & ~df_anime_themes["nsfw"]
    ]

    # Drop animes that doestn have any theme
    df_anime = df_anime[df_anime["id_anime"].isin(df_anime_themes["id_anime"].unique())]

    df_anime["hardcore"] = df_anime["rank"] >= 200

    df_anime_easy = df_anime[~df_anime["hardcore"]]
    df_anime_hardcore = df_anime[df_anime["hardcore"]]

    df_anime_themes_easy = df_anime_themes[
        df_anime_themes["id_anime"].isin(df_anime_easy["id_anime"])
    ]

    df_anime_themes_hardcore = df_anime_themes[
        df_anime_themes["id_anime"].isin(df_anime_hardcore["id_anime"])
    ]

    df_days = select_animethemes(
        df_anime_themes_easy,
        df_anime_themes_hardcore,
        date_start=date_start,
    )

    test_data(df_anime, df_anime_themes, df_days)

    animes_to_json(df_anime, f"{path_out}/animes.json")
    themes_to_json(df_anime_themes, f"{path_out}/themes.json")
    days_to_json(df_days, f"{path_out}/days.json")

    # After this, you can run the following commands to populate the database:
    # python manage.py loaddata scripts/parsed_data/animes.json
    # python manage.py loaddata scripts/parsed_data/themes.json
    # python manage.py loaddata scripts/parsed_data/days.json

    # df_days.to_csv(f"{path_out}/days.csv", index=False)
    # df_anime.to_csv(f"{path_out}/animes.csv", index=False)
    # df_anime_themes.to_csv(f"{path_out}/themes.csv", index=False)


if __name__ == "__main__":
    typer.run(main)
