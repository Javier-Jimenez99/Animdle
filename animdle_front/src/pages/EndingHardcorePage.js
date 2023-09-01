import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";
import { useParams } from "react-router-dom";

function EndingHardcorePage() {
    const date = useParams().date;
    const actual_mode = "Endings Hardcore";

    return (
        <div className="main-page ending-hardcore">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"hardcore-ending"} date={date} />
        </div>
    )
}

export default EndingHardcorePage; 