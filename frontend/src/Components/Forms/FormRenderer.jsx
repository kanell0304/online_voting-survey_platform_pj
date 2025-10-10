import React, { useState, useMemo } from 'react';

export default function FormRenderer({ form, onSubmit }) {

  const [answers, setAnswers] = useState({});

  const setAnswer = (idx, val) => {
    setAnswers(p => ({...p, [idx]:val}));
  };

  // 필수 체크한 질문 안할 경우 alert
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
    <div className="min-h-screen bg-[#f5f5dc] flex justify-center py-12">
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-2xl p-8 border border-gray-200">

        {/* 제목 */}
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-800">{form.title || "제목 없음"}</h2>

        {/* 질문 영역 */}
        <div className="space-y-6">
          {form.questions.map((q, i)=>(
            <div key={i} className="p-5 bg-gray-50 rounded-xl border border-gray-300 hover:border-blue-400 transition">
              <div className="mb-3 font-semibold text-gray-800">
                {i + 1}. {q.text}{q.required && <span className="text-red-500 ml-1">(필수)</span>}
              </div>

              {/* 단답형 */}
              {q.type === "text" && (
                <input value={answers[i] || ""} placeholder="답변을 입력하세요" onChange={(e)=>setAnswer(i, e.target.value)} className="w-full px-3 py-2 border-b-2 border-gray-400 bg-transparent outline-none focus:border-blue-500 transition" />
              )}

              {/* 객관식 */}
              {q.type === "choice" && (
                <div className="mt-2 space-y-2">
                  {(q.options || []).map((opt, oi) => (
                    <label key={oi} className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name={`q-${i}`} value={opt} checked={answers[i] === opt} onChange={(e)=>setAnswer(i, e.target.value)} className="accent-blue-600" />
                      <span className="text-gray-700">{opt}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* 제출 */}
          <button onClick={handleSubmit} className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700 active:scale-95 transition">제출</button>
      </div>
    </div>
  );
}