import React from 'react';

export default function QuestionViewer({ question, answer, onChange }) {
  return (
    <div>
      <p>{question.text}</p>
      
      {question.type === "text" && (
        <input value={answer} onChange={(e)=>onChange(e.target.value)} />
      )}

      {question.type === "choice" && (
        <div>
          {(question.options || []).map((opt, i) => (
            <label key={i}>
              <input type="radio" name={question.text} value={opt} checked={answer === opt} onChange={(e)=>onChange(e.target.value)} />
              <span>{opt}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}