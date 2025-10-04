import React from 'react';
import QuestionEditor from './QuestionEditor';
import { useNavigate } from 'react-router-dom';

export default function FormBuilder({ formData, setFormData, onSave }) {
  const navigate = useNavigate();

  const addQuestion = () => {
    setFormData({
      ...formData,
      questions: [...formData.questions, { text: "", type: "text", options: [] }]
    });
  };

  const updateQuestion = (idx, newQuestion) => {
    const newQuestions = [...formData.questions];
    newQuestions[idx] = newQuestion;
    setFormData({ ...formData, questions: newQuestions });
  };

  const updateTitle = (newTitle) => {
    setFormData({ ...formData, title: newTitle });
  };

  const handleSave = async () => {
    if (onSave) await onSave(formData);
  };

  const handlePreview = () => {
    navigate("/preview");
  };

  return (
    <div>
      <div>
        <input placeholder="제목 없는 양식" value={formData.title} onChange={(e)=>updateTitle(e.target.value)} />

        <div>
          {formData.questions.map((q, i) => (
            <QuestionEditor key={i} question={q} onChange={(newQ)=>updateQuestion(i, newQ)} />
          ))}
        </div>
        
        <div>
          <button onClick={addQuestion}>+ 새 질문 추가</button>
          <button onClick={handleSave}>저장</button>
          <button onClick={handlePreview}>미리보기</button>
        </div>

      </div>
    </div>
  );
}
