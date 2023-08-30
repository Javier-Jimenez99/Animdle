import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";

function EndingPage() {
    const actual_mode = "Endings Wordle";
    return (
        <div className="main-page ending">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"ending"} />
        </div>
    )
}

export default EndingPage; 