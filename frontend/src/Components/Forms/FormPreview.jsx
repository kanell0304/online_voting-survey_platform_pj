import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function FormPreview({ formData }) {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate(-1);
  };

  return (
    <div>
      <h2>{formData.title || "Untitled Form"}</h2>

      {formData.questions.length === 0 && (
        <p>No questions yet</p>
      )}

      {formData.questions.map((q, i) => (
        <div key={i}>

          <p>{q.text}</p>

          {q.type === "text" && (
            <input placeholder="Your answer" disabled />
          )}

          {q.type === "choice" && (
            <div>

              {q.options.map((opt, j)=>(
                <label key={j}>
                  <input type="radio" name={`q-${i}`} disabled />
                  <span>{opt}</span>
                </label>
              ))}

            </div>
          )}
          
        </div>
      ))}

      <button onClick={handleBack}>돌아가기</button>
    </div>
  );
}