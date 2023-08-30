import "../styles/Navbar.css";
import logo from "../assets/images/logo.png";
import Clock from "../components/Clock";
import FadeMenu from "../components/FadeMenu";
import templeIcon from '../assets/images/temple_icon.png';
import drakeIcon from '../assets/images/drake_icon.png';

function Navbar({ colors, actual_mode }) {
    const gradient = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[1]} 100%)`;

    const possibleModes = {
        "Openings Wordle": "/",
        "Openings Hardcore": "/openings-hardcore",
        "Endings Wordle": "/endings",
        "Endings Hardcore": "/endings-hardcore"
    };

    const possibleIcons = {
        "Openings Wordle": templeIcon,
        "Openings Hardcore": drakeIcon,
        "Endings Wordle": templeIcon,
        "Endings Hardcore": drakeIcon
    };

    const options = Object.entries(possibleModes)
        .filter(([mode]) => mode !== actual_mode)
        .map(([name, link]) => ({ name, link, icon: possibleIcons[name] }));


    return (
        <nav className="navbar" style={{ background: gradient }}>
            <div className="navbar-logo">
                <img className="logo" src={logo} alt="Animdle Logo" />
                <h2>ANIMDLE</h2>
            </div>
            <div className="navbar-title">
                <h1>{actual_mode}</h1>
            </div>
            <div className="navbar-end">
                <div className="navbar-clock">
                    <Clock />
                </div>
                <FadeMenu options={options} />
            </div>
        </nav>
    );
}

export default Navbar;