import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function MainPage() {
  const navigate = useNavigate();

  //로그인 유무 확인 후 로그인 되어있으면
  const CreateSurvey = () => {
    const token = document.cookie.split("; ").find(x => x.startsWith("access_token"));
      // console.log(`CreateFormPage_token: ${token}`);
      if(!token){
        alert('로그인 후 이용 가능합니다');
        navigate('/login')
        return
      }
      navigate('/create')
  }

  return (
    <div className="flex items-center justify-center m-30 bg-neutral-50">
      <div className="p-20 text-center bg-white border rounded-lg shadow-md">
        <h1 className="text-4xl font-bold text-blue-900 mb-3">All the forms, for mz</h1>
        <p className="text-gray-500 mb-10">쉽고 빠르게 만들고, 공유하고, 관리하세요. FORMZ는 당신을 위해 만들어졌습니다</p>
        <button onClick={()=>CreateSurvey()}className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">시작하기</button>
      </div>
    </div>
  );
}