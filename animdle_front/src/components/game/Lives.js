import heartIcon from "../../assets/pixelart_icon/heart_icon.png";
import heartGreenIcon from "../../assets/pixelart_icon/heart_green_icon.png";
import heartGoldIcon from "../../assets/pixelart_icon/heart_gold_icon.png";
import heartGoldBlockedIcon from "../../assets/pixelart_icon/heart_gold_blocked_icon.png";
import Tooltip from '@mui/material/Tooltip';
import "../../styles/Lives.css";

function Lives({ livesUsed, gameState, hardcore = false, maxLives = 5 }) {

    const generateHearts = () => {
        console.log(livesUsed, maxLives, gameState, hardcore);
        let hearts = [];
        for (let i = 0; i < maxLives - livesUsed; i++) {
            hearts.push(<img className="heart" width={"15%"} src={heartIcon} alt="Live Heart of lost tries" key={hearts.length} />);
        }

        let loopStart = 0;
        if (gameState === "win") {
            hearts.push(<img className="heart" width={"15%"} src={heartGreenIcon} alt="Live Heart meaning that you won" key={hearts.length} />);
            loopStart++;
        }

        for (let i = loopStart; i < livesUsed; i++) {
            hearts.push(<img className="heart dead-heart" width={"15%"} src={heartIcon} alt="Live Heart of remaining tries" key={hearts.length} />);
        }

        if (hardcore) {
            if (maxLives === 5) {
                hearts.push(
                    <Tooltip title={"Win no hardcore mode to unlock this heart"} followCursor>
                        <img className="heart" width={"15%"} src={heartGoldBlockedIcon} alt="Live Heart of remaining tries" key={hearts.length} />
                    </Tooltip>
                );
            }

            if (maxLives === 6 && livesUsed < 1) {
                hearts.pop();
                hearts.push(
                    <img className="heart" width={"15%"} src={heartGoldIcon} alt="Live Heart of remaining tries" key={hearts.length} />
                );
            }

        }

        return hearts;
    }

    return (
        <div className="hearts-container">
            {generateHearts()}
        </div>
    )
}

export default Lives;