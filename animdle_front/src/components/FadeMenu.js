import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Fade from '@mui/material/Fade';
import DehazeRoundedIcon from '@mui/icons-material/DehazeRounded';

import '../styles/FadeMenu.css';
import { Link } from 'react-router-dom';

export default function FadeMenu({ options }) {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    console.log(options);

    return (
        <div>
            <IconButton
                aria-label="more"
                id="long-button"
                aria-controls={open ? 'long-menu' : undefined}
                aria-expanded={open ? 'true' : undefined}
                aria-haspopup="true"
                onClick={handleClick}
            >
                <DehazeRoundedIcon id="icon-menu" />
            </IconButton>
            <Menu
                id="fade-menu"
                MenuListProps={{
                    'aria-labelledby': 'fade-button',
                }}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                TransitionComponent={Fade}
            >
                {options.map(({ name, link, icon }, index) => (
                    <MenuItem key={index}>
                        <Link className="menu-link" to={link}>
                            <img className="menu-icon" src={icon} alt={name + " icon"} />
                            {name}
                        </Link>
                    </MenuItem>
                ))}
            </Menu>
        </div>
    );
}