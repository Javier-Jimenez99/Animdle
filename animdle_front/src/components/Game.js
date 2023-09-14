import { useEffect, useState, useRef } from "react"
import { useParams } from "react-router-dom";
import { getGameState, postGuess, getPlayedModes } from "../api/apiCalls";
import "../styles/Game.css";
import "../styles/utils.css";
import Video from "./game/Video";
import Lives from "./game/Lives"
import SearchBar from "./game/SearchBar";
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ConfettiExplosion from 'react-confetti-explosion';
import { useNavigate } from "react-router-dom";
import Joyride, { STATUS } from 'react-joyride';
import { usePlayedModes } from "../App";
import { useTranslation } from "react-i18next";

const DIFFICULTY = [
    { "maxPlayableTime": 3, "blur": 40 },
    { "maxPlayableTime": 5, "blur": 20 },
    { "maxPlayableTime": 10, "blur": 10 },
    { "maxPlayableTime": 15, "blur": 5 },
    { "maxPlayableTime": 20, "blur": 0 },
    { "maxPlayableTime": 30, "blur": 0 },
    { "maxPlayableTime": 1000, "blur": 0 } // This is to dont crash the game
]

function Game({ mode }) {
    const { t } = useTranslation('common');
    const { playedModes, setPlayedModes } = usePlayedModes();
    const navigate = useNavigate();
    const date = useParams().date;
    const windowSize = useRef([window.innerWidth, window.innerHeight]);
    const [showVideo, setShowVideo] = useState(true);
    const [spoiler, setSpoiler] = useState(false);

    // Game variables
    const [gameState, setGameState] = useState(null);
    const [videoURL, setVideoURL] = useState(null);
    // This is to reset the video when there is a guess or a skip
    const [resetVideo, setResetVideo] = useState(false);
    const [attempts, setAttempts] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [allTitles, setAllTitles] = useState([]);
    const [guessDisabled, setGuessDisabled] = useState(true);

    const maxLives = mode.includes("hardcore") && playedModes[mode.replace("hardcore-", "")] === "win" ? 6 : 5;

    useEffect(() => {
        getGameState(mode, date).then(response => {
            setVideoURL(response.video_url);
            setGameState(response.state);
            setAttempts(response.attempts);
            setAllTitles(response.all_titles);
            setSpoiler(response.spoiler);
            setShowVideo(!response.spoiler);

            getPlayedModes().then((data) => { setPlayedModes(data) });

        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    useEffect(() => {
        if (gameState && gameState !== "pending") {
            const time = gameState == "win" ? 2000 : 500;

            const timer = setTimeout(() => {
                navigate("/" + mode + "/results/" + (date ? date : ""));
            }, time);

            return () => clearTimeout(timer);
        }
    }, [gameState, navigate, mode, date]);

    useEffect(() => {
        if (allTitles)
            setGuessDisabled(!allTitles.includes(inputValue));
    }, [inputValue, allTitles])

    const handleGuess = () => {
        postGuess(mode, date, inputValue, maxLives).then(response => {
            setGameState(response.state);
            setAttempts(response.attempts);
            const newTitles = allTitles.filter(title => title !== inputValue);
            setAllTitles(newTitles);
            setInputValue("");
            setResetVideo(true);

            if (response.state !== "pending") {
                setPlayedModes({ ...playedModes, [mode]: response.state });
            }

        }).catch(error => {
            console.log(error);
        })
    }

    const handleSkip = () => {
        postGuess(mode, date, "Skip!", maxLives).then(response => {
            setGameState(response.state);
            setAttempts(response.attempts);
            setResetVideo(true);

            if (response.state !== "pending") {
                console.log([mode], response.state);
                setPlayedModes({ ...playedModes, [mode]: response.state });
            }
        }).catch(error => {
            console.log(error);
        })
    }

    const guideSteps = [
        {
            target: "body",
            placement: "center",
            content: (
                <div style={{ textAlign: "center" }}>
                    <h2>{t("guide.intro.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.intro.text") }} />
                </div>
            )
        },
        {
            target: ".video-container",
            content: (
                <div>
                    <h2>{t("guide.video.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.video.text") }} />
                </div>
            )
        },
        {
            target: ".guess-container",
            content: (
                <div>
                    <h2>{t("guide.guess.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.guess.text") }} />
                </div>
            )
        },
        {
            target: ".hearts-container",
            content: (
                <div>
                    <h2>{t("guide.lives.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.lives.text") }} />
                </div>
            )
        },
        {
            target: ".switch-container",
            content: (
                <div>
                    <h2>{t("guide.videoSwitch.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.videoSwitch.text") }} />
                </div>
            )
        },
        {
            target: "#long-button",
            content: (
                <div>
                    <h2>{t("guide.modes.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("guide.modes.text") }} />
                </div>
            )
        },
        {
            target: "body",
            placement: "center",
            content: (
                <div>
                    <h2>{t("guide.end.title")}</h2>
                </div>
            )
        }
    ]

    const spoilerStep = [
        {
            target: ".switch-container",
            content: (
                <div>
                    <h2>{t("spoilerAlert.title")}</h2>
                    <p dangerouslySetInnerHTML={{ __html: t("spoilerAlert.text") }} />
                </div>
            ),
            disableBeacon: true
        }
    ]

    return (
        <>
            {gameState &&
                <div className="game-container">
                    <Joyride
                        steps={guideSteps}
                        run={!localStorage.getItem("visited") && gameState === "pending"}
                        callback={(data) => {
                            if ([STATUS.FINISHED, STATUS.SKIPPED].includes(data.status)) {
                                localStorage.setItem("visited", true);
                            }
                        }}
                        continuous={true}
                        showProgress={true}
                        showSkipButton={true}
                        styles={{
                            options: {
                                primaryColor: '#dd6559',
                            }
                        }}
                        locale={{
                            back: t("guide.buttons.back"),
                            close: t("guide.buttons.close"),
                            last: t("guide.buttons.last"),
                            next: t("guide.buttons.next"),
                        }}
                    />

                    <Joyride
                        steps={spoilerStep}
                        run={spoiler && gameState === "pending"}
                        styles={{
                            options: {
                                primaryColor: '#dd6559',
                            }
                        }}
                        locale={{
                            close: t("guide.buttons.close"),
                        }}
                    />

                    {gameState === "win" &&
                        <>
                            <ConfettiExplosion
                                className="confetti1"
                                force={0.2}
                                duration={3000}
                                particleCount={400}
                                colors={["#DD675B", "#E4A892", "#FBEDE4"]}
                                zIndex={0}
                                width={windowSize.current[0] * 1.5}
                                height={windowSize.current[1] * 3}
                            />
                            <ConfettiExplosion
                                className="confetti2"
                                force={0.2}
                                duration={3000}
                                particleCount={400}
                                colors={["#DD675B", "#E4A892", "#FBEDE4"]}
                                zIndex={0}
                                width={windowSize.current[0] * 1.5}
                                height={windowSize.current[1] * 3}
                            />
                        </>
                    }

                    <Video
                        maxPlayableTime={gameState === "win" ? 1000 : DIFFICULTY[attempts.length].maxPlayableTime}
                        blur={gameState === "win" ? 0 : DIFFICULTY[attempts.length].blur}
                        videoURL={videoURL}
                        resetVideo={resetVideo}
                        setResetVideo={setResetVideo}
                        gameState={gameState}
                        showVideo={showVideo}
                    />
                    <div className="lives-row">
                        <Lives livesUsed={attempts.length} gameState={gameState} hardcore={mode.includes("hardcore")} maxLives={maxLives} />
                        <div className="switch-container">
                            <h1 className="switch-text">VIDEO</h1>
                            <input className="tgl tgl-skewed" id="cb3" type="checkbox" checked={showVideo} onChange={() => { setShowVideo(!showVideo) }} />
                            <label className="tgl-btn" data-tg-off="OFF" data-tg-on="ON" for="cb3"></label>
                        </div>
                    </div>

                    <div className="guess-container">
                        <SearchBar inputValue={inputValue} setInputValue={setInputValue} allResults={allTitles} />
                        <div className="search-buttons">
                            <button className="search-btn round-border" disabled={guessDisabled || ["win", "lose"].includes(gameState)} onClick={handleGuess}>
                                {t("search.buttons.guess")}
                            </button>
                            <button className="search-btn round-border" disabled={["win", "lose"].includes(gameState)} onClick={handleSkip}>
                                {t("search.buttons.skip")}
                            </button>
                        </div>
                    </div>
                    {attempts.length > 0 &&
                        <div className="attempts-container">
                            {attempts.map((attempt, index) => {
                                if (gameState === "win" && index === attempts.length - 1) {
                                    return (
                                        <div key={index} className="attempt correct-shadow round-border">
                                            <CheckCircleIcon style={{ color: "#5eba61" }} />
                                            <div className="attempt-text">{attempt}</div>
                                        </div>
                                    );
                                }
                                else {
                                    return (
                                        <div key={index} className="attempt error-shadow round-border">
                                            <ErrorIcon style={{ color: "#e34f4f" }} />
                                            <div className="attempt-text">{attempt}</div>
                                        </div>
                                    );
                                }

                            })}
                        </div>
                    }
                </div >
            }

        </>
    )
}

export default Game;