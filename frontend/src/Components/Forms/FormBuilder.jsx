import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FormBuilder({ formData, setFormData }) {
  const navigate = useNavigate();
  
  // 질문 추가
  const addQuestion = () => {
    const nq = {text:"", type:"단답형", required:false, options:[]};
    setFormData({
      ...formData,
      questions:[...formData.questions, nq]
    });
  };

  // 질문 수정
  const updateQuestion = (idx, updated) => {
    const nq = [...formData.questions];
    nq[idx] = {...nq[idx], ...updated};
    setFormData({...formData, questions: nq});
  };

  // 질문 복사
  const copyQuestion = (idx) => {
    const nq = [...formData.questions];
    nq.splice(idx + 1, 0, {...nq[idx]});
    setFormData({...formData, questions: nq});
  };
  
  // 질문 삭제
  const deleteQuestion = (idx) => {
    const nq = formData.questions.filter((_, i) => i !== idx);
    setFormData({...formData, questions: nq});
  };

  // 폼 저장 한번 더 확인 //(테스트용 - 수정 예정)
  const handleSave = ()=> {
    if(confirm("이대로 폼을 제출하시겠습니까?")){
      alert("폼이 저장되었습니다(확인용 임시)");
    }
  };

  return (
    <div className="flex justify-center py-10 bg-gray-50 min-h-screen">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-8 space-y-6 border border-gray-200">

        {/* 상단 제목 + 미리보기 버튼 */}
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold">Create Form</h1>
          <button onClick={()=>navigate("/preview")} className="text-blue-600 hover:underline">미리보기</button>
        </div>

        {/* 폼 제목 입력 */}
        <input type="text" placeholder="제목 없는 양식" value={formData.title} onChange={(e)=>setFormData({ ...formData, title:e.target.value})} className="w-full border-b border-gray-400 text-lg p-2 outline-none focus:border-blue-500" />

        {/* 질문 리스트 */}
        {formData.questions.map((q, i) => (
          <div key={i} className="bg-[#f8f6ef] border border-gray-300 rounded-lg p-4 space-y-3">
            <div className="flex items-center space-x-3">

              {/* 질문 입력 */}
              <input type="text" placeholder="질문을 입력하세요" value={q.text} onChange={(e) => updateQuestion(i, { text: e.target.value })} className="flex-1 border-b border-gray-400 p-2 outline-none focus:border-blue-500" />

              {/* 질문 유형 선택(단답형, 객관식) */}
              <select value={q.type} onChange={(e) => updateQuestion(i,{type: e.target.value})} className="border rounded-md p-2">
                <option>단답형</option>
                <option>객관식</option>
              </select>
            </div>

            {q.type === "객관식" && (
              <div className="ml-2 space-y-2">
                {q.options.map((opt, j) => (
                  <div key={j} className="flex items-center space-x-2">
                    <input type="text" value={opt} placeholder="옵션 입력" onChange={(e) => {
                        const newOpts = [...q.options];
                        newOpts[j] = e.target.value;
                        updateQuestion(i, { options: newOpts });
                      }}
                      className="border-b flex-1 p-1" />
                    <button onClick={()=> {
                        const newOpts = q.options.filter((_, k) => k !== j);
                        updateQuestion(i, {options: newOpts});
                      }}
                      className="text-sm text-red-600 hover:underline">삭제</button>
                  </div>
                ))}
                <button onClick={()=>updateQuestion(i, {options:[...q.options, ""]})} className="text-blue-600 text-sm hover:underline">+ 옵션 추가</button>
              </div>
            )}

            {/* 필수선택, 복사, 삭제 버튼 */}
            <div className="flex items-center space-x-4 text-sm pt-2 border-t border-gray-300 mt-3">
              <label className="flex items-center space-x-1">
                <input type="checkbox" checked={q.required} onChange={(e)=>updateQuestion(i, { required: e.target.checked })} />
                <span>필수</span>
              </label>
              <button onClick={()=>copyQuestion(i)} className="hover:text-blue-600">복사</button>
              <button onClick={() => deleteQuestion(i)} className="hover:text-red-600">삭제</button>
            </div>
          </div>
        ))}

        <div className="flex justify-between pt-6">
          <button onClick={addQuestion} className="text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg">+ 새 질문 추가</button>
          <button onClick={handleSave} className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg">저장하기</button>
        </div>
      </div>
    </div>
  );
}