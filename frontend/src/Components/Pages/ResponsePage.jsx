import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import FormRenderer from '../Forms/FormRenderer';

export default function ResponsePage() {
  const location = useLocation();
  const form = location.state || { title: "", questions: [] };

  const [answers, setAnswers] = useState({});

  const handleChange = (idx, value) => {
    setAnswers({ ...answers, [idx]: value });
  };

  const submitResponse = async () => {
    try {
      const res = await fetch(`http://localhost:8000/responses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      });
      if (res.ok) {
        alert("Response submitted!");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <FormRenderer form={form} onSubmit={submitResponse} />
    </div>
  );
}
