import React, { useState, useMemo } from 'react';

export default function FormRenderer({ form, onSubmit }) {
  const [answers, setAnswers] = useState({});

  const setAnswer = (idx, val) => {
    setAnswers(p => ({...p, [idx]:val}));
  };

  const handleSubmit = async () => {
    for(i=0; i < form.questions.length; i++){
      const q = form.questions[i];
      if(q.required){
        const a = answers[i];
        if(a === undefined || a === ""){
          alert("필수로 체크된 질문은 작성해주셔야 합니다");
          return;
        }
      }
    }
    if(onSubmit){
      await onSubmit(answers);
    }
  };

  return (
    <div className="min-h-screen py-8 bg-neutral-50">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
        <h2 className="text-2xl font-bold mb-4">{form.title}</h2>

        <div className="space-y-4">
          {form.questions.map((q, i)=>(
            <div key={i} className="p-4 border border-neutral-200 rounded">
              <div className="mb-2 font-medium">{i + 1}. {q.text} {q.required && <span className="text-red-600">(필수)</span>}</div>

              {q.type === "text" && (
                <input value={answers[i] || ""} onChange={(e) => setAnswer(i, e.target.value)} className="w-full p-2 border rounded" />
              )}

              {q.type === "choice" && (
                <div className="space-y-2">
                  {(q.options || []).map((opt, oi) => (
                    <label key={oi} className="flex items-center gap-3">
                      <input type="radio" name={`q-${i}`} value={opt} checked={answers[i] === opt} onChange={(e) => setAnswer(i, e.target.value)}/>
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-6 flex justify-end">
          <button onClick={handleSubmit} className="px-4 py-2 bg-blue-600 text-white rounded">제출</button>
        </div>
      </div>
    </div>
  );
}