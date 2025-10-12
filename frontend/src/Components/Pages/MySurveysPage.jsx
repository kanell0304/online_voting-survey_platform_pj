import React from 'react';

// 실제로는 API를 통해 받아올 데이터의 예시입니다.
const mockSurveys = [
  { id: 1, title: '고객 만족도 설문', createdAt: '2025-10-01' },
  { id: 2, title: '신제품 아이디어 조사', createdAt: '2025-10-05' },
  { id: 3, title: '팀 워크숍 장소 선호도', createdAt: '2025-10-11' },
  { id: 4, title: '웹사이트 사용성 평가', createdAt: '2025-10-12' },
];

export default function MySurveysPage() {
  return (
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">My Surveys</h1>
          <p className="text-gray-600">지금까지 만든 설문 목록입니다.</p>
        </div>

        {/* 설문 목록을 그리드 형태로 표시 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockSurveys.map((survey) => (
            <div key={survey.id} className="p-4 bg-white border rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-2">{survey.title}</h3>
              <p className="text-sm text-gray-500 mb-4">생성일: {survey.createdAt}</p>
              <div className="flex justify-end space-x-2">
                <button className="px-3 py-1 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700">
                  결과보기
                </button>
                <button className="px-3 py-1 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600">
                  공유하기
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}