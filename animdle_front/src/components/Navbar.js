import "../styles/Navbar.css";
import "../styles/Pages.css"
import logo from "../assets/logo.png";
import Clock from "../components/Clock";
import FadeMenu from "./FadeMenu";
import templeIcon from '../assets/pixelart_icon/temple_icon.png';
import darkDrakeIcon from '../assets/pixelart_icon/dark_drake_icon.png';
import whiteDrakeIcon from '../assets/pixelart_icon/white_drake_icon.png';
import lanternIcon from '../assets/pixelart_icon/lantern_icon.png';
import { Outlet } from "react-router-dom";
import { useRef } from "react";


function Navbar({ actual_mode, colors = ["#fbede4", "#dd6559", "#e4a892"] }) {
    const windowWidth = useRef(window.innerWidth);
    const gradient = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[1]} 100%)`;

    const modes = {
        "opening": {
            "name": "Openings Wordle",
            "icon": templeIcon,
            "link": "/opening"
        },
        "hardcore-opening": {
            "name": "Openings Hardcore",
            "icon": darkDrakeIcon,
            "link": "/hardcore-opening"
        },
        "ending": {
            "name": "Endings Wordle",
            "icon": lanternIcon,
            "link": "/ending"
        },
        "hardcore-ending": {
            "name": "Endings Hardcore",
            "icon": whiteDrakeIcon,
            "link": "/hardcore-ending"
        }
    }
    const options = Object.keys(modes).filter(mode => mode !== actual_mode).map(mode => modes[mode]);

    return (
        <div className={"main-page " + actual_mode}>
            <nav className="navbar" style={{ background: gradient }}>
                <div className="navbar-logo">
                    <img className="logo" src={logo} alt="Animdle Logo" />
                    <h2 style={{ margin: 0 }}>ANIMDLE</h2>
                </div>
                <div className="navbar-title">
                    <h1>{modes[actual_mode].name}</h1>
                </div>
                <div className="navbar-end">
                    {windowWidth.current > 1000 &&
                        <div className="navbar-clock">
                            <Clock />
                        </div>
                    }
                    <FadeMenu options={options} />
                </div>
            </nav>

            <Outlet />

        </div>
    );
}

export default Navbar;