import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/';

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
    try {
        const token = await authGuest();
        let url;
        if (date === null) {
            url = API_BASE_URL + 'api/game-state/' + mode + '/';
        } else {
            url = API_BASE_URL + 'api/game-state/' + mode + '/' + date + '/';
        }
        const response = await axios.get(url, {
            headers: { "Authorization": "Token " + token }
        });
        return response.data;
    } catch (error) {
        console.log(error);
        return "error";
    }
}
