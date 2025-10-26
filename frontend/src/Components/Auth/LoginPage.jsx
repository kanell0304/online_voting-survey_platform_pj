import React, { useState } from 'react';

import { Link, useNavigate } from 'react-router-dom';
import { login } from '../../api/authApi.js'; 
export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // API 연동된 handleLogin 함수 (async/await)
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login({ email, password });
      console.log('로그인 성공:', response.data);
      alert('로그인에 성공했습니다!');
      navigate('/my-surveys');
    } catch (error) {
      console.error('로그인 실패:', error);
      alert('이메일 또는 비밀번호가 올바르지 않습니다.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white border rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center">로그인</h2>
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <input
              type="email"
              placeholder="이메일"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="비밀번호"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none"
          >
            로그인
          </button>
        </form>
        <div className="text-sm text-center text-gray-500">
          <Link to="/signup" className="text-blue-500 hover:underline">회원가입</Link>
          {' | '}
        
          <Link to="/find-password" className="text-blue-500 hover:underline">비밀번호 찾기</Link>
        </div>
      </div>
    </div>
  );
}
