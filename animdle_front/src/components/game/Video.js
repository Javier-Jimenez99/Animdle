import { useState, useRef, useEffect } from "react"
import ReactPlayer from "react-player";
import { IconButton, Slider } from '@mui/material';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';
import PauseRoundedIcon from '@mui/icons-material/PauseRounded';
import FullscreenIcon from '@mui/icons-material/Fullscreen';
import FullscreenExitIcon from '@mui/icons-material/FullscreenExit';
//import ReplayRoundedIcon from '@mui/icons-material/ReplayRounded';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import "../../styles/Video.css";
import "../../styles/utils.css";
import { useTranslation } from "react-i18next";
import screenfull from 'screenfull';

function Video({ maxPlayableTime, blur, videoURL, resetVideo, setResetVideo, gameState, showVideo = true }) {
    const { t } = useTranslation('common');
    const [playing, setPlaying] = useState(false);
    const [filter, setFilter] = useState("blur(0px)")
    const [progress, setProgress] = useState(0);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const playerRef = useRef(null);
    const [volume, setVolume] = useState(0.6);

    useEffect(() => {
        if (resetVideo) {
            setPlaying(false);
            setProgress(0);
            playerRef.current.seekTo(0, "seconds");
        }
    }, [resetVideo])

    useEffect(() => {
        let filterString = "blur(" + blur + "px)";
        if (!showVideo)
            filterString += " brightness(0)";

        setFilter(filterString);
    }, [blur, showVideo])

    const handleProgress = (progress) => {
        if (progress.playedSeconds > maxPlayableTime) {
            playerRef.current.seekTo(0, "seconds");
            setPlaying(false);
        };
        setProgress(progress.playedSeconds)
    }

    const handlePlay = () => {
        setResetVideo(false);
        setPlaying(true);
    }

    const handlePause = () => {
        setPlaying(false);
    }

    /*const handleReplay = () => {
        playerRef.current.seekTo(0, "seconds");
        setPlaying(true);
    }*/

    const handleClickSlider = (e, value) => {
        const percentage = value / 100;
        const time = percentage * maxPlayableTime;
        playerRef.current.seekTo(time, 'seconds');
        setProgress(time);
    }

    const handleVolume = (event, newValue) => {
        setVolume(newValue / 100);
    };

    const videoContainerControls = useRef(null);
    const handleClickFullscreen = () => {

        if (screenfull.isEnabled) {
            setIsFullscreen(!isFullscreen);
            screenfull.toggle(videoContainerControls.current);
        }
    };

    return (
        <div ref={videoContainerControls} className="video-container round-border">
            <style>
                {
                    `.blur {
                                -webkit-filter: ${filter}; 
                                -moz-filter: ${filter}; 
                                -o-filter: ${filter}; 
                                -ms-filter: ${filter}; 
                                filter: ${filter};                                
                            }`
                }
            </style>
            <div className="player-wrapper1">
                <div className="player-wrapper2">
                    <ReactPlayer
                        className="react-player blur"
                        ref={playerRef}
                        url={videoURL}
                        playing={playing}
                        volume={volume}
                        controls={["win", "lose"].includes(gameState)}
                        width="100%"
                        height="100%"
                        onProgress={handleProgress}
                        progressInterval={100}
                        onPlay={handlePlay}
                        onPause={handlePause}
                    />
                    {!showVideo && <div className="overlay-text">{t("deactivatedVideo")}</div>}
                </div>
            </div>
            {
                ["win", "lose"].includes(gameState) ? null :
                    <div className="video-controls">
                        {playing ?
                            <IconButton onClick={handlePause}>
                                <PauseRoundedIcon className="control-icon" />
                            </IconButton> :
                            <IconButton onClick={handlePlay} >
                                <PlayArrowRoundedIcon className="control-icon" />
                            </IconButton>
                        }
                        <Slider style={{ margin: "10px", color: "white" }} value={progress / maxPlayableTime * 100} onChangeCommitted={handleClickSlider} aria-label="Progress slider" />
                        <VolumeUpIcon className="control-icon" />
                        <Slider style={{ margin: "10px", color: "white", width: "20%" }} onChange={handleVolume} defaultValue={60} aria-label="Volume slider" />

                        <IconButton onClick={handleClickFullscreen} >
                            {!isFullscreen ? <FullscreenIcon className="control-icon" /> :
                                <FullscreenExitIcon className="control-icon" />
                            }
                        </IconButton>

                        {
                            /*<IconButton onClick={handleReplay} >
                                <ReplayRoundedIcon className="control-icon" />
                            </IconButton>*/
                        }
                    </div>
            }
        </div>
    )
}

export default Video;