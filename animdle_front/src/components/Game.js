import { useEffect, useState } from "react"
import { getGameState } from "../api/apiCalls";
import "../styles/Game.css";
import Video from "./game/Video";
import Lives from "./game/Lives"
import SearchBar from "./game/SearchBar";

const DIFFICULTY = [
    { "maxPlayableTime": 3, "blur": 40 },
    { "maxPlayableTime": 5, "blur": 20 },
    { "maxPlayableTime": 10, "blur": 10 },
    { "maxPlayableTime": 15, "blur": 5 },
    { "maxPlayableTime": 20, "blur": 0 },
]

function Game({ mode, date = null }) {
    // Game variables
    const [gameState, setGameState] = useState(null);
    const [maxPlayableTime, setMaxPlayableTime] = useState(5);
    const [attempts, setAttempts] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [allTitles, setAllTitles] = useState([]);

    useEffect(() => {
        getGameState(mode, date).then(response => {
            setGameState(response);
            setAttempts(response.attempts);
            setMaxPlayableTime(DIFFICULTY[response.attempts.length].maxPlayableTime);
            setAllTitles(response.all_titles);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    return (
        <>
            {gameState !== null ?
                <div className="game-container">
                    <Video maxPlayableTime={maxPlayableTime} blur={DIFFICULTY[attempts.length].blur} videoURL={gameState.video_url} />
                    <Lives livesUsed={attempts.length} />

                    <div className="guess-container">
                        <SearchBar inputValue={inputValue} setInputValue={setInputValue} allResults={allTitles} />
                        <div className="guess-buttons">
                            <button className="search-btn">
                                GUESS
                            </button>
                            <button className="search-btn">
                                SKIP
                            </button>
                        </div>
                    </div>
                </div >
                : null
            }
        </>
    )
}

export default Game;