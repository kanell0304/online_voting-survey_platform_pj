import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import logo from '../../assets/logo.jpg'
import defaultProfile from '../../assets/defaultProfile.png';

export default function Header() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [profileImage, setProfileImage] = useState(defaultProfile); //현재 이미지 고정값으로 들어감 -> useeffect에 이미지가 존재하면 변경되게 코드 수정 필요

  //로그인 여부 확인, 유저네임 가져오기
  useEffect(()=>{
    const token = document.cookie.split("; ").find(x => x.startsWith("access_token"));
    console.log(token)
    if(token){
      (async () => {
        try{
          setIsLoggedIn(true);
          const res = await axios.get(`http://localhost:8081/users/profile`, {withCredentials: true});
          setUsername(res.data.username)
          if(res.data.profile_image_url) {
            setProfileImage(`http://localhost:8081${res.data.profile_image_url}`);
          }
        } catch(err){
          console.error("정보 가져오기 실패:", err);
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
      setProfileImage(defaultProfile);
      alert('로그아웃 되었습니다.');
      navigate('/');
    } catch(err){
      // console.error("로그아웃 실패:", err);
      setIsLoggedIn(false);
      setUsername("");
      setProfileImage(defaultProfile);
      alert('로그아웃 처리 중 오류가 발생했습니다.');
      navigate('/');
    }
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/"><img src={logo} alt="formz logo" className='w-30' /></Link>

          <nav className="flex items-center space-x-4">
            {isLoggedIn ? (
              <div className='flex items-center'>
                <img src={profileImage} alt="프로필" className="w-5 h-5 rounded-full border object-cover cursor-pointer" onClick={()=>navigate('/profile')} onError={(e) => {e.target.src = defaultProfile}}/>
                <span className=" font-bold px-3 py-2 text-sm">{username}님</span>
                <Link to="/my-surveys" className="hover:text-blue-600 font-medium px-3 py-2 text-sm">나의 설문</Link>
                <button onClick={handleLogout} className="px-3 py-2 text-sm font-medium hover:text-blue-600 cursor-pointer">로그아웃</button>
              </div>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium px-3 py-2 text-sm">로그인</Link>
                <Link to="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 shadow-sm text-sm">회원가입</Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}