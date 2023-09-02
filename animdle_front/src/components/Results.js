import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getResults } from "../api/apiCalls"
import Lives from "./game/Lives"
import "../styles/Results.css";

function Results({ mode }) {
    const date = useParams().date;
    const [results, setResults] = useState(null);

    useEffect(() => {
        getResults(mode, date).then(response => {
            setResults(response);
            console.log(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date])

    return (
        <>
            {results &&
                <div className="results-container">
                    <div className="anime-data">
                        <img
                            className={"anime-image " + (results.state === "win" ? "win-image" : "lose-image")}
                            src={results.image_url}
                            alt={"Image from " + results.title}
                        />
                        <div className="anime-info">
                            <div className="anime-info-inner">
                                <h1 className="anime-text">{results.title}</h1>
                                <h2 className="anime-text">{"(" + results.song + ")"}</h2>
                                <video
                                    className="anime-video"
                                    src={results.video_url}
                                    playing={false}
                                    controls={true}
                                    width="70%"
                                    height="auto"
                                />
                                <Lives livesUsed={results.attempts.length} gameState={results.state} />
                            </div>
                        </div>
                    </div>
                </div>
            }
        </>
    )
}

export default Results;