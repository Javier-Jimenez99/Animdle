import axios from 'axios';
import { API_BASE_URL } from '../constants';

function prepareDate(date) {
    if (!date) {
        const now = new Date();
        const japanTime = new Date(
            now.toLocaleString('en-US', { timeZone: 'Asia/Tokyo' })
        );
        date = japanTime.getFullYear();
        date += "-" + (japanTime.getMonth() + 1).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false, timeZone: "Asia/Tokyo" });
        date += "-" + japanTime.getDate().toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false, timeZone: "Asia/Tokyo" });
    }

    return date;
}

axios.interceptors.response.use(
    response => response,
    async error => {
        if (error.response.status === 401) {
            // Creates a new guest user
            localStorage.clear();
            sessionStorage.clear();
            try {
                const token = await authGuest();
                return Promise.resolve({ data: { token } });
            }
            catch (error) {
                return Promise.reject(error);
            }

        }

        return Promise.reject(error);
    }
);

export const createGuest = async () => {
    try {
        const response = await axios.post(API_BASE_URL + 'api/create-guest/');
        return response.data;
    } catch (error) {
        console.log(error);
    }
}

export const authGuest = async () => {
    let browser_id = localStorage.getItem("browser_id");
    let token = sessionStorage.getItem("token");
    if (browser_id === null) {
        const response = await createGuest().catch(error => { console.log(error); });
        browser_id = response.browser_id;
        localStorage.setItem("browser_id", browser_id);
        token = response.token;
        sessionStorage.setItem("token", token);

    }

    // Check if it is already authenticated
    if (token === null) {
        try {
            const response = await axios.post(API_BASE_URL + 'api-token-auth/', { "username": "guest-" + browser_id, "password": "guest" });
            token = response.data.token;
            sessionStorage.setItem("token", token);
        } catch (error) {
            console.log(error);
        }
    }

    return token;
}

export const getGameState = async (mode, date) => {
    date = prepareDate(date);
    try {
        const token = await authGuest();
        const url = API_BASE_URL + 'api/game-state/' + mode + '/' + date + '/';
        const response = await axios.get(url, {
            headers: { "Authorization": "Token " + token }
        });
        return response.data;
    } catch (error) {
        console.log(error);
        return "error";
    }
}

export const postGuess = async (mode, date, title, maxLives = 5) => {
    date = prepareDate(date);
    try {
        const token = await authGuest();

        const url = API_BASE_URL + 'api/guess/' + mode + '/' + date + '/' + maxLives + '/';
        const response = await axios.post(url, { "title": title }, {
            headers: { "Authorization": "Token " + token }
        });
        return response.data;
    } catch (error) {
        console.log(error);
        return "error";
    }
}

export const getResults = async (mode, date) => {
    date = prepareDate(date);
    try {
        const token = await authGuest();

        const url = API_BASE_URL + 'api/results/' + mode + '/' + date + '/';

        const response = await axios.get(url, {
            headers: { "Authorization": "Token " + token }
        });

        return response.data;
    }
    catch (error) {
        console.log(error);
        return "error";
    }
}

export const getPlayedModes = async (date) => {
    date = prepareDate(date);
    try {
        const token = await authGuest();

        const url = API_BASE_URL + 'api/played-modes/' + date + '/';

        const response = await axios.get(url, {
            headers: { "Authorization": "Token " + token }
        });

        return response.data;
    }
    catch (error) {
        console.log(error);
        return "error";
    }
}