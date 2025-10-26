import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8081',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});


export const signup = (userData) => {
  return apiClient.post('/users/register', userData);
};


export const login = (credentials) => {
  return apiClient.post('/users/login', credentials);
};


export const requestPasswordReset = (reqData) => {
 
  return apiClient.post('/users/forgot-password', reqData);
};


export const resetPassword = (resetData) => {
  

  return apiClient.post('/users/reset-password', resetData);
};

export default apiClient;
