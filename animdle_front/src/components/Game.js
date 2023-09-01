import { useEffect, useState, useRef } from "react"
import { getGameState, postGuess } from "../api/apiCalls";
import "../styles/Game.css";
import Video from "./game/Video";
import Lives from "./game/Lives"
import SearchBar from "./game/SearchBar";
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ConfettiExplosion from 'react-confetti-explosion';

const DIFFICULTY = [
    { "maxPlayableTime": 3, "blur": 40 },
    { "maxPlayableTime": 5, "blur": 20 },
    { "maxPlayableTime": 10, "blur": 10 },
    { "maxPlayableTime": 15, "blur": 5 },
    { "maxPlayableTime": 20, "blur": 0 },
    { "maxPlayableTime": 1000, "blur": 0 } // This is to dont crash the game
]

function Game({ mode, date = null }) {
    const windowSize = useRef([window.innerWidth, window.innerHeight]);

    // Game variables
    const [gameState, setGameState] = useState(null);
    const [videoURL, setVideoURL] = useState(null);
    // This is to reset the video when there is a guess or a skip
    const [resetVideo, setResetVideo] = useState(false);
    const [attempts, setAttempts] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [allTitles, setAllTitles] = useState([]);
    const [guessDisabled, setGuessDisabled] = useState(true);

    useEffect(() => {
        getGameState(mode, date).then(response => {
            setVideoURL(response.video_url);
            setGameState(response.state);
            setAttempts(response.attempts);
            setAllTitles(response.all_titles);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    useEffect(() => {
        setGuessDisabled(!allTitles.includes(inputValue));
    }, [inputValue, allTitles])

    const handleGuess = () => {
        postGuess(mode, date, inputValue).then(response => {
            setGameState(response.state);
            setAttempts(response.attempts);
            const newTitles = allTitles.filter(title => title !== inputValue);
            setAllTitles(newTitles);
            setInputValue("");
            setResetVideo(true);
        }).catch(error => {
            console.log(error);
        })
    }

    const handleSkip = () => {
        postGuess(mode, date, "Skip!").then(response => {
            let newAttempts = [...attempts];
            newAttempts.push("Skip!");
            setGameState(response.state);
            setAttempts(newAttempts);
            setResetVideo(true);
        }).catch(error => {
            console.log(error);
        })
    }

    return (
        <>
            {gameState ?
                <div className="game-container">
                    {gameState === "win" ?
                        <>
                            <ConfettiExplosion
                                className="confetti1"
                                force={0.8}
                                duration={3000}
                                particleCount={400}
                                colors={["#DD675B", "#E4A892", "#FBEDE4"]}
                                zIndex={0}
                                width={windowSize.current[0]}
                                height={windowSize.current[1]}
                            />
                            <ConfettiExplosion
                                className="confetti2"
                                force={0.8}
                                duration={3000}
                                particleCount={400}
                                colors={["#DD675B", "#E4A892", "#FBEDE4"]}
                                zIndex={0}
                                width={windowSize.current[0]}
                                height={windowSize.current[1]}
                            />
                        </>
                        : null}

                    <Video
                        maxPlayableTime={gameState === "win" ? 1000 : DIFFICULTY[attempts.length].maxPlayableTime}
                        blur={gameState === "win" ? 0 : DIFFICULTY[attempts.length].blur}
                        videoURL={videoURL}
                        resetVideo={resetVideo}
                        setResetVideo={setResetVideo}
                    />
                    <Lives livesUsed={attempts.length} gameState={gameState} />

                    <div className="guess-container">
                        <SearchBar inputValue={inputValue} setInputValue={setInputValue} allResults={allTitles} />
                        <div className="guess-buttons">
                            <button className="search-btn" disabled={guessDisabled || ["win", "lose"].includes(gameState)} onClick={handleGuess}>
                                GUESS
                            </button>
                            <button className="search-btn" disabled={["win", "lose"].includes(gameState)} onClick={handleSkip}>
                                SKIP
                            </button>
                        </div>
                    </div>
                    {attempts.length > 0 ?
                        <div className="attempts-container">
                            {attempts.map((attempt, index) => {
                                console.log(gameState, index, attempt);
                                if (gameState === "win" && index === attempts.length - 1) {
                                    return (
                                        <div key={index} className="attempt attempt-correct">
                                            <CheckCircleIcon style={{ color: "#5eba61" }} />
                                            <div className="attempt-text">{attempt}</div>
                                        </div>
                                    );
                                }
                                else {
                                    return (
                                        <div key={index} className="attempt attempt-error">
                                            <ErrorIcon style={{ color: "#e34f4f" }} />
                                            <div className="attempt-text">{attempt}</div>
                                        </div>
                                    );
                                }

                            })}
                        </div>
                        : null}
                </div >
                : null
            }
        </>
    )
}

export default Game;