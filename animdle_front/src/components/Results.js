import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getResults } from "../api/apiCalls"
import "../styles/Results.css";
import "../styles/utils.css";
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CountUp from 'react-countup';
import { useNavigate } from "react-router-dom";
import Share from "./game/Share";
import templeIcon from '../assets/pixelart_icon/temple_icon.png';
import darkDrakeIcon from '../assets/pixelart_icon/dark_drake_icon.png';
import whiteDrakeIcon from '../assets/pixelart_icon/white_drake_icon.png';
import lanternIcon from '../assets/pixelart_icon/lantern_icon.png';
import { motion } from 'framer-motion';
import { usePlayedModes } from "../App";
import Badge from '@mui/material/Badge';
import { useTranslation } from "react-i18next";


function Results({ mode }) {
    const { t } = useTranslation('common');
    const { playedModes } = usePlayedModes();
    const date = useParams().date;
    const dateString = date ? "/" + date : "";
    const [results, setResults] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getResults(mode, date).then(response => {
            if (!response.attempts)
                navigate("/" + mode + dateString);
            setResults(response);
        }).catch(error => {
            console.log(error);
        })
    }, [mode, date, dateString, navigate])

    return (
        <>
            {results &&
                <motion.div
                    initial="hidden"
                    animate="visible"
                    variants={{
                        hidden: { y: '100vh' },
                        visible: {
                            y: 0, transition: { duration: 0.2 }
                        }
                    }}
                    className="results-container"
                >
                    <div className="anime-data">
                        <img
                            className={"round-border " + (results.state === "win" ? "correct-shadow" : "error-shadow")}
                            src={results.image_url}
                            alt={"Image from " + results.title}
                        />
                        <div className={"anime-info round-border " + (results.state === "win" ? "correct-shadow" : "error-shadow")}>
                            <div className="anime-title">
                                <h1 className="anime-text" style={{ marginBottom: 0 }}>{results.title}</h1>
                                {results && results.state === "win" ?
                                    <CheckCircleIcon style={{ color: "#5eba61" }} /> :
                                    <ErrorIcon style={{ color: "#e34f4f" }} />
                                }
                            </div>
                            <h2 className="anime-text">({results.song})</h2>
                            <div className="video-wrapper">
                                <video
                                    style={{ backgroundColor: "black" }}
                                    src={results.video_url}
                                    controls
                                />
                            </div>
                        </div>
                    </div>
                    <div className="anime-result round-border simple-shadow">
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">{t("results.label.played")}</h3>
                            <div className="result-text">
                                <CountUp end={results.played} duration={2} />
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">{t("results.label.wins")}</h3>
                            <div className="result-text">
                                <p style={{ margin: "0px" }}><CountUp end={results.wins / results.played * 100} duration={2} /> %</p>
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">{t("results.label.streak")}</h3>
                            <div className="result-text">
                                <CountUp end={results.current_streak} duration={2} />
                            </div>
                        </div>
                        <div className="result-circle simple-shadow">
                            <h3 className="result-title">{t("results.label.record")}</h3>
                            <div className="result-text">
                                <CountUp end={results.record_streak} duration={2} />
                            </div>
                        </div>
                    </div>
                    <div className="results-last-row">
                        <Share
                            results={results}
                            date={date}
                            game_mode={mode}
                        />

                        <div className="redirect-buttons">
                            <div className="buttons-row">
                                <Badge badgeContent={!Object.keys(playedModes).includes("opening") ? "!" : 0} invisible={Object.keys(playedModes).includes("opening")} color='error'>
                                    <button className="redirect-button search-btn round-border" onClick={() => navigate("/opening" + dateString)}>
                                        <img className="button-icon" src={templeIcon} alt="Opening icon" />
                                        Openings
                                    </button>
                                </Badge>
                                <Badge badgeContent={!Object.keys(playedModes).includes("ending") ? "!" : 0} invisible={Object.keys(playedModes).includes("ending")} color='error'>
                                    <button className="redirect-button search-btn round-border" onClick={() => navigate("/ending" + dateString)}>
                                        <img className="button-icon" src={lanternIcon} alt="Ending icon" />
                                        Endings
                                    </button>
                                </Badge>
                            </div>
                            <div className="buttons-row">
                                <Badge badgeContent={!Object.keys(playedModes).includes("hardcore-opening") ? "!" : 0} invisible={Object.keys(playedModes).includes("hardcore-opening")} color='error'>
                                    <button className="redirect-button search-btn round-border" onClick={() => navigate("/hardcore-opening" + dateString)}>
                                        <img className="button-icon" src={darkDrakeIcon} alt="Hardcore opening icon" />
                                        Hardcore Openings
                                    </button>
                                </Badge>
                                <Badge badgeContent={!Object.keys(playedModes).includes("hardcore-ending") ? "!" : 0} invisible={Object.keys(playedModes).includes("hardcore-ending")} color='error'>
                                    <button className="redirect-button search-btn round-border" onClick={() => navigate("/hardcore-ending" + dateString)}>
                                        <img className="button-icon" src={whiteDrakeIcon} alt="Hardcore ending icon" />
                                        Hardcore Endings
                                    </button>
                                </Badge>
                            </div>
                        </div>
                    </div>
                </motion.div >
            }
        </>
    )
}

export default Results;