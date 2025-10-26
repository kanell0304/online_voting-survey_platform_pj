import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { resetPassword } from '../../api/authApi.js'; // 경로 확인!

export default function FindPasswordResetPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email; 

  const [resetCode, setResetCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  if (!email) {
    // 사용자가 페이지를 새로고침하면 email 정보가 사라집니다.
    // 이 경우를 대비해 1단계로 돌려보냅니다.
    alert("잘못된 접근입니다. 이메일 인증부터 다시 시도해 주세요.");
    navigate('/find-password');
    return null; 
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      alert("새 비밀번호가 일치하지 않습니다.");
      return;
    }
    setIsLoading(true);

    // 3. API 명세서에 맞는 Body 데이터를 준비합니다.
    const resetData = {
      email: email,
      reset_code: resetCode, 
      new_password: newPassword,
    };

    // ----- (⭐️ 1. 디버깅용 console.log 추가! ⭐️) -----
    // F12 개발자 도구의 'Console' 탭에서 이 로그를 확인해 보세요!
  
    console.log("백엔드로 전송할 데이터 (Body):", JSON.stringify(resetData, null, 2));

    try {
     
      const response = await resetPassword(resetData);

    
      console.log(response.data.message);
      alert('비밀번호가 성공적으로 변경되었습니다. 로그인 페이지로 이동합니다.');
      navigate('/login');

    } catch (error) {
    
      console.error('비밀번호 변경 실패:', error);
      
    
      if (error.response) {
       
        console.error("서버 응답 에러:", error.response.data);
        alert(`비밀번호 변경 실패: ${error.response.data.detail || '서버 오류'}`);
      } else if (error.request) {
       
        console.error("서버 응답 없음:", error.request);
        alert("서버에 연결할 수 없습니다. CORS 또는 네트워크를 확인하세요.");
      } else {
        
        console.error("요청 설정 에러:", error.message);
        alert(`오류 발생: ${error.message}`);
      }
      
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white border rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center">비밀번호 변경</h2>
        <p className="text-center text-gray-600">{email}로 전송된 코드를 입력하세요.</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input type="text" placeholder="인증코드 (reset_code)" value={resetCode} onChange={(e) => setResetCode(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="password" placeholder="새 비밀번호 (new_password)" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="password" placeholder="새 비밀번호 확인" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-4 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none disabled:bg-gray-400"
          >
            {isLoading ? '변경 중...' : '비밀번호 변경'}
          </button>
        </form>
      </div>
    </div>
  );
}

