import { getAccessToken } from '../utils/auth.js';

let socket = null;
/**
 * @param {Object} proxy
 */

export const connectWS = (proxy) => {
  if (!proxy) {
    console.error("Vue proxy instance required to access $api");
    return null;
  }

  const token = getAccessToken();
  if (!token) {
    console.error("No access token available");
    return null;
  }

  const API_URL = import.meta.env.VITE_API_URL.replace(/\/$/, '');
  let wsUrl = API_URL.replace('/api','').replace(/^http/, 'ws') + `/ws/comments/?token=${token}`;
  if (location.protocol === 'https:') wsUrl = wsUrl.replace(/^ws/, 'wss');
  socket = new WebSocket(wsUrl);

  socket.onopen = () => console.log("WebSocket connected!");
  socket.onclose = () => {
    console.log("WebSocket disconnected");
    socket = null;
  };
  socket.onerror = (err) => console.error("WebSocket error:", err);

  return socket;
};

/**
 * @param {Object} proxy 
 * @param {Object} message 
 */

export const sendMessage = async (proxy, message) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(message));
  } else {
    console.warn("WebSocket not connected, sending via HTTP as fallback");
    if (proxy) {
      try {
        await proxy.$api.post('/comments/', message);
      } catch (err) {
        console.error("Failed to send comment via $api:", err.response?.data || err.message);
      }
    }
  }
};

/**
 * @param {Function} callback
 */

export const onMessage = (callback) => {
  if (!socket) {
    console.warn("WebSocket not initialized");
    return;
  }
  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      callback(data);
    } catch (e) {
      console.error("Failed to parse WS message:", e);
    }
  };
};

export const disconnectWS = () => {
  if (socket) {
    socket.close();
    socket = null;
  }
};


// let socket = null;

// export const connectWS = (token) => {
//   if (socket) return socket;

//   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
//   // const API_URL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8000';
//   // const API_URL = import.meta.env.VITE_API_URL
//   // const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
//   const wsUrl = API_URL.replace(/^http/, 'ws') + `/ws/comments/?token=${token}`;

//   console.log("Connecting to WS:", wsUrl);

//   socket = new WebSocket(wsUrl);

//   socket.onopen = () => {console.log("WebSocket connected!");};
//   socket.onclose = () => {console.log("WebSocket disconnected"); socket = null;};
//   socket.onerror = (err) => {console.error("WebSocket error:", err);};

//   return socket;
// };

// export const sendMessage = (message) => {
//   if (!socket || socket.readyState !== WebSocket.OPEN) {
//     console.error("WebSocket not connected");
//     return;
//   }
//   socket.send(JSON.stringify(message));
// };

// export const onMessage = (callback) => {
//   if (!socket) return;
//   socket.onmessage = (event) => {
//     const data = JSON.parse(event.data);
//     callback(data.message);
//   };
// };
