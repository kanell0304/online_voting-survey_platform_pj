import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom'; 

// 백엔드 API 기본 URL
const API_BASE_URL = "http://localhost:8081/survey_stats";

// 날짜 포맷 변환 유틸리티 함수 (ISO 문자열 -> YYYY. MM. DD)
const formatDate = (isoString) => {
    if (!isoString) return '미정';
    try {
        const date = new Date(isoString);
        if (isNaN(date.getTime())) return '미정';
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}. ${month}. ${day}`;
    } catch (e) {
        return '미정';
    }
};

// 초기 데이터 구조
const initialData = {
    overall: {
        survey_title: '설문 결과 페이지', 
        distributed_count: '0', 
        response_count: '0',
        completion_rate: '0.00', 
        total_questions: '0', 
        single_choice_count: '0',
        short_text_count: '0', 
        created_at: null, 
        expire_at: null,
    },
    single_choice_questions: [],
    short_text_questions: [],
};

export default function SurveyResultPage() {
    
    // URL 파라미터에서 설문 ID 추출
    const { formId: survey_id } = useParams(); 
    const navigate = useNavigate();

    // survey_id가 없을 경우 에러 화면 표시
    if (!survey_id) {
        return (
            <div className="min-h-screen bg-neutral-50 py-8 flex justify-center items-center">
                <p className="text-xl text-red-500">
                    오류: 설문지 ID가 URL 경로에서 발견되지 않았습니다.
                    <br />
                    <span className="text-sm">현재 URL: {window.location.pathname}</span>
                </p>
            </div>
        );
    }

    // 상태 관리
    const [resultData, setResultData] = useState(initialData); 
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('response'); 
    const [activeResponseTab, setActiveResponseTab] = useState('single');

    // 컴포넌트 마운트 시 설문 결과 데이터 불러오기
    useEffect(() => {
        const fetchSurveyData = async () => {
            setIsLoading(true);
            setError(null);

            const token = localStorage.getItem("access_token");
            const API_URL = `${API_BASE_URL}/${survey_id}/complete`;

            try {
                const response = await axios.get(
                    API_URL,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            ...(token && { 'Authorization': `Bearer ${token}` })
                        },
                        withCredentials: true
                    }
                );
                
                if (response.data && response.data.success && response.data.data) {
                    setResultData(response.data.data);
                } else {
                    throw new Error("응답 데이터 구조가 올바르지 않습니다.");
                }

            } catch (err) {
                console.error("API 호출 실패:", err);
                
                let errorMessage = "데이터를 불러오는 중 오류가 발생했습니다.";
                
                if (err.response) {
                    const status = err.response.status;
                    const serverMessage = err.response.data?.message || err.response.data?.detail || '알 수 없는 오류';
                    
                    if (status === 401) {
                        errorMessage = `인증 오류 (401): 토큰이 만료되었거나 유효하지 않습니다.`;
                    } else if (status === 404) {
                        errorMessage = `설문지를 찾을 수 없습니다 (404). ID: ${survey_id}`;
                    } else {
                        errorMessage = `서버 오류 (${status}): ${serverMessage}`;
                    }
                } else if (err.request) {
                    errorMessage = "서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.";
                } else {
                    errorMessage = `오류: ${err.message}`;
                }
                
                setError(errorMessage);
                setResultData(initialData);
            }
            
            setIsLoading(false);
        };

        fetchSurveyData();
    }, [survey_id]);

    // API 응답 데이터 구조 분해
    const { overall, single_choice_questions, short_text_questions } = resultData;
    const { 
        survey_title, 
        distributed_count, 
        response_count, 
        completion_rate, 
        total_questions, 
        single_choice_count, 
        short_text_count, 
        created_at, 
        expire_at 
    } = overall;

    // 탭 전환 핸들러
    const handleTabChange = (tabName) => { setActiveTab(tabName); };
    const handleResponseTabChange = (tabName) => { setActiveResponseTab(tabName); };

    // 메인 탭 스타일 (응답/통계)
    const getTabClass = (tabName) => { 
        const baseClasses = "px-5 py-2 font-medium border border-gray-300 transition-colors text-gray-700";
        if (tabName === 'response') { 
            return `${baseClasses} rounded-l-md border-r-0 ${activeTab === 'response' ? 'bg-neutral-200 text-gray-800 border-gray-400 z-10' : 'bg-white hover:bg-neutral-100'}`; 
        } else { 
            return `${baseClasses} rounded-r-md ${activeTab === 'statistics' ? 'bg-neutral-200 text-gray-800 border-gray-400 z-10' : 'bg-white hover:bg-neutral-100'}`; 
        }
    };

    // 상세 탭 스타일 (응답/통계)
    const getDetailTabClass = (tabName) => { 
        const baseClasses = "pb-2 px-3 text-lg cursor-pointer transition-colors";
        return activeTab === tabName 
            ? `${baseClasses} font-semibold text-green-600 border-b-2 border-green-600` 
            : `${baseClasses} text-gray-600 hover:text-gray-800`;
    };

    // 응답 서브 탭 스타일 (객관식/주관식)
    const getResponseSubTabClass = (tabName) => { 
        const baseClasses = "py-1 px-4 text-sm font-medium transition-colors rounded-full";
        return activeResponseTab === tabName 
            ? `${baseClasses} bg-green-500 text-white shadow-md` 
            : `${baseClasses} bg-gray-100 text-gray-700 hover:bg-gray-200`;
    };
    
    // 로딩 상태 UI
    if (isLoading) {
        return (
            <div className="min-h-screen bg-neutral-50 py-8 flex justify-center items-center">
                <div className="flex items-center text-xl text-gray-600">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    데이터를 불러오는 중입니다...
                </div>
            </div>
        );
    }

    // 에러 상태 UI
    if (error) {
        return (
            <div className="min-h-screen bg-neutral-50 py-8 flex justify-center items-center p-4">
                <div className="p-8 bg-white border border-red-300 rounded-xl shadow-lg max-w-xl text-center">
                    <svg className="w-12 h-12 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p className="text-lg font-semibold text-red-700 mb-2">데이터 로드 실패</p>
                    <p className="text-sm text-gray-600 mb-3">설문 ID: {survey_id}</p>
                    <div className="text-sm text-red-600 bg-red-50 p-4 rounded-lg">
                        {error}
                    </div>
                </div>
            </div>
        );
    }
    
    // 메인 UI 렌더링
    return (
        <div className="min-h-screen bg-neutral-50 py-8 font-inter">
            <div className="max-w-6xl mx-auto px-4">
                <div className="flex flex-col md:flex-row gap-8">
                    
                    {/* 왼쪽 패널: 설문 개요 및 통계 */}
                    <div className="w-full md:w-1/3 min-w-[300px]">
                        {/* 설문 제목 및 대상자 수 */}
                        <h1 className="text-3xl font-bold text-gray-800 mb-1">
                            설문명: {survey_title}
                        </h1>
                        <p className="text-base text-gray-500 mb-6">
                            총 설문 대상자: {distributed_count}명
                        </p>

                        {/* 메인 탭 전환 버튼 (응답/통계) */}
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

                        {/* 주요 통계 카드 (응답 수, 완료율) */}
                        <div className="grid grid-cols-2 gap-4 mb-8">
                            <div className="p-4 rounded-xl shadow-md bg-white border border-gray-200">
                                <p className="text-sm text-gray-600">완료된 응답 수:</p>
                                <p className="text-4xl font-extrabold text-blue-600">{response_count}</p>
                            </div>
                            <div className="p-4 rounded-xl shadow-md bg-white border border-gray-200">
                                <p className="text-sm text-gray-600">설문 완료율:</p>
                                <p className="text-4xl font-extrabold text-green-600">{completion_rate}%</p>
                            </div>
                        </div>

                        {/* 설문지 상세 정보 */}
                        <div className="p-5 bg-white border rounded-xl shadow-md mt-6">
                            <h3 className="text-lg font-semibold text-gray-700 mb-3 border-b pb-2">
                                설문지 정보
                            </h3>
                            <div className="space-y-2 text-sm text-gray-600">
                                <p><strong>총 질문 개수:</strong> {total_questions}개</p>
                                <p><strong>객관식/주관식:</strong> {single_choice_count}개 / {short_text_count}개</p>
                                <p><strong>생성일:</strong> {formatDate(created_at)}</p>
                                <p><strong>마감일:</strong> {formatDate(expire_at)}</p>
                            </div>
                        </div>
                    </div>

                    {/* 오른쪽 패널: 상세 응답/통계 */}
                    <div className="w-full md:w-2/3">
                        {/* 상세 탭 헤더 */}
                        <div className="mb-4">
                            <h2 className="text-2xl font-bold text-gray-800 mb-3">
                                {activeTab === 'response' ? `상세 응답 [${response_count}]개` : '상세 통계 분석'}
                            </h2>
                            <div className="flex border-b-2 border-gray-200 relative">
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
                            </div>
                        </div>

                        {/* 응답 탭 콘텐츠 */}
                        {activeTab === 'response' ? (
                            <div className="p-6 bg-white border rounded-xl shadow-lg">
                                <h3 className="text-xl font-semibold border-b pb-3 mb-5 text-gray-700">
                                    개별 응답 질문 목록
                                </h3>
                                
                                {/* 객관식/주관식 서브 탭 */}
                                <div className="flex space-x-3 mb-6">
                                    <button 
                                        className={getResponseSubTabClass('single')} 
                                        onClick={() => handleResponseTabChange('single')}
                                    >
                                        객관식 질문 ({single_choice_count}개)
                                    </button>
                                    <button 
                                        className={getResponseSubTabClass('text')} 
                                        onClick={() => handleResponseTabChange('text')}
                                    >
                                        주관식 질문 ({short_text_count}개)
                                    </button>
                                </div>

                                {/* 질문 목록 렌더링 */}
                                <div className="space-y-4">
                                    {activeResponseTab === 'single' ? (
                                        // 객관식 질문 목록
                                        single_choice_questions.length > 0 ? (
                                            single_choice_questions.map((question, index) => (
                                                <div 
                                                    key={question.question_id || index} 
                                                    className="p-4 border rounded-lg bg-neutral-50 shadow-sm border-l-4 border-green-400"
                                                >
                                                    <p className="font-semibold text-gray-700">
                                                        Q{index + 1}. {question.question_text}
                                                    </p>
                                                    <p className="text-sm text-gray-500 mt-1">
                                                        총 응답 수: <span className="font-bold text-green-600">
                                                            {question.total_responses || response_count}
                                                        </span>
                                                    </p>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="h-40 flex items-center justify-center text-gray-500 border border-dashed rounded-xl">
                                                객관식 질문이 없거나 데이터가 없습니다.
                                            </div>
                                        )
                                    ) : (
                                        // 주관식 질문 목록
                                        short_text_questions.length > 0 ? (
                                            short_text_questions.map((question, index) => (
                                                <div 
                                                    key={question.question_id || index} 
                                                    className="p-4 border rounded-lg bg-neutral-50 shadow-sm border-l-4 border-blue-400"
                                                >
                                                    <p className="font-semibold text-gray-700">
                                                        Q{index + 1}. {question.question_text}
                                                    </p>
                                                    <p className="text-sm text-gray-500 mt-1">
                                                        총 응답 수: <span className="font-bold text-blue-600">
                                                            {question.total_responses || response_count}
                                                        </span>
                                                    </p>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="h-40 flex items-center justify-center text-gray-500 border border-dashed rounded-xl">
                                                주관식 질문이 없거나 데이터가 없습니다.
                                            </div>
                                        )
                                    )}
                                </div>
                            </div>
                        ) : (
                            // 통계 탭
                            <div className="p-6 bg-white border rounded-xl shadow-lg">
                                <h3 className="text-xl font-semibold border-b pb-3 mb-5 text-gray-700">
                                    설문 통계 분석
                                </h3>
                                <div className="h-64 flex items-center justify-center text-gray-500 border border-dashed rounded-xl">
                                    <p className="text-lg">통계 차트</p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}