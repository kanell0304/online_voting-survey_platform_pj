import React, { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import axios from 'axios';
import FormRenderer from '../Forms/FormRenderer';

export default function ResponsePage() {
  const location = useLocation();
  const { formId } = useParams();
  const [form, setForm] = useState(location.state || { title: "", questions: [] });

  useEffect(() => {
    if(!location.state && formId){
      (async ()=>{
        try{
          const res = await axios.get(`http://localhost:8081/surveys/${formId}`);
          console.log(`res: ${res}`);
          setForm(res.data);
        } catch(err){
          console.error("정보 가져오는데 오류", err);
        }
      })();
    }
  }, [location.state, formId]);

  const submitResponse = async (answers)=>{
    try{
      const payload={
        survey_id: form.survey_id,
        user_id: null,
        details: Object.entries(answers).map(([index, value])=>{
          const question = form.questions[index];
          return{
            question_id: question.question_id,
            selected_option_id:
              question.type === "choice"
                ? question.options.find(opt=>opt === value)?.id || null
                : null,
            text_response: question.type === "text" ? value : null
          };
        })
      };
      await axios.post("http://localhost:8081/responses/create", payload);
      alert("응답이 성공적으로 제출되었습니다.");
    }
    catch(err){
      if(err.response){
        console.error("서버 응답:", err.response.data);
        console.log("응답 제출 실패: " + JSON.stringify(err.response.data));
        // alert("응답 제출 실패: " + JSON.stringify(err.response.data));
      } else{
        alert("서버 오류로 제출에 실패했습니다.");
      }
    }
  };

  return(
    <div>
      <FormRenderer form={form} onSubmit={submitResponse} />
    </div>
  );
}