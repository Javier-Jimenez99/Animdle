import { useEffect, useState } from "react"
import { getGameState } from "../api/apiCalls";
import "../styles/Game.css";
import Video from "./Video";

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
    //const maxLives = 5;
    const [usedLives, setUsedLives] = useState(0);

    useEffect(() => {
        getGameState(mode, date).then(response => {
            setGameState(response);
            setUsedLives(response.attempts.length)
            setMaxPlayableTime(DIFFICULTY[response.attempts.length].maxPlayableTime);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    return (
        <>
            {gameState !== null ?
                <div className="game-container">
                    <Video maxPlayableTime={maxPlayableTime} blur={DIFFICULTY[usedLives].blur} videoURL={gameState.video_url} />
                </div>
                : null}
        </>
    )
}

export default Game;