import { useState } from "react";
import { useTranslation } from "react-i18next";

function Clock() {
    const { t } = useTranslation('common');
    let time = new Date().toLocaleTimeString()

    const [ctime, setTime] = useState(time)
    const UpdateTime = () => {
        const now = new Date();
        const japanTime = new Date(
            now.toLocaleString('en-US', { timeZone: 'Asia/Tokyo' })
        );

        const hoursLeft = 23 - japanTime.getHours();
        const minutesLeft = 59 - japanTime.getMinutes();
        const secondsLeft = 59 - japanTime.getSeconds();

        setTime(hoursLeft.toString().padStart(2, "0") + ":" + minutesLeft.toString().padStart(2, "0") + ":" + secondsLeft.toString().padStart(2, "0"))
    }
    setInterval(UpdateTime)

    return <h1>{t("time", { time: ctime })}</h1>;
}

export default Clock;