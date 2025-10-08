import React, { useEffect, useState } from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';
import FormRenderer from '../Forms/FormRenderer';

export default function ResponsePage() {
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const [form, setForm] = useState(location.state || { title: "", questions: [] });

  useEffect(() => {
    const formId = searchParams.get("formId");
    if (!location.state && formId) {
      (async () => {
        try {
          const res = await fetch(`http://localhost:8000/forms/${formId}`);
          if (res.ok) {
            const data = await res.json();
            setForm(data);
          }
        } catch (err) {
          console.error("정보 가져오는데 오류", err);
        }
      })();
    }
  }, [location.state, searchParams]);

  const submitResponse = async (answers) => {
    try {
      const payload = { form, answers };
      const res = await fetch("http://localhost:8000/responses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        alert("성공");
      } else {
        alert("실패");
      }
    } catch (err) {
      console.error(err);
      alert("제출 오류");
    }
  };

  return (
    <div>
      <FormRenderer form={form} onSubmit={submitResponse} />
    </div>
  );
}