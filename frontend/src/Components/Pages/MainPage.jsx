import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function MainPage() {
  const navigate = useNavigate();

  // 로그인 여부에 따라 로그인이 되어있지 않으면 설문지 작성 페이지로 이동 불가
  const handleCreateSurveyClick = () => {
    const token = localStorage.getItem("access_token");
      // console.log(`CreateFormPage_token: ${token}`);
      if (!token) {
        alert('로그인 후 이용 가능합니다');
        return
      }
      navigate("/create");
  }

  return (
    // 화면 전체를 차지하도록 설정하고, 컨텐츠를 중앙 정렬합니다.
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="p-10 text-center bg-white border rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-700 mb-2">설문이 필요하신가요?</h2>
        <p className="text-gray-500 mb-6">당신만의 설문, 세상에 던져보세요</p>
        <button
          onClick={() => handleCreateSurveyClick()} // '설문 만들기' 페이지로 이동
          className="px-6 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors"
        >
          설문 만들기
        </button>
      </div>
    </div>
  );
}