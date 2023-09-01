import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";
import { useParams } from "react-router-dom";

function OpeningHardcorePage() {
    const actual_mode = "Openings Hardcore";
    const date = useParams().date;
    return (
        <div className="main-page opening-hardcore">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"hardcore-opening"} date={date} />
        </div>
    )
}

export default OpeningHardcorePage; 