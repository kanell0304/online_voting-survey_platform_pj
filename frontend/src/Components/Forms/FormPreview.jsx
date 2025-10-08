import React from "react";
import { useNavigate } from "react-router-dom";

export default function FormPreview({ formData }) {
  const navigate = useNavigate();

  return (
    <div className="flex justify-center py-10 bg-gray-50 min-h-screen">
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-xl p-8 border border-gray-200 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{formData.title || "제목 없음"}</h1>
          <button onClick={() => navigate("/create")} className="text-blue-600 hover:underline">돌아가기</button>
        </div>

        {formData.questions.map((q, i) => (
          <div key={i} className="border-b pb-4 mb-4">
            <p className="font-semibold">
              {i + 1}.{q.text}
              {q.required && <span className="text-red-500 ml-1">*</span>}
            </p>

            {q.type === "단답형" ? (
              <input type="text" className="w-full border-b border-gray-400 mt-2 p-1 outline-none focus:border-blue-500" placeholder="답변을 입력하세요" />
            ) : (
              <div className="mt-2 space-y-1">
                {q.options.map((opt, j) => (
                  <label key={j} className="flex items-center space-x-2">
                    <input type="radio" name={`q${i}`} />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}