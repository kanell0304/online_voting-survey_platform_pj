import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

export default function EditFormPage(){
  const navigate=useNavigate();
  const {formId} = useParams();

  const [formData, setFormData]=useState({
    title: "",
    description: "",
    expire_at: "",
    updated_at: "2025-10-24T06:46:27.373Z"
  });
  const [loading, setLoading] = useState(true);

  useEffect(()=>{
    (async () =>{
      try{
        const res = await axios.get(`http://localhost:8081/surveys/${formId}`, {withCredentials: true});
        const{title, description, expire_at} = res.data;
        const expired_at = typeof expire_at === "string" && expire_at.includes("T") ? expire_at.split("T")[0].slice(0, 10) : expire_at || "";
        setFormData({title, description, expire_at: expired_at});
        setLoading(false);
      } catch(err){
        console.error("설문 불러오기 실패:", err);
        // navigate("/my-surveys");
      }
    })();
  }, [formId, navigate]);

  const handleSave = async ()=>{
    try{
      const payload={
        title: formData.title,
        description: formData.description,
        expire_at: formData.expire_at,
        updated_at: new Date().toISOString(),
      };

      await axios.patch(`http://localhost:8081/surveys/${formId}`, payload, {withCredentials: true});
      alert("설문이 성공적으로 수정되었습니다!");
      navigate("/my-surveys");
    } catch (err) {
      console.error("설문 수정 실패:", err.response?.data || err);
      alert("설문 수정 실패: " + JSON.stringify(err.response?.data || "서버 오류"));
    }
  };

  if (loading) return <div className="text-center py-20">Loading...</div>;

  return (
    <div className="min-h-screen bg-neutral-50 py-8 flex justify-center">
      <div className="w-full max-w-2xl bg-gray-50 shadow-lg rounded-xl p-8 border border-gray-200 space-y-6">
        <h1 className="text-2xl font-bold">설문 수정</h1>

        <div className="space-y-4">
          <div>
            <h3 className="block mb-1 font-semibold">제목</h3>
            <input type="text" value={formData.title} onChange={(e)=>setFormData({...formData, title: e.target.value})} className="w-full border-b border-gray-400 p-2 outline-none focus:border-blue-500" />
          </div>

          <div>
            <h3 className="block mb-1 font-semibold">설문 설명</h3>
            <input type='text' value={formData.description} onChange={(e)=>setFormData({...formData, description: e.target.value})} className="w-full border-b border-gray-400 p-2 outline-none focus:border-blue-500" />
          </div>

          <div>
            <h3 className="block mb-1 font-semibold">마감일</h3>
            <input type="date" value={formData.expire_at} onChange={(e)=>setFormData({...formData, expire_at: e.target.value})} className="w-full border-b border-gray-400 p-2 outline-none focus:border-blue-500"/>
            <input type='date' value={formData.expire_at}></input>
            <p>{formData.expire_at}</p>
          </div>
        </div>

        <button onClick={handleSave} className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700">저장하기</button>

      </div>
    </div>
  );
}