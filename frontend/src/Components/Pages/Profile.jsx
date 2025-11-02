import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Profile() {

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: ''
  });
  const [userId, setUserId] = useState(null);
  const [profileImage, setProfileImage] = useState(null); //이미지를 위한 용도
  const navigate = useNavigate()

  useEffect(() => {
    // 로그인한 사용자 정보 가져오기
    axios.get('http://localhost:8081/users/userme', {withCredentials: true})
      .then(res => {
        setFormData({
          email: res.data.email,
          username: res.data.username,
          password: ''
        });
        setUserId(res.data.user_id); // user_id 저장
      })
  }, []);

  const handleChange = (e)=>{
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  //이미지 변경하는 함수 필요
  const handleImageChange = ()=>{

  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      await axios.patch(`http://localhost:8081/users/${userId}`, formData, {withCredentials: true});

      // 이미지 업로드 부분 작성해야함

      alert('정보가 업데이트되었습니다');
      navigate('/');
      window.location.reload();
    } catch(err){
      console.error('업데이트 실패:', err);
      alert('정보 업데이트에 실패했습니다.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-md shadow-md flex gap-8">
      {/* 이미지 변경 */}
      <div className="flex flex-col items-center w-1/3">
        {/* 원형 이미지 박스 */}
        <div className="w-40 h-40 mb-4 border rounded-full overflow-hidden bg-gray-100 flex items-start justify-center pt-4">
        
        </div>
        {/* 이미지 변경 버튼 */}
        
      </div>

      {/* 구분선 */}
      <div className="border-l border-gray-300 h-auto mx-4"></div>

      {/* 개인정보 수정 폼 */}
      <div className="flex-1">
        <h2 className="text-2xl font-bold mb-4">개인정보 수정</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-700">이메일<span className="text-rose-500 ml-1 text-xs align-super">*</span></label>
            <input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-3 py-2 border rounded-md" required/>
          </div>

          <div>
            <label className="block text-gray-700">사용자명<span className="text-rose-500 ml-1 text-xs align-super">*</span></label>
            <input type="text" name="username" value={formData.username} onChange={handleChange} className="w-full px-3 py-2 border rounded-md" required/>
          </div>

          <div>
            <label className="block text-gray-700">비밀번호<span className="text-rose-500 ml-1 text-xs align-super">*</span></label>
            <input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-3 py-2 border rounded-md" required/>
          </div>

          <button type="submit" className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700">변경하기</button>
        </form>
      </div>
    </div>
  );
}
