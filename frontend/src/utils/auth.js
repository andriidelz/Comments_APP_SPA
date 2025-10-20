import api from './axios.js';

export function setTokens(access, refresh) {
  localStorage.setItem('accessToken', access)
  localStorage.setItem('refreshToken', refresh)
}

export async function login(username, password) {
  try {
    const res = await api.post('/token/', { username, password });
    localStorage.setItem('accessToken', res.data.access);
    localStorage.setItem('refreshToken', res.data.refresh);
    return true;
  } catch (err) {
    console.error('Login failed:', err.response?.data || err.message);
    return false;
  }
}

export async function refreshAccessToken(refreshToken) {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  if (!res.ok) throw new Error("Failed to refresh token");
  const data = await res.json();
  localStorage.setItem("accessToken", data.access);
  return data.access;
}

export function getAccessToken() {
  return localStorage.getItem("accessToken");
}

export function getRefreshToken() {
  return localStorage.getItem("refreshToken");
}

export function logout() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
}

export async function autoLogin() {
  const username = import.meta.env.VITE_AUTOLOGIN_USER;
  const password = import.meta.env.VITE_AUTOLOGIN_PASS;

  if (!username || !password) {
    console.warn("Auto-login skipped: no credentials found in .env");
    return false;
  }

  const existingToken = getAccessToken();
  if (existingToken) {
    console.log("Existing token found — skipping auto-login");
    return true;
  }

  try {
    console.log("Performing auto-login...");
    const res = await api.post('/token/', { username, password }); 
    localStorage.setItem('accessToken', res.data.access);
    localStorage.setItem('refreshToken', res.data.refresh);
    console.log("Auto-login successful!");
    return true;
  } catch (err) {
    console.error("Auto-login failed:", err.response?.data || err.message);
    return false;
  }
}