import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getResults } from "../api/apiCalls"
import "../styles/Results.css";
import "../styles/utils.css";
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

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
                            class={"anime-image " + (results.state === "win" ? "correct-shadow" : "error-shadow")}
                            src={results.image_url}
                            alt={"Image from " + results.title}
                        />
                        <div class={"anime-info " + (results.state === "win" ? "correct-shadow" : "error-shadow")}>
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
                </div>

            }
        </>
    )
}

export default Results;