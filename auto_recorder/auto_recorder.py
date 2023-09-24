import os
import subprocess
import time

import pandas as pd
import requests
import typer
from moviepy.editor import (
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def split_text(text, max_length=15):
    words = text.split(" ")
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) > max_length:
            lines.append(line)
            line = ""
        line += f" {word}"
    lines.append(line)
    return "\n".join(lines)


SECOND_TEXTS = [
    "Din't guess it? Keep thinking!",
    "Don't worry you still have a last chance!",
]

THIRD_TEXTS = [
    "You are almost there!",
    "Leave your guess in the comments!",
]


def compose_live_clip(video_url, num_live, utils_folder="videos/utils"):
    baseclip = VideoFileClip(video_url)
    baseclip = baseclip.set_duration(baseclip.duration - 0.5)

    width, height = baseclip.size

    dancing_clip = VideoFileClip(f"{utils_folder}/dancing.gif", has_mask=True)
    dancing_clip = dancing_clip.loop().set_duration(baseclip.duration).set_start(0)
    dancing_clip = dancing_clip.resize(height=height * 0.4).set_position(
        ("center", 500)
    )

    baseclip = CompositeVideoClip([baseclip, dancing_clip])

    # Add texts to the base clip
    if num_live == 3:
        start_time = 1
        for text in SECOND_TEXTS:
            text_clip = TextClip(
                split_text(text, max_length=30),
                color="black",
                font="Arial",
                align="center",
                fontsize=30,
                bg_color="white",
            )
            text_clip = (
                text_clip.set_position(("center", 400))
                .set_duration(3)
                .set_start(start_time)
            )
            baseclip = CompositeVideoClip([baseclip, text_clip])

            start_time += 4

    elif num_live == 5:
        start_time = 2
        for text in THIRD_TEXTS:
            text_clip = TextClip(
                split_text(text, max_length=30),
                color="black",
                font="Arial",
                align="center",
                fontsize=30,
                bg_color="white",
            )
            text_clip = (
                text_clip.set_position(("center", 400))
                .set_duration(7)
                .set_start(start_time)
            )
            baseclip = CompositeVideoClip([baseclip, text_clip])

            start_time += 9

    if num_live != 1:
        time_between = 2

        first_frame = baseclip.get_frame(0)
        frame_clip = ImageClip(first_frame, duration=time_between)

        black_square = ColorClip(size=(width, height), color=(0, 0, 0, 170))
        black_square = black_square.set_duration(time_between)

        forward_clip = (
            VideoFileClip(f"{utils_folder}/forward.gif", has_mask=True)
            .loop()
            .resize(height=height * 0.4)
            .set_duration(time_between)
        )
        forward_clip = forward_clip.set_position(("center", 40))

        if num_live == 3:
            text = "LET'S TRY AGAIN!"
        else:
            text = "THIS IS YOUR LAST CHANCE!"

        text_clip = TextClip(
            split_text(text), color="white", font="Impact", align="center", fontsize=70
        )
        text_clip = text_clip.set_position(("center", 450)).set_duration(time_between)

        between_clip = CompositeVideoClip(
            [frame_clip, black_square, forward_clip, text_clip]
        )

        baseclip = concatenate_videoclips([between_clip, baseclip])

    return baseclip


def back_clip(
    image_url, anime_title, width, height, audio, utils_folder="videos/utils"
):
    end_duration = 7

    audio_clip = audio.subclip(5, 5 + end_duration).audio_fadeout(1.0)

    image_clip = (
        ImageClip(image_url)
        .set_duration(end_duration)
        .resize((width, height))
        .set_audio(audio_clip)
    )

    black_square = ColorClip(size=(width, height), color=(0, 0, 0, 170))
    black_square = black_square.set_duration(end_duration)

    text_clip = TextClip(
        split_text("The anime was!"), color="white", font="Impact", fontsize=80
    )
    text_clip = text_clip.set_position(("center", 500)).set_duration(end_duration)

    anime_title_clip = TextClip(
        split_text(anime_title, max_length=25),
        color="white",
        font="Impact",
        align="center",
        fontsize=100,
    )
    anime_title_clip = anime_title_clip.set_position(("center", 650)).set_duration(
        end_duration
    )

    logo_clip = (
        ImageClip(f"{utils_folder}/logo.png")
        .set_duration(end_duration)
        .resize(width=width * 0.7)
        .set_position(("center", 950))
    )

    confetti1 = (
        VideoFileClip(f"{utils_folder}/confetti1.gif", has_mask=True)
        .loop()
        .set_duration(7)
        .set_position(("left", "top"))
        .resize(height=width * 0.4)
    )
    confetti2 = (
        VideoFileClip(f"{utils_folder}/confetti2.gif", has_mask=True)
        .loop()
        .set_duration(7)
        .set_position(("right", "top"))
        .resize(height=width * 0.4)
    )
    confetti3 = (
        VideoFileClip(f"{utils_folder}/confetti3.gif", has_mask=True)
        .loop()
        .set_duration(7)
        .set_position(("center", 1000))
        .resize(height=width * 0.4)
    )

    return CompositeVideoClip(
        [
            image_clip,
            black_square,
            text_clip,
            anime_title_clip,
            logo_clip,
            confetti1,
            confetti2,
            confetti3,
        ]
    )


def download_image(url, output_path):
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)


def create_video(video_folder, utils_folder, mode, anime_data):
    front_clip = VideoFileClip(f"{utils_folder}/front_{mode}.mp4")

    liveclips = [
        compose_live_clip(f"{video_folder}/{i}.mp4", i, utils_folder) for i in [1, 3, 5]
    ]
    main_clip = concatenate_videoclips(liveclips).resize(front_clip.size)

    audio = VideoFileClip(f"{video_folder}/5.mp4").audio

    title = anime_data["title"]
    image_url = anime_data["image_url"]

    download_image(image_url, f"{video_folder}/anime_image.png")

    back_clip_ = back_clip(
        f"{video_folder}/anime_image.png",
        title,
        front_clip.size[0],
        front_clip.size[1],
        audio,
    )

    final_clip = concatenate_videoclips([front_clip, main_clip, back_clip_])
    final_clip.write_videofile(f"{video_folder}/final.mp4")


def start_recording(output_path):
    recorder = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-video_size",
            "594x1056",
            "-probesize",
            "32M",
            "-framerate",
            "60",
            "-thread_queue_size",
            "512",
            "-f",
            "x11grab",
            "-draw_mouse",
            "0",
            "-i",
            ":1.0",
            "-thread_queue_size",
            "512",
            "-f",
            "pulse",
            "-i",
            "default",
            "-c:a",
            "aac",
            "-pix_fmt",
            "yuv420p",
            output_path,
        ]
    )

    return recorder


def play_game(driver, output_folder):
    # Skip guide
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='react-joyride__tooltip']//button[@aria-label='Skip']",
                )
            )
        ).click()
    except TimeoutException:
        print("No guide found...")

    recorder = start_recording(f"{output_folder}/test.mp4")

    time.sleep(5)

    recorder.terminate()

    for i in range(5):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "playIcon")),
            30,
        ).click()

        recorder = start_recording(f"{output_folder}/{i+1}.mp4")

        time.sleep(1)

        # Play video
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "playIcon")),
            30,
        )

        recorder.terminate()
        driver.find_element(
            By.XPATH, "//button[@class='search-btn round-border'][2]"
        ).click()

        time.sleep(1)


def record_game(
    data_dir="./animdle_back/api/scripts/parsed_data",
    videos_folder="videos",
    date=None,
    force=False,
):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("--display=:1")
    options.add_argument("--app=https://animdle.com")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service()

    if date is None:
        date = pd.Timestamp.now().strftime("%Y-%m-%d")

    days_df = pd.read_json(f"{data_dir}/days.json")
    days_df["date"] = days_df["fields"].apply(lambda x: x["date"])
    themes_df = pd.read_json(f"{data_dir}/themes.json")
    animes_df = pd.read_json(f"{data_dir}/animes.json")

    day = days_df[days_df["date"] == date]["fields"].values[0]

    output_folder = f"{videos_folder}/games/{date}"
    utils_folder = f"{videos_folder}/utils"

    base_url = "https://animdle.com"
    for col in ["opening", "hardcore_opening", "ending", "hardcore_ending"]:
        theme_id = day[col]
        anime_id = themes_df[themes_df["pk"] == theme_id]["fields"].values[0]["anime"]
        anime_data = animes_df[animes_df["pk"] == anime_id]["fields"].values[0]

        url = f"{base_url}/{col.replace('_','-')}/{date}"

        print(f"Playing {url}...")

        game_folder = f"{output_folder}/{col}"
        if not os.path.exists(game_folder):
            os.makedirs(game_folder)

        # Fix this expression
        if force or any(
            [not os.path.exists(f"{game_folder}/{i}.mp4") for i in [1, 3, 5]]
        ):
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_window_size(574, 1036)
            driver.get(url)

            time.sleep(2)
            play_game(driver, game_folder)
            driver.quit()

        print("Creating video...")
        create_video(game_folder, utils_folder, col, anime_data)

        print("Done!")


if __name__ == "__main__":
    typer.run(record_game)
