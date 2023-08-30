import { useEffect, useState } from "react"
import { getGameState } from "../api/apiCalls";

function Game({ mode, date = null }) {
    const [gameState, setGameState] = useState(null);

    useEffect(() => {
        getGameState(mode, date).then(response => {
            setGameState(response);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    return (
        <div>
            <h1>Game</h1>
            {gameState !== null ?
                <div>

                </div>
                : null}
        </div>
    )
}

export default Game;