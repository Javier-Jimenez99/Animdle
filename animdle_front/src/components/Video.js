import { useState, useRef } from "react"
import ReactPlayer from "react-player";
import { IconButton } from '@mui/material';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';
import PauseRoundedIcon from '@mui/icons-material/PauseRounded';
import LinearProgress from '@mui/material/LinearProgress';
import "../styles/Video.css";

function Video({ maxPlayableTime, blur, videoURL }) {
    const [playing, setPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const playerRef = useRef(null);

    const handleProgress = (progress) => {
        if (progress.playedSeconds > maxPlayableTime) {
            playerRef.current.seekTo(0);
            setPlaying(false);
        };
        setProgress(progress.playedSeconds)
    }

    const handlePlay = () => {
        setPlaying(true);
    }

    const handlePause = () => {
        setPlaying(false);
    }

    return (
        <div className="video-container">
            <style>
                {
                    `.blur {
                                -webkit-filter: blur(${blur}px); 
                                -moz-filter: blur(${blur}px); 
                                -o-filter: blur(${blur}px); 
                                -ms-filter: blur(${blur}px); 
                                filter: blur(${blur}px);                                
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
                        controls={false}
                        width="100%"
                        height="100%"
                        onProgress={handleProgress}
                        progressInterval={100}
                        onPlay={handlePlay}
                        onPause={handlePause}
                    />
                </div>
            </div>
            <div className="video-controls">
                {playing ?
                    <IconButton onClick={handlePause}>
                        <PauseRoundedIcon className="control-icon" />
                    </IconButton> :
                    <IconButton onClick={handlePlay} >
                        <PlayArrowRoundedIcon className="control-icon" />
                    </IconButton>
                }
                <div className="progress-bar">
                    <LinearProgress className="progress-bar-line" variant="determinate" value={progress / maxPlayableTime * 100} />
                    <p className="progress-bar-time">
                        {progress.toFixed() + " s"}
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Video;