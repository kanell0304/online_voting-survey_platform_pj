import React from "react";
import { useNavigate } from "react-router-dom";

export default function Template({ formData, setFormData }) {
  const navigate = useNavigate();

  // 템플릿 데이터
  const data={
    인적사항:[
      {text: "이름을 입력하세요", type: "단답형", is_required: true},
      {text: "성별을 선택하세요", type: "객관식", is_required: true, options: ["남성", "여성"]},
      {text: "소속을 입력해주세요", type: "단답형", is_required: false},
    ],

    강의평가: [
      {text: "강의 만족도를 평가해주세요", type: "객관식", is_required: true, options: ["매우 만족", "만족", "보통", "불만족"]},
      {text: "강사에 대한 의견을 작성해주세요", type: "장문형", is_required: false},
    ],

    작업요청: [
      {text: "요청하실 작업 내용을 작성해주세요", type: "장문형", is_required: true},
      {text: "작업 긴급도는 어느 정도인가요?", type: "객관식", is_required: true, options: ["높음", "보통", "낮음"]},
    ],

    고객만족도:[
      {text: "서비스 만족도를 평가해주세요", type:"객관식", is_required: true, options:["매우 만족", "만족", "보통", "불만족"]},
      {text: "재방문 의사가 있나요?", type: "객관식", is_required: true, options: ["있음", "없음"]}
    ],

    방문후기: [
      {text: "방문 후 느낀 점을 작성해주세요", type: "장문형", is_required: false},
      {text: "추천 의사가 있나요?", type: "객관식", is_required: true, options: ["추천함", "추천하지 않음"]},
    ]
  };

  // 템플릿 가져오기(기존 질문 뒤 새로 추가 가능)
  const select = (name) => {
    setFormData({...formData, questions:[...formData.questions, ...data[name]]});
    navigate("/create");
  };

  return (
    <div className="min-h-screen flex py-10 bg-gray-50">
      <div className="w-full space-y-6">
        <h1 className="text-3xl font-bold text-center mb-6">템플릿 선택</h1>

        <div className="grid grid-cols-2 gap-6">
          {Object.keys(data).map((name)=>(
            <div key={name} onClick={()=>select(name)} className="cursor-pointer border rounded-lg p-6 hover:bg-blue-50 flex flex-col text-center">
              <h2 className="text-lg text-blue-700">{name}</h2>
              <p className="text-xs text-gray-500 mt-2">{data[name].length}개의 질문 포함</p>
            </div>
          ))}
        </div>
        <div className="text-center">
          <button onClick={()=>navigate("/create")} className="hover:bg-blue-50 text px-3 text-sm py-2 rounded-lg">돌아가기</button>
        </div>
      </div>
    </div>
  );
}