import React from 'react';
import OptionInput from './OptionInput';

export default function QuestionEditor({ question, onChange }) {
  const updateField = (field, value) => {
    onChange({ ...question, [field]: value });
  };

  const addOption = () => {
    updateField("options", [...(question.options || []), ""]);
  };

  const updateOption = (idx, value) => {
    const newOptions = [...question.options];
    newOptions[idx] = value;
    updateField("options", newOptions);
  };

  return (
    <div>
      <input placeholder="질문" value={question.text} onChange={(e)=>updateField("text", e.target.value)}/>

      <select value={question.type} onChange={(e)=>updateField("type", e.target.value)}>
        <option value="text">텍스트</option>
        <option value="choice">선택형</option>
      </select>

      {question.type === "choice" && (
        <div>
          {(question.options || []).map((opt, i) => (
            <OptionInput key={i} value={opt} onChange={(val)=>updateOption(i, val)} />
          ))}
          
          <button onClick={addOption}>+ 옵션 추가</button>
        </div>
      )}
    </div>
  );
}