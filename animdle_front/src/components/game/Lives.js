import heartIcon from "../../assets/pixelart_icon/heart_icon.png";
import heartGreenIcon from "../../assets/pixelart_icon/heart_green_icon.png";
import "../../styles/Lives.css";

function Lives({ livesUsed, gameState, maxLives = 5 }) {

    const generateHearts = () => {
        let hearts = [];
        let keys = [];
        for (let i = livesUsed; i < maxLives; i++) {
            hearts.push(<img className="heart" width={"15%"} src={heartIcon} alt="Live Heart of lost tries" key={i} />);
            keys.push(i);
        }

        let loopStart = 0;
        if (gameState === "win") {
            hearts.push(<img className="heart" width={"15%"} src={heartGreenIcon} alt="Live Heart meaning that you won" key={maxLives} />);
            keys.push(maxLives);
            loopStart++;
        }

        for (let i = loopStart; i < livesUsed; i++) {
            hearts.push(<img className="heart dead-heart" width={"15%"} src={heartIcon} alt="Live Heart of remaining tries" key={i} />);
            keys.push(i);
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