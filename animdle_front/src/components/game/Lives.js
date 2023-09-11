import heartIcon from "../../assets/pixelart_icon/heart_icon.png";
import heartGreenIcon from "../../assets/pixelart_icon/heart_green_icon.png";
import heartGoldIcon from "../../assets/pixelart_icon/heart_gold_icon.png";
import heartGoldBlockedIcon from "../../assets/pixelart_icon/heart_gold_blocked_icon.png";
import Tooltip from '@mui/material/Tooltip';
import "../../styles/Lives.css";
import { useTranslation } from "react-i18next";

function Lives({ livesUsed, gameState, hardcore = false, maxLives = 5 }) {
    const { t } = useTranslation('common');

    const generateHearts = () => {
        let hearts = [];
        for (let i = 0; i < maxLives - livesUsed; i++) {
            hearts.push(<img className="heart" width={"13%"} src={heartIcon} alt="Live Heart of lost tries" key={hearts.length} />);
        }

        let loopStart = 0;
        if (gameState === "win") {
            hearts.push(<img className="heart" width={"13%"} src={heartGreenIcon} alt="Live Heart meaning that you won" key={hearts.length} />);
            loopStart++;
        }

        for (let i = loopStart; i < livesUsed; i++) {
            hearts.push(<img className="heart dead-heart" width={"13%"} src={heartIcon} alt="Live Heart of remaining tries" key={hearts.length} />);
        }

        if (hardcore) {
            if (maxLives === 5) {
                hearts.push(
                    <Tooltip title={t("goldenLocked")} followCursor>
                        <img className="heart" width={"13%"} src={heartGoldBlockedIcon} alt="Extra Live Heart locked" key={hearts.length} />
                    </Tooltip>
                );
            }

            if (maxLives === 6 && livesUsed < 1) {
                hearts.pop();
                hearts.push(
                    <Tooltip title={t("goldenUnlocked")} followCursor>
                        <img className="heart" width={"13%"} src={heartGoldIcon} alt="Extra Live Heart unlocked" key={hearts.length} />
                    </Tooltip >
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