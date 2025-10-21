import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import FormBuilder from '../Forms/FormBuilder';

export default function CreateFormPage({ formData, setFormData }) {
  const navigate = useNavigate();

  const saveToServer = async (form) => {
    const ok = window.confirm("이대로 폼을 제출하시겠습니까?");
    if (!ok) return;

    const payload = {
      title: form.title,
      description: "객관식과 주관식이 혼합된 설문입니다",
      expire_at: "2025-12-31T23:59:59Z",
      questions: form.questions.map((q) => ({
        question_text: q.text,
        question_type: q.type === "단답형" ? "short_text" : "choice",
        options: q.options?.map((opt) => ({ option_text: opt })) || [],
      })),
    };

    try {
      const res = await axios.post("http://localhost:8081/surveys", payload);

      alert("성공적으로 저장되었습니다!");
      if (window.confirm("배포 페이지로 이동하시겠습니까?")) {
        navigate("/distribute");
        return;
      }
      navigate("/my-surveys");
    } catch (err) {
      if (err.response) {
        alert("서버 오류: " + err.response.data);
      } else {
        alert("서버 연결에 실패했습니다.");
      }
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <FormBuilder formData={formData} setFormData={setFormData} onSave={saveToServer} />
      </div>
    </div>
  );
}