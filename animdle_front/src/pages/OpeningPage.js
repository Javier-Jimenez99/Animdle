import "../styles/Pages.css";
import Navbar from "../components/Navbar";
import Game from "../components/Game";
import { useParams } from "react-router-dom";

function OpeningPage() {
    const actual_mode = "Openings Wordle";
    const date = useParams().date;
    return (
        <div className="main-page opening">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <Game mode={"opening"} date={date} />
        </div>
    )
}

export default OpeningPage; 