import { useEffect, useState } from "react"
import { getTodaysVideo } from "../api/apiCalls";

function Game({ mode }) {
    const [videoURL, setVideoURL] = useState(null);

    useEffect(() => {
        getTodaysVideo(mode).then(response => {
            setVideoURL(response.video_url);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode])

    return (
        <div>
            <h1>Game</h1>
            {videoURL !== null ?
                <div>
                    <p>{videoURL}</p>
                </div>
                : null}
        </div>
    )
}

export default Game;