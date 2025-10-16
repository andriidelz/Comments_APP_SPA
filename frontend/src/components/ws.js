let socket = null;

export const connectWS = (token) => {
  if (socket) return socket;

  // const API_URL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8000';
  const API_URL = import.meta.env.VITE_API_URL
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
  const wsUrl = API_URL.replace(/^http/, 'ws') + `/ws/comments/?token=${token}`;
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log("WebSocket connected!");
  };

  socket.onclose = () => {
    console.log("WebSocket disconnected");
    socket = null;
  };

  socket.onerror = (err) => {
    console.error("WebSocket error:", err);
  };

  return socket;
};

export const sendMessage = (message) => {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    console.error("WebSocket not connected");
    return;
  }
  socket.send(JSON.stringify(message));
};

export const onMessage = (callback) => {
  if (!socket) return;
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    callback(data.message);
  };
};
