import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getResults } from "../api/apiCalls"
import "../styles/Results.css";
import "../styles/utils.css";
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CountUp from 'react-countup';

import Share from "./game/Share";

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
                <div class="results-container">
                    <div class="anime-data">
                        <img
                            class={"anime-image round-border " + (results.state === "win" ? "correct-shadow" : "error-shadow")}
                            src={results.image_url}
                            alt={"Image from " + results.title}
                        />
                        <div class={"anime-info round-border " + (results.state === "win" ? "correct-shadow" : "error-shadow")}>
                            <div className="anime-title">
                                <h1 class="anime-text">{results.title}</h1>
                                {results && results.state === "win" ?
                                    <CheckCircleIcon style={{ color: "#5eba61" }} /> :
                                    <ErrorIcon style={{ color: "#e34f4f" }} />
                                }
                            </div>
                            <h2 class="anime-text">({results.song})</h2>
                            <p dangerouslySetInnerHTML={{ __html: results.synopsis }} />
                        </div>
                    </div>
                    <div className="anime-result round-border simple-shadow">
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">PLAYED</h3>
                            <div className="result-text">
                                <CountUp end={results.played} duration={2} />
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">WINS RATE</h3>
                            <div className="result-text">
                                <p style={{ margin: "0px" }}><CountUp end={results.wins / results.played * 100} duration={2} /> %</p>
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">STREAK</h3>
                            <div className="result-text">
                                <CountUp end={results.current_streak} duration={2} />
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">RECORD</h3>
                            <div className="result-text">
                                <CountUp end={results.record_streak} duration={2} />
                            </div>
                        </div>
                    </div>
                    <Share results={results} date={date} />
                </div >

            }
        </>
    )
}

export default Results;