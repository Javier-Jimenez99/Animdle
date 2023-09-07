import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Fade from '@mui/material/Fade';
import DehazeRoundedIcon from '@mui/icons-material/DehazeRounded';

import '../styles/FadeMenu.css';
import { Link } from 'react-router-dom';
import { usePlayedModes } from '../App';
import Badge from '@mui/material/Badge';

export default function FadeMenu({ options }) {
    const { playedModes, setPlayedModes } = usePlayedModes();
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

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
                {options.map(({ id, name, icon, link }, index) => (
                    <MenuItem key={index}>
                        {console.log(playedModes, id, playedModes.includes(id), playedModes.includes(id) ? 0 : " 12321 ")}


                        <Link className="menu-link" to={link}>
                            <Badge badgeContent={!playedModes.includes(id) ? "!" : 0} invisible={playedModes.includes(id)} color='error'>
                                <img className="menu-icon" src={icon} alt={name + " icon"} />
                            </Badge>
                            {name}
                        </Link>


                    </MenuItem>
                ))}
            </Menu>
        </div >
    );
}