import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";

function EndingHardcorePage() {

    const actual_mode = "Endings Hardcore";
    return (
        <div className="main-page ending-hardcore">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"hardcore-ending"} />
        </div>
    )
}

export default EndingHardcorePage; 