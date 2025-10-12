import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function SignupPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [nickname, setNickname] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }
    // TODO: 실제 회원가입 API 연동 로직 구현
    console.log({ email, password, nickname });
    alert('회원가입 완료! 로그인 페이지로 이동합니다.');
    navigate('/login'); // 회원가입 성공 후 로그인 페이지로 이동
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-neutral-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white border rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center">회원가입</h2>
        <form onSubmit={handleSignup} className="space-y-4">
          <div>
            <input type="email" placeholder="이메일" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="password" placeholder="비밀번호" value={password} onChange={(e) => setPassword(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="password" placeholder="비밀번호 확인" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <input type="text" placeholder="닉네임" value={nickname} onChange={(e) => setNickname(e.target.value)} required className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <button type="submit" className="w-full px-4 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600">
            회원가입
          </button>
        </form>
         <div className="text-sm text-center text-gray-500">
          계정이 이미 있으신가요? <Link to="/login" className="text-blue-500 hover:underline">로그인</Link>
        </div>
      </div>
    </div>
  );
}