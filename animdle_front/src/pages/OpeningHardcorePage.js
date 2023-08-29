import "../styles/Pages.css";
import Navbar from "../components/Navbar";

function OpeningHardcorePage() {
    const actual_mode = "Openings Hardcore";
    return (
        <div className="main-page opening-hardcore">
            <Navbar colors={["#fbede4", "#dd6559", "#e4a892"]} actual_mode={actual_mode} />
            <div>
            </div>
        </div>
    )
}

export default OpeningHardcorePage; 