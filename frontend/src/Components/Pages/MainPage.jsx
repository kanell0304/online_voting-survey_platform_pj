import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function MainPage() {
  const navigate = useNavigate();

  // 로그인된 상태에서만 설문생성 가능
  const CreateSurvey = () => {
    const token = document.cookie.split("; ").find(x => x.startsWith("access_token") == 0);
      // console.log(`CreateFormPage_token: ${token}`);
      if (!token) {
        alert('로그인 후 이용 가능합니다');
        return
      }
      navigate("/create");
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="p-20 text-center bg-white border rounded-lg shadow-md">
        <h2 className="text-3xl font-bold text-gray-700 mb-2">당신의 설문, 세상과 연결되다</h2>
        <p className="text-gray-500 mb-6">VOTING & SURVEY를 통해 당신의 아이디어가 모두의 의견과 만나는 순간을 기록하세요.</p>
        <button onClick={()=>CreateSurvey()}className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">지금 시작하기</button>
      </div>
    </div>
  );
}