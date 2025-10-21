// src/api/authApi.js

import axios from 'axios';

// 1. axios 클라이언트를 생성합니다.
const apiClient = axios.create({
  // 백엔드 서버의 기본 주소
  baseURL: 'http://localhost:8081',
  
  // (가장 중요!) 모든 요청에 쿠키(access_token)를
  // 자동으로 포함시키기 위한 설정입니다.
  withCredentials: true,
  
  // 서버에 JSON 형식으로 데이터를 보낸다고 알려줍니다.
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 회원가입 API (POST /users/register)
 * @param {object} userData - { email, password, username, phone_number, role }
 */
export const signup = (userData) => {
  // apiClient가 /users/register 주소로 POST 요청을 보냅니다.
  return apiClient.post('/users/register', userData);
};

/**
 * 로그인 API (POST /users/login)
 * @param {object} credentials - { email, password }
 */
export const login = (credentials) => {
  // apiClient가 /users/login 주소로 POST 요청을 보냅니다.
  // 성공하면 브라우저가 알아서 쿠키를 저장합니다.
  return apiClient.post('/users/login', credentials);
};

// 나중에 다른 API 파일에서도 이 설정을 쓸 수 있게 export 합니다.
export default apiClient;