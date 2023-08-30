import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";

function OpeningPage() {
    const actual_mode = "Openings Wordle";
    return (
        <div className="main-page opening">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"opening"} />
        </div>
    )
}

export default OpeningPage; 