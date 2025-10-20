export async function fetchComments(proxy, page = 1, sortBy = '-created_at') {
  if (!proxy) {
    console.error("Vue proxy instance required to access $api");
    return [];
  }

  try {
    const res = await proxy.$api.get(`/comments/?page=${page}&sort_by=${sortBy}`);
    return res.data;
  } catch (err) {
    console.error("Failed to fetch comments:", err.response?.data || err.message);
    return [];
  }
}

// import { getAccessToken, getRefreshToken, refreshAccessToken } from '../utils/auth';

// const API_URL = import.meta.env.VITE_API_URL
// const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// async function fetchComments() {
//   let token = getAccessToken();

//   try {
//     const res = await fetch(`${API_URL}/api/comments/`, {
//       headers: { Authorization: `Bearer ${token}` },
//     });

//     if (res.status === 401) { // token expired
//       token = await refreshAccessToken(getRefreshToken());
//       return fetch(`${API_URL}/api/comments/`, {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//     }

//     return res.json();
//   } catch (err) {
//     console.error("Failed to fetch comments:", err);
//   }
// }
