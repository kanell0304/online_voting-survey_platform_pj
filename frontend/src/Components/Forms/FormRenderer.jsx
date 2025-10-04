import React, { useState } from 'react';
import QuestionViewer from './QuestionViewer';

export default function FormRenderer({ form, onSubmit }) {
  const [answers, setAnswers] = useState({});

  const handleChange = (index, value) => {
    setAnswers({ ...answers, [index]: value });
  };

  const handleSubmit = async () => {
    if (onSubmit) await onSubmit(answers);
  };

  return (
    
    <div>
      <h2>{form.title}</h2>
      
      {form.questions.map((q, i)=>(
        <QuestionViewer key={i} question={q} answer={answers[i] || ""} onChange={(val)=>handleChange(i, val)} />
      ))}

      <button onClick={handleSubmit}>Submit</button>

    </div>
  );
}