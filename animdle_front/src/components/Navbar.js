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
import { useTranslation } from "react-i18next";
import flagSpain from "../assets/flags/spain.png";
import flagUSA from "../assets/flags/usa.png";


function Navbar({ actual_mode, colors = ["#fbede4", "#dd6559", "#e4a892"] }) {
    const { t, i18n } = useTranslation('common');
    const gradient = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[1]} 100%)`;

    const modes = {
        "opening": {
            "id": "opening",
            "name": t("gameModes.opening"),
            "icon": templeIcon,
            "link": "/opening"
        },
        "hardcore-opening": {
            "id": "hardcore-opening",
            "name": t("gameModes.hardcore-opening"),
            "icon": darkDrakeIcon,
            "link": "/hardcore-opening"
        },
        "ending": {
            "id": "ending",
            "name": t("gameModes.ending"),
            "icon": lanternIcon,
            "link": "/ending"
        },
        "hardcore-ending": {
            "id": "hardcore-ending",
            "name": t("gameModes.hardcore-ending"),
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
                    <h2 className="logo-title" style={{ margin: 0 }}>ANIMDLE</h2>
                </div>
                <div className="navbar-title">
                    <h1>{modes[actual_mode].name}</h1>
                </div>
                <div className="navbar-end">
                    <div className="navbar-clock">
                        <Clock />
                    </div>
                    <FadeMenu options={options} />

                    <div className="language-selector">
                        <img
                            src={flagSpain}
                            alt="Spanish Language Icon"
                            onClick={() => i18n.changeLanguage('en')}
                            style={{ display: (i18n.language === 'es' ? 'initial' : 'none') }}
                        />
                        <img
                            src={flagUSA}
                            alt="English Language Icon"
                            onClick={() => i18n.changeLanguage('es')}
                            style={{ display: (i18n.language === 'en' ? 'initial' : 'none') }}
                        />
                    </div>
                </div>
            </nav>

            <Outlet />

        </div>
    );
}

export default Navbar;