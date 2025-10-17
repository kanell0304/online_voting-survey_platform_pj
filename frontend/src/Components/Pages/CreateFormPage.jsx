import React from 'react';
import { useNavigate } from 'react-router-dom';
import FormBuilder from '../Forms/FormBuilder';

export default function CreateFormPage({ formData, setFormData }) {
  const navigate = useNavigate();

  const saveToServer = async (form) => {
    //첫번째 confirm
    const ok = window.confirm("이대로 폼을 제출하시겠습니까?");
    if(!ok) return;
    
    //true이면 밑에 코드 실행
    const payload = {
      title: form.title,
      description: "객관식과 주관식이 혼합된 설문입니다", //임시값
      expire_at: "2025-12-31T23:59:59Z", //임시값
      questions: form.questions.map((q)=>({
        question_text: q.text,
        question_type: q.type === "단답형" ? "short_text" : "choice",
        options: q.options?.map((opt)=>({option_text:opt})) || [],
      })),
    };

    try{
      const res = await fetch("http://localhost:8081/surveys",{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload),
      });

      if(res.ok){
        alert("성공적으로 저장되었습니다!");
        // 두번째 confirm
        if(confirm("배포 페이지로 이동하시겠습니까?")){
          navigate("/distribute");
          return;
        }
        navigate("/my-surveys");
      }
      else{
        const msg = await res.text();
        alert("서버 오류: " + msg);
      }
    }
    catch(err){
      console.error(err);
      alert("서버 연결에 실패했습니다.");
    }
  };

  return(
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <FormBuilder formData={formData} setFormData={setFormData} onSave={saveToServer} />
      </div>
    </div>
  );
}