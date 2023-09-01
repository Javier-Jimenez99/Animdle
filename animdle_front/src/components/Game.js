import { useEffect, useState } from "react"
import { getGameState, postGuess } from "../api/apiCalls";
import "../styles/Game.css";
import Video from "./game/Video";
import Lives from "./game/Lives"
import SearchBar from "./game/SearchBar";
import ErrorIcon from '@mui/icons-material/Error';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';

const DIFFICULTY = [
    { "maxPlayableTime": 3, "blur": 40 },
    { "maxPlayableTime": 5, "blur": 20 },
    { "maxPlayableTime": 10, "blur": 10 },
    { "maxPlayableTime": 15, "blur": 5 },
    { "maxPlayableTime": 20, "blur": 0 },
    { "maxPlayableTime": 1000, "blur": 0 } // This is to dont crash the game
]

const MAX_LIVES = 5;

function Game({ mode, date = null }) {
    // Game variables
    const [gameState, setGameState] = useState(null);
    const [videoURL, setVideoURL] = useState(null);
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
        console.log(guessDisabled);
    }, [inputValue, allTitles])

    const handleGuess = () => {
        postGuess(mode, date, inputValue).then(response => {
            setGameState(response.state);
            setAttempts(response.attempts);
            const newTitles = allTitles.filter(title => title !== inputValue);
            setAllTitles(newTitles);
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
        }).catch(error => {
            console.log(error);
        })
    }

    return (
        <>
            {gameState ?
                <div className="game-container">
                    <Video
                        maxPlayableTime={DIFFICULTY[attempts.length].maxPlayableTime}
                        blur={DIFFICULTY[attempts.length].blur}
                        videoURL={videoURL}
                    />
                    <Lives livesUsed={attempts.length} />

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
                                            <ThumbUpAltIcon style={{ color: "#5eba61" }} />
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