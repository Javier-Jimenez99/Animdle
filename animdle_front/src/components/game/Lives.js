import heartIcon from "../../assets/pixelart_icon/heart_icon.png";
import "../../styles/Lives.css";

function Lives({ livesUsed, maxLives = 5 }) {
    const generateHearts = () => {
        let hearts = [];
        for (let i = livesUsed; i < maxLives; i++) {
            hearts.push(<img className="heart" width={"10%"} src={heartIcon} alt="Live Hearts" key={i} />);
        }

        for (let i = 0; i < livesUsed; i++) {
            hearts.push(<img className="heart dead-heart" src={heartIcon} alt="Dead Hearts" key={i} />);
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