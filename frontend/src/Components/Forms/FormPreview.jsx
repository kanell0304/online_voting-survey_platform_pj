import React from "react";
import { useNavigate } from "react-router-dom";

export default function FormPreview({ formData }) {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex justify-center py-12">
      <div className="w-full max-w-2xl bg-blue-100 shadow-lg rounded-xl p-8 border border-gray-200">
        
        {/* 제목, 돌아가기 */}
        <div className="h-2 bg-blue-600 w-full"/>
        <div className="p-5 bg-gray-100 border border-gray-300 mb-5">
        <h1 className="text-3xl p-1.5 font-semibold mb-3 text-gray-800">{formData.title || "제목 없음"}</h1>
        <p className="space-y-3 p-1.5 text-gray-800 text-sm">{formData.description || ""}</p>
        <button onClick={()=>navigate("/create")} className="pt-1.5 pr-1.5 pl-1.5 text-blue-600 hover:underline cursor-pointer text-xs">돌아가기</button>
        </div>
        
        {/* 질문 미리보기 */}
        {formData.questions.map((q, i)=>(
          <div key={i} className="pb-2 mb-2">
            <div className="p-5 bg-gray-50 rounded-xl border border-gray-300 hover:border-blue-400 transition">
            <p className="text-sm">
              {i + 1}.{q.text}
              {q.is_required && <span className="text-rose-500 ml-1 text-xs align-super">*</span>}
            </p>
            

            {/* 단답형/객관식 구분 */}
            {q.type === "단답형" ? (
              <input type="text" className="w-full border-b px-3 py-2 border-gray-400 mt-2 p-1 text-sm outline-none focus:border-blue-500" placeholder="답변을 입력하세요." />
            ) : (
              <div className="mt-2 space-y-2 text-sm p-2">
                {q.options.map((opt, j)=>(
                  <label key={j} className="flex items-center gap-2 cursor-pointer">
                    <input type="radio" name={`q${i}`} />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}