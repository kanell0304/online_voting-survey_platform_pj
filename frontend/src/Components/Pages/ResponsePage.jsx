import React, { useEffect, useState } from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';
import FormRenderer from '../Forms/FormRenderer';

export default function ResponsePage() {
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const [form, setForm] = useState(location.state || {title: "", questions: []});

  useEffect(() => {
    const formId = searchParams.get("formId");
    if(!location.state && formId){
      (async () => {
        try {
          const res = await fetch(`http://localhost:8081/forms/${formId}`);
          if (res.ok) {
            const data = await res.json();
            setForm(data);
          }
        }
        catch(err){
          console.error("정보 가져오는데 오류", err);
        }
      })();
    }
  }, [location.state, searchParams]);

  const submitResponse = async (answers) => {
    try{
      const payload = {
        survey_id: form.survey_id,
        user_id: null,
        details: Object.entries(answers).map(([index, value])=>{
          const question = form.questions[index];
          return{
            question_id: question.question_id,
            selected_option_id:
              question.type === "choice"
                ? question.options.find(opt => opt === value)?.id || null
                : null,
            text_response: question.type === "text" ? value : null,
          };
        }),
      };

      const res = await fetch("http://localhost:8081/responses/create", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });

      if(res.ok){
        alert("응답이 성공적으로 제출되었습니다.");
      }
      else{
        const errText = await res.text();
        console.error("서버 응답:", errText);
        alert("응답 제출 실패");
      }
    }catch(err){
      console.error("제출 중 오류:", err);
      alert("서버 오류로 제출에 실패했습니다.");
    }
  };

  return(
    <div>
      <FormRenderer form={form} onSubmit={submitResponse} />
    </div>
  );
}