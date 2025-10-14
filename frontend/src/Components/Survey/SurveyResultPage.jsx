import React, { useState } from 'react';

// 초기값 비워둠
const mockResultData = {
    respondents: '???',
    completionRate: '???',
    responseCount: '???',
    avgTime: '??:??',
    descriptionItems: [
        "설문 결과 분석에 대한 기본적인 안내 내용이 표시되는 곳입니다.",
        "각 통계 항목에 대한 자세한 설명이나 참고 사항을 여기에 기입할 수 있습니다.",
    ]
};

export default function SurveyResultPage() {
    const [activeTab, setActiveTab] = useState('response'); 
    
    const { respondents, completionRate, responseCount, avgTime, descriptionItems } = mockResultData;

    const handleTabChange = (tabName) => {
        setActiveTab(tabName);
    };

    // 좌측 상단 탭 버튼
    // 활성일 때: 회색 배경, 비활성일 때: 흰색 배경
    const getTabClass = (tabName) => {
        const baseClasses = "px-5 py-2 font-medium border border-gray-300 transition-colors text-gray-700";
        
        if (tabName === 'response') {
            return `${baseClasses} rounded-l-md border-r-0 ${
                activeTab === 'response' ? 'bg-neutral-200 text-gray-800 border-gray-400 z-10' : 'bg-white hover:bg-neutral-100'
            }`;
        } else {
            return `${baseClasses} rounded-r-md ${
                activeTab === 'statistics' ? 'bg-neutral-200 text-gray-800 border-gray-400 z-10' : 'bg-white hover:bg-neutral-100'
            }`;
        }
    };
    
    // 우측 상세 내용 탭
    const getDetailTabClass = (tabName) => {
        const baseClasses = "pb-2 px-3 text-lg cursor-pointer transition-colors";
        return activeTab === tabName
            ? `${baseClasses} font-semibold text-green-600 border-b-2 border-green-600`
            : `${baseClasses} text-gray-600 hover:text-gray-800`;
    };


    return (
        // 전체 배경 및 컨테이너
        <div className="min-h-screen bg-neutral-50 py-8">
            <div className="max-w-6xl mx-auto px-4"> 
                
                <div className="flex flex-col md:flex-row gap-8">
                    
                    {/* -------------------- 좌측 영역: 요약 및 액션 -------------------- */}
                    <div className="w-full md:w-1/3 min-w-[300px]"> 
                        
                        <h1 className="text-3xl font-bold text-gray-800 mb-1">
                            설문명: [설문 제목]
                        </h1>
                        <p className="text-base text-gray-500 mb-6">
                            총 {respondents}명 응답 | 완료율 {completionRate}%
                        </p>

                        {/* 좌측 상단 탭 버튼 그룹 */}
                        <div className="flex mb-8 relative z-0">
                            <button 
                                className={getTabClass('response')} 
                                onClick={() => handleTabChange('response')}
                            >
                                응답
                            </button>
                            <button 
                                className={getTabClass('statistics')} 
                                onClick={() => handleTabChange('statistics')}
                            >
                                통계
                            </button>
                        </div>
                        
                        {/* 요약 카드 그룹 */}
                        <div className="flex flex-col gap-4 mb-8">
                            <div className="p-4 rounded-lg shadow-sm bg-neutral-100">
                                <p className="text-sm text-gray-600">총 응답 수:</p>
                                <p className="text-4xl font-extrabold text-gray-800">{responseCount}</p>
                            </div>
                            <div className="p-4 rounded-lg shadow-sm bg-neutral-100">
                                <p className="text-sm text-gray-600">설문 완료율:</p>
                                <p className="text-4xl font-extrabold text-gray-800">{completionRate}%</p>
                            </div>
                            <div className="p-4 rounded-lg shadow-sm bg-neutral-100">
                                <p className="text-sm text-gray-600">평균 소요 시간:</p>
                                <p className="text-4xl font-extrabold text-gray-800">{avgTime}</p>
                            </div>
                        </div>

                        {/* 다운로드 및 공유 버튼 그룹 */}
                        <div className="flex flex-wrap gap-3">
                            <button className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 transition-colors">
                                CSV 다운로드
                            </button>
                            <button className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 transition-colors">
                                Excel 다운로드
                            </button>
                            <button className="px-4 py-2 text-sm text-blue-600 font-semibold bg-transparent hover:bg-blue-50 rounded-md transition-colors">
                                내 결과 공유하기
                            </button>
                        </div>
                    </div>
                    
                    {/* -------------------- 우측 영역: 상세 내용 -------------------- */}
                    <div className="w-full md:w-2/3">

                        {/* 설명 박스 */}
                        <div className="p-5 bg-white border rounded-lg shadow-md mb-8">
                            <h3 className="font-bold text-lg border-b pb-2 mb-3">상세 내용</h3>
                            <ul className="space-y-1 text-sm text-gray-700 list-disc list-inside">
                                {descriptionItems.map((item, index) => (
                                    <li key={index}>
                                        <span className="font-bold mr-1">■</span> {item}
                                    </li>
                                ))}
                                <li className="text-red-500 font-semibold">
                                    <span className="font-bold mr-1">■</span> 주의해야 할 중요한 내용은 빨간색으로 강조
                                </li>
                            </ul>
                        </div>

                        {/* 상세 내용 헤더 */}
                        <div className="mb-4">
                            <h2 className="text-xl font-bold text-gray-800 mb-3">
                                {activeTab === 'response' ? '상세 응답 [???]개' : '상세 통계 분석'}
                            </h2> 
                            
                            <div className="flex border-b-2 border-gray-200 relative">
                                {/* 우측 상세 탭 메뉴 */}
                                <span 
                                    className={getDetailTabClass('response')} 
                                    onClick={() => handleTabChange('response')}
                                >
                                    응답
                                </span>
                                <span 
                                    className={getDetailTabClass('statistics')} 
                                    onClick={() => handleTabChange('statistics')}
                                >
                                    통계
                                </span>
                                <button className="absolute right-0 top-1 px-3 py-1 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700 transition-colors">
                                    전체 보기
                                </button>
                            </div>
                        </div>

                        {/* -------------------- 탭 내용: 조건부 렌더링 -------------------- */}
                        {activeTab === 'response' ? (
                            // 응답 탭 내용
                            <div className="p-5 bg-white border rounded-lg shadow-md">
                                <h3 className="text-lg font-semibold">개별 응답 목록</h3>
                                <div className="mt-4 h-64 flex items-center justify-center text-gray-500">
                                    개별 응답을 확인할 수 있는 목록/뷰어
                                </div>
                            </div>
                        ) : (
                            // 통계 탭 내용
                            <div className="p-5 bg-white border rounded-lg shadow-md">
                                <h3 className="text-lg font-semibold border-b pb-2 mb-4">통계</h3>
                                
                                <div className="flex space-x-6 text-sm text-gray-500 mb-6">
                                    <span>평균: ???점</span>
                                    <span>최저: ???점</span>
                                    <span>최고: ???점</span>
                                </div>
                                
                                <p className="font-semibold mb-4">응답 분포</p>
                                
                                {/* 차트 영역 */}
                                <div className="h-64 bg-gray-100 flex items-center justify-center text-gray-500 rounded-md">
                                    차트 라이브러리 영역
                                </div>
                            </div>
                        )}
                        {/* ------------------------------------------------------------------ */}

                    </div>
                </div>
            </div>
        </div>
    );
}