function saveToken(data) {
    if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
    }
}

async function apiRequest(url, options = {}) {
    const token = localStorage.getItem("access_token");

    options.headers = options.headers || {};

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}