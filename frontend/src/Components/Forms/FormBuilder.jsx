import React from 'react';
import { useNavigate } from 'react-router-dom';
import Template from './Template';

export default function FormBuilder({formData, setFormData, onSave}) {
  const navigate = useNavigate();
  
  // 질문 추가
  const add = () => {
    const nq = {text:"", type:"단답형", is_required:false, options:[]};
    setFormData({...formData, questions:[...formData.questions, nq]});
  };

  // 질문 수정
  const update = (idx, updated) => {
    const nq = [...formData.questions];
    nq[idx] = {...nq[idx], ...updated};
    setFormData({...formData, questions: nq});
  };

  // 질문 복사
  const copy = (idx) => {
    const nq = [...formData.questions];
    nq.splice(idx + 1, 0, {...nq[idx]});
    setFormData({...formData, questions: nq});
  };
  
  // 질문 삭제
  const deleteQuestion = (idx) => {
    const nq = formData.questions.filter((_, i) => i !== idx);
    setFormData({...formData, questions: nq});
  };

  //모든 질문 삭제
  const deleteAll = () => {
    setFormData({...formData, questions: []});
  };

  // 폼 저장 / 우선 이대로 시도
  const save = () => {
    if (onSave) onSave(formData);
  };


  return (
    <div className="flex justify-center py-10 bg-gray-50 min-h-screen">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-8 space-y-6 border border-gray-200">

        {/* 상단 제목 + 미리보기 버튼 */}
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-semibold text-blue-600 text-shadow-2xs">Create Form</h1>
          <div className="flex space-x-2">
            <button onClick={()=>navigate("/templates")} className="hover:bg-blue-50 px-3 text-sm py-2 rounded-lg">템플릿</button>
            <button onClick={()=>navigate("/preview")} className="hover:bg-blue-50 px-3 text-sm py-2 rounded-lg">미리보기</button>
          </div>
        </div>

        {/* 폼 제목 입력 */}
        <input type="text" placeholder="제목 없는 양식" value={formData.title} onChange={(e)=>setFormData({ ...formData, title:e.target.value})} className="w-full border-b border-gray-400 text-xl p-1 outline-none focus:border-blue-500" />
        <input placeholder="ex) 이 설문은 000에 관련된 설문입니다." value={formData.description} onChange={(e)=>setFormData({ ...formData, description:e.target.value})} className="w-full border-b text-sm border-gray-400 p-1 outline-none focus:border-blue-500" />

        {/* 질문 리스트 */}
        {formData.questions.map((q, i) => (
          <div key={i} className="bg-slate-50 border text-sm border-gray-300 rounded-lg p-4 space-y-3">
            <div className="flex items-center space-x-3">

              {/* 질문 입력 */}
              <input type="text" placeholder="질문을 입력하세요." value={q.text} onChange={(e) => update(i, { text: e.target.value })} className="flex-1 border-b border-gray-400 p-2 outline-none focus:border-blue-500" />

              {/* 질문 유형 선택(단답형, 객관식) */}
              <select value={q.type} onChange={(e) => update(i,{type: e.target.value})} className="border rounded-md p-2 text-xs">
                <option>단답형</option>
                <option>객관식</option>
              </select>
            </div>

            {q.type === "객관식" && (
              <div className="mx-4 space-y-2">
                {q.options.map((opt, j) => (
                  <div key={j} className="flex items-center space-x-2">
                    <input type="text" value={opt} placeholder="옵션 입력" onChange={(e) => {
                        const newOpts = [...q.options];
                        newOpts[j] = e.target.value;
                        update(i, { options: newOpts });
                      }}
                      className="border-b flex-1 p-1 text-xs" />
                    <button onClick={()=> {
                        const newOpts = q.options.filter((_, k) => k !== j);
                        update(i, {options: newOpts});
                      }}
                      className="text-xs hover:text-rose-500">삭제</button>
                  </div>
                ))}
                <button onClick={()=>update(i, {options:[...q.options, ""]})} className="text-blue-500 text-xs hover:underline">+ 옵션 추가</button>
              </div>
            )}

            {/* 필수선택, 복사, 삭제 버튼 */}
            <div className="flex items-center justify-between pt-2 border-t border-gray-300 mt-3">
              <label className="flex items-center space-x-1.5 cursor-pointer">
                <input type="checkbox" checked={q.is_required || false} onChange={(e)=>update(i, { is_required: e.target.checked ? true : false })} className="w-3.5 h-3.5 cursor-pointer" />
                <span className="text-xs leading-none">필수</span>
              </label>
              <div className="flex items-center space-x-4">
                <button onClick={()=>copy(i)} className="hover:text-blue-600 text-xs leading-none">복사</button>
                <button onClick={() => deleteQuestion(i)} className="hover:text-rose-500 text-xs leading-none">삭제</button>
              </div>
            </div>
          </div>
        ))}

        <div className="flex justify-between pt-6">
          <div className="flex space-x-2">
            <button onClick={add} className=" hover:bg-blue-50 px-3 py-2 text-sm rounded-lg">+ 새 질문 추가</button>
            <button onClick={deleteAll} className="hover:bg-rose-50 px-3 py-2 text-sm rounded-lg text-rose-500">전체삭제</button>
          </div>
          <button onClick={save} className="bg-blue-800 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">저장하기</button>
        </div>
      </div>
    </div>
  );
}