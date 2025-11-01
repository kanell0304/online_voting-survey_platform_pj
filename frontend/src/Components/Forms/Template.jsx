import React from "react";
import { useNavigate } from "react-router-dom";

export default function Template({ formData, setFormData }) {
  const navigate = useNavigate();

  // 템플릿 데이터
  const data={
    인적사항:[
      {text: "이름을 입력해주세요", type: "단답형", is_required: true},
      {text: "성별을 선택해주세요", type: "객관식", is_required: true, options: ["남성", "여성"]},
      {text: "연령대를 선택해주세요", type: "객관식", is_required: true, options: ["10대", "20대", "30대", "40대 이상"]},
      {text: "주소를 입력해주세요", type: "단답형", is_required: false},
      {text: "핸드폰 번호를 입력해주세요", type: "단답형", is_required: false}
    ],

    강의평가: [
      {text: "강의 만족도를 평가해주세요", type: "객관식", is_required: true, options: ["매우 만족", "만족", "보통", "불만족"]},
      {text: "강의 내용이 실무에 도움이 되었나요?", type: "객관식", is_required: true, options:["네", "아니요"]},
      {text: "강의에 대한 추가 피드백을 작성해주세요", type: "단답형", is_required: false}
    ],

    고객만족도:[
      {text: "직원의 응대 태도에 만족하셨나요?", type:"객관식", is_required: true, options:["매우 만족", "만족", "보통", "불만족", "매우 불만족"]},
      {text: "가격 대비 만족도는 어떠셨나요?", type:"객관식", is_required: true, options:["매우 만족", "만족", "보통", "불만족", "매우 불만족"]},
      {text: "재방문 의사가 있나요?", type: "객관식", is_required: true, options: ["있음", "없음"]},
      {text: "개선이 필요하다고 느낀 점이 있나요?", type:"단답형", is_required: false}
    ],

    방문후기: [
      {text: "방문하신 날짜를 입력해주세요", type:"단답형", is_required: true},
      {text: "매장 청결 상태는 어땠나요?", type:"객관식", is_required: true, options:["매우 만족", "만족", "보통", "불만족", "매우 불만족"]},
      {text: "직원의 친절도는 어땠나요?", type:"객관식", is_required: true, options:["매우 만족", "만족", "보통", "불만족", "매우 불만족"]},
      {text: "방문 후 느낀 점을 작성해주세요", type: "단답형", is_required: false},
      {text: "주변 지인에게 이곳을 추천하고 싶나요?", type: "객관식", is_required: false, options:["네", "아니요"]},
      {text: "추천 의사가 있나요?", type: "객관식", is_required: true, options: ["추천함", "추천하지 않음"]}
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