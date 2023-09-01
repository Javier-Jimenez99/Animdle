import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";
import { useParams } from "react-router-dom";

function EndingPage() {
    const actual_mode = "Endings Wordle";
    const date = useParams().date;
    return (
        <div className="main-page ending">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"ending"} date={date} />
        </div>
    )
}

export default EndingPage; 