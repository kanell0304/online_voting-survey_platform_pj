import React from 'react';
import { useNavigate } from 'react-router-dom';
import FormBuilder from '../Forms/FormBuilder';

export default function CreateFormPage({ formData, setFormData }) {
  const navigate = useNavigate();

  const saveToServer = async (form) => {
    const ok = window.confirm("이대로 폼을 제출하시겠습니까?");
    if (!ok) return;

    try {
      const res = await fetch("http://localhost:8000/forms", { //임시
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        alert("Form saved on server.");
      } else {
        alert("Failed to save form on server.");
      }
    } catch (err) {
      console.error(err);
      alert("Network error while saving form.");
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