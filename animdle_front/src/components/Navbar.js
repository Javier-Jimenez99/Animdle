import "../styles/Navbar.css";
import logo from "../assets/images/logo.png";
import Clock from "../components/Clock";

function Navbar({ colors }) {
    const gradient = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[1]} 100%)`;
    return (
        <nav className="navbar" style={{ background: gradient }}>
            <div className="navbar-logo">
                <img className="logo" src={logo} alt="Animdle Logo" />
                <h2>ANIMDLE</h2>
            </div>
            <div className="navbar-title">
                <h1>Openings Wordle</h1>
            </div>
            <div className="navbar-end">
                <div className="navbar-clock">
                    <Clock />
                </div>
            </div>
        </nav>
    );
}

export default Navbar;