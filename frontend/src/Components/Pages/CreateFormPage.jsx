import React from 'react';
import FormBuilder from '../Forms/FormBuilder';

export default function CreateFormPage({ formData, setFormData }) {
  const saveForm = async (form) => {
    try {
      const res = await fetch("http://localhost:8000/forms", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        alert("Form saved!");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1 >Create Form</h1>
      <FormBuilder formData={formData} setFormData={setFormData} onSave={saveForm} />
    </div>
  );
}