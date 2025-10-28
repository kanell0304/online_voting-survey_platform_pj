import React, { useEffect, useState } from 'react';
import { useLocation, useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import FormRenderer from '../Forms/FormRenderer';

export default function ResponsePage() {
  const location = useLocation();
  const {formId} = useParams();
  const [form, setForm] = useState(location.state || { title: "", description: "", questions: [] });
  const navigate = useNavigate();

  // get으로 특정 survey 정보가져오기
  useEffect(()=>{
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

  // front-backend
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
              question.question_type === "single_choice"
                ? question.options.find(opt=>opt.option_text === value)?.option_id || null
                : null,
            text_response: question.question_type === "short_text" ? (value || null) : null
          };
        })
      };
      await axios.post("http://localhost:8081/responses/create", payload, {withCredentials: false});
      alert("응답이 성공적으로 제출되었습니다.");
      navigate("/");
    }
    catch(err){
      if(err.response){
        console.error("서버 응답:", err.response.data);
        console.log("응답 제출 실패: " + JSON.stringify(err.response.data));
        // alert("응답 제출 실패: " + JSON.stringify(err.response.data));
      } else{
        // console.log(form);
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