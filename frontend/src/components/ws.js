//  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwNDMzMTI0LCJpYXQiOjE3NjA0MzI4MjQsImp0aSI6IjZiOGNiM2U2MTgzNTRjZTA4OWU5YTA4NjRlZDZjOWVjIiwidXNlcl9pZCI6MX0.ytXvTdXmCAGstOiggdH6NOEC2NY2ialHGOjWFPLnXgM";

let socket = null;

export const connectWS = (token) => {
  if (socket) return socket; // already connected

  socket = new WebSocket(`ws://localhost:8000/ws/comments/?token=${token}`);

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
