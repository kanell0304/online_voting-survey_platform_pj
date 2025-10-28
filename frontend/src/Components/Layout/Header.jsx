import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios'

export default function Header() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  //로그인 여부 확인, 유저네임 가져오기
  useEffect(()=>{
    const token = document.cookie.split("; ").find(x => x.startsWith("access_token") == 0);
    console.log(token)
    if(token){
      (async () => {
        try{
          setIsLoggedIn(true);
          const res = await axios.get(`http://localhost:8081/users/userme`, {withCredentials: true});
          setUsername(res.data.username)
        } catch(err){
          console.error("정보 가져오기 실패:", err)
        }
      })();
    }
    else{
        setIsLoggedIn(false);
    }
  }, [])

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:8081/users/logout', {}, {withCredentials: true});
      
      setIsLoggedIn(false);
      setUsername("");
      alert('로그아웃 되었습니다.');
      navigate('/');
    } catch(err){
      // console.error("로그아웃 실패:", err);
      setIsLoggedIn(false);
      setUsername("");
      alert('로그아웃 처리 중 오류가 발생했습니다.');
      navigate('/');
    }
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
          <nav className="flex items-center space-x-4">
            {/* 로그인 ture */}
            {isLoggedIn ? (
              <>
                <Link to="/my-surveys" className="text-gray-600 hover:text-blue-600 font-medium px-3 py-2 rounded-md text-sm">
                  내 설문
                </Link>
                <span className="text-gray-700 font-semibold text-sm">{username}님</span>
                <button onClick={handleLogout} className="text-sm font-medium text-gray-500 hover:text-blue-600">로그아웃</button>
              </>
            ) : (
              <>
              {/* 로그인 false */}
                <Link to="/login" className="text-gray-600 hover:text-blue-600 transition-colors font-medium px-3 py-2 rounded-md text-sm">
                  로그인
                </Link>
                <Link to="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors shadow-sm font-medium text-sm">
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