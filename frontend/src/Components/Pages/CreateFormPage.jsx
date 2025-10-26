import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import FormBuilder from '../Forms/FormBuilder';

export default function CreateFormPage({ formData, setFormData }) {
  const navigate = useNavigate();

  const saveToServer = async (form)=>{
    const ok = window.confirm("이대로 폼을 제출하시겠습니까?");
    if(!ok)return;

    const payload={
      title: form.title,
      description: "객관식과 주관식이 혼합된 설문입니다",
      expire_at: "2025-12-31T23:59:59Z",
      questions: form.questions.map((q)=>({
        question_text: q.text,
        question_type: q.type === "단답형" ? "short_text" : "single_choice",
        is_required: q.is_required || false,
        options: q.options?.map((opt)=>({option_text: opt})) || [],
      }))
    };

    try{
      const token = localStorage.getItem("access_token");
      const res = await axios.post(
        "http://localhost:8081/surveys",
        payload,
        {withCredentials: true}
      ); //jwt가 쿠키로 오기때문에 credential true. 만약 여기서 false나오면 바로 catch문으로 이동

      alert("성공적으로 저장되었습니다!");
      if(window.confirm("공유 하시겠습니까?")){
        navigate(`/distribute/${res.data.survey_id}`); //배포페이지
        return;
      }
      navigate("/my-surveys"); // 배포로 안갈때

    }
    catch(err){
      console.error("서버 오류:", err);
      if(err.response){
        alert('로그인 후 이용 가능합니다')
        navigate("/login"); //로그인 안되면 바로 로그인창으로
      }
    }
  }

  return(
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <FormBuilder formData={formData} setFormData={setFormData} onSave={saveToServer} />
      </div>
    </div>
  );
}