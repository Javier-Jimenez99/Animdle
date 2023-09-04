import TwitterIcon from '@mui/icons-material/Twitter';
import FacebookIcon from '@mui/icons-material/Facebook';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';
import RedditIcon from '@mui/icons-material/Reddit';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import { IconButton } from "@mui/material";
import "../../styles/Share.css"
import "../../styles/utils.css"

function Share({ results, date }) {

    const generateMessage = () => {
        let message = "🌸 Animdle";

        message += "【" + (date ? date : new Date().toLocaleDateString()) + "】\n\n";

        for (let i = 0; i < results.attempts.length - 1; i++) {
            message += "💔";
        }

        message += results.state === "win" ? "💚" : "💔";

        for (let i = 0; i < 5 - results.attempts.length; i++) {
            message += "🤍";
        }

        message += "\n\n#animdle";

        return message;
    }

    const twitterMessage = encodeURIComponent(generateMessage(results) + "\n\n");
    const whatsappMessage = encodeURIComponent(generateMessage(results) + "\n\nhttps://animdle.com/");
    const urlToShare = encodeURIComponent("https://animdle.com/");

    const openPopup = (url) => {
        const width = 600;
        const height = 400;
        const left = (window.screen.width - width) / 2;
        const top = (window.screen.height - height) / 2;

        window.open(url, '', `toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=${width}, height=${height}, top=${top}, left=${left}`);
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(decodeURIComponent(urlToShare));
        alert('Link copied to clipboard!');
    };

    return (
        <div className="share-container round-border simple-shadow">
            <h3 className="share-title">Share your results!</h3>
            <div className="share-icons">
                <IconButton onClick={() => openPopup(`https://twitter.com/intent/tweet?text=${twitterMessage}&url=${urlToShare}`)}>
                    <TwitterIcon className="share-icon round-border" />
                </IconButton>
                <IconButton onClick={() => openPopup(`https://www.facebook.com/sharer/sharer.php?u=${decodeURIComponent(urlToShare)}`)}>
                    <FacebookIcon className="share-icon round-border" />
                </IconButton>
                <IconButton onClick={() => openPopup(`whatsapp://send?&text=${whatsappMessage}`)}>
                    <WhatsAppIcon className="share-icon round-border" />
                </IconButton>
                <IconButton onClick={() => openPopup(`https://www.reddit.com/submit?url=${decodeURIComponent(urlToShare)}&title=${twitterMessage}`)}>
                    <RedditIcon className="share-icon round-border" />
                </IconButton>
                <IconButton onClick={copyToClipboard}>
                    <FileCopyIcon className="share-icon round-border" />
                </IconButton>
            </div>
        </div>
    );
}

export default Share;
