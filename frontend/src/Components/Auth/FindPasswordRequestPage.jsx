// src/Components/Auth/FindPasswordRequestPage.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestPasswordReset } from '../../api/authApi.js'; 

export default function FindPasswordRequestPage() {
  const navigate = useNavigate();
  
  // 1. API 명세서에 필요한 3가지 값을 state로 관리합니다.
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    // 2. API 명세서에 맞는 Body 데이터를 준비합니다.
    const reqData = {
      email: email,
      username: username,
      phone_number: phoneNumber,
    };

    try {
      // 3. API "주문"
      const response = await requestPasswordReset(reqData);
      
      // 4. 성공
      console.log(response.data.message);
      alert('인증코드가 이메일로 전송되었습니다. 다음 단계로 이동합니다.');
      
      // 5. 2단계 페이지로 이동 (이메일 정보를 전달)
    
      navigate('/reset-password', { state: { email: email } });

    } catch (error) {
      // 6. 실패 (500 에러 등)
      console.error('인증코드 요청 실패:', error);
      alert('인증코드 요청에 실패했습니다. (정보가 일치하지 않음)');
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white border rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center">비밀번호 찾기</h2>
        <p className="text-center text-sm text-gray-500">가입 시 등록한 정보를 입력해 주세요.</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input type="email" placeholder="이메일 (email)" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="text" placeholder="사용자 이름 (username)" value={username} onChange={(e) => setUsername(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="tel" placeholder="전화번호 (phone_number)" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-4 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none disabled:bg-gray-400"
          >
            {isLoading ? '전송 중...' : '인증코드 전송'}
          </button>
        </form>
      </div>
    </div>
  );
}