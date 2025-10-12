import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Header() {
  const navigate = useNavigate();

  // 🚨 중요: 이 부분은 나중에 실제 로그인 상태 관리 로직으로 대체해야 합니다.
  // (예: Context API, Redux, Zustand 등)
  // 지금은 UI 확인을 위해 false로 설정되어 있습니다. true로 바꾸면 로그인된 화면을 볼 수 있습니다.
  const isLoggedIn = false; 
  const userNickname = "김기현"; // 예시 닉네임

  const handleLogout = () => {
    // TODO: 실제 로그아웃 처리 로직 (서버에 요청, 토큰 삭제 등)
    alert('로그아웃 되었습니다.');
    navigate('/'); // 로그아웃 후 메인 페이지로 이동
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 1. 왼쪽: 로고 */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
              VOTING & SURVEY
            </Link>
          </div>

          {/* 2. 오른쪽: 네비게이션 및 인증 버튼 */}
          <nav className="flex items-center space-x-4">
            {isLoggedIn ? (
              // 로그인 상태일 때 보여줄 UI
              <>
                <Link 
                  to="/my-surveys" 
                  className="text-gray-600 hover:text-blue-600 transition-colors font-medium px-3 py-2 rounded-md text-sm"
                >
                  내 설문
                </Link>
                <span className="text-gray-700 font-semibold text-sm">{userNickname}님</span>
                <button 
                  onClick={handleLogout}
                  className="text-sm font-medium text-gray-500 hover:text-gray-700"
                >
                  로그아웃
                </button>
              </>
            ) : (
              // 비로그인 상태일 때 보여줄 UI
              <>
                <Link 
                  to="/login" 
                  className="text-gray-600 hover:text-blue-600 transition-colors font-medium px-3 py-2 rounded-md text-sm"
                >
                  로그인
                </Link>
                <Link 
                  to="/signup" 
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors shadow-sm font-medium text-sm"
                >
                  회원가입
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}