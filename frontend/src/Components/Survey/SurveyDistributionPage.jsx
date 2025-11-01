import React, { useState, useEffect } from 'react';
import axios from 'axios'; 
import { useParams } from 'react-router-dom';

// 이메일 배포 영역 컴포넌트
const EmailDistributionArea = ({ 
    emails, 
    newEmail, 
    onNewEmailChange, 
    onAddEmail, 
    onDeleteEmail, 
    emailSubject, 
    onSubjectChange, 
    emailBody, 
    onBodyChange 
}) => (
    <div className="flex flex-col gap-6">
        {/* 이메일 주소 입력 및 관리 */}
        <div className="flex flex-col gap-4 p-5 bg-white border rounded-lg shadow-md">
            <h3 className="font-semibold text-lg border-b pb-2 mb-2 text-gray-800">이메일 주소 입력</h3>
            <div className="flex gap-2">
                <input
                    type="email"
                    placeholder="test@example.com"
                    value={newEmail}
                    onChange={onNewEmailChange} 
                    className="flex-grow p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') onAddEmail();
                    }}
                />
                <button 
                    onClick={onAddEmail} 
                    className="px-4 py-2 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700 transition-colors"
                >
                    추가
                </button>
            </div>
            
            {/* 등록된 이메일 목록 */}
            <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
                {emails.map((email) => (
                    <div key={email} className="flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
                        {email}
                        <button 
                            onClick={() => onDeleteEmail(email)} 
                            className="ml-2 font-bold text-blue-600 hover:text-blue-900 leading-none"
                        >
                            &times;
                        </button>
                    </div>
                ))}
            </div>
        </div>

        {/* 이메일 제목 입력 */}
        <div className="p-5 bg-white border rounded-lg shadow-md">
            <h3 className="font-semibold text-lg border-b pb-2 mb-2 text-gray-800">이메일 제목</h3>
            <input
                type="text"
                value={emailSubject}
                onChange={onSubjectChange}
                placeholder="설문 요청 제목을 입력하세요."
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
        </div>

        {/* 이메일 내용 입력 */}
        <div className="p-5 bg-white border rounded-lg shadow-md">
            <h3 className="font-semibold text-lg border-b pb-2 mb-2 text-gray-800">이메일 내용</h3>
            <textarea 
                rows="8" 
                value={emailBody}
                onChange={onBodyChange}
                placeholder="설문 참여를 유도하는 메시지와 함께 설문 링크를 포함해 주세요."
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
            <p className="mt-2 text-sm text-gray-500">
                주의: 이메일 본문에 설문 URL이 포함되어야 응답자가 설문에 접근할 수 있습니다.
            </p>
        </div>
    </div>
);

// URL 배포 영역 컴포넌트
const UrlDistributionArea = ({ surveyUrl, onUrlCopy }) => (
    <div className="p-5 bg-white border rounded-lg shadow-md">
        <h3 className="font-semibold text-lg border-b pb-2 mb-3 text-gray-800">설문 URL</h3>
        <div className="flex items-center gap-3">
            <input
                type="text"
                value={surveyUrl}
                readOnly
                className="flex-grow p-2 border border-gray-300 rounded-md bg-neutral-50 text-gray-600 focus:bg-white focus:ring-blue-500 focus:border-blue-500"
            />
            <button 
                className="px-4 py-2 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600 transition-colors"
                onClick={() => onUrlCopy(surveyUrl)}
            >
                URL 복사
            </button>
        </div>
        <p className="mt-3 text-sm text-gray-500">
            URL을 복사하여 다양한 채널(메신저, SNS 등)에 직접 공유하세요.
        </p>
    </div>
);

// API 상태 알림 토스트 컴포넌트
const ApiStatusToast = ({ message, type, onClose }) => {
    const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
    const icon = type === 'success' ? (
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
    ) : (
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
    );

    return (
        <div className={`fixed bottom-10 left-1/2 transform -translate-x-1/2 p-4 text-white text-sm rounded-lg shadow-xl z-50 transition-opacity duration-300 flex items-center ${bgColor}`}>
            {icon}
            <span>{message}</span>
            <button onClick={onClose} className="ml-4 font-bold leading-none">&times;</button>
        </div>
    );
};

// 메인 컴포넌트
export default function SurveyDistributionPage() {
    
    // URL 파라미터에서 설문 ID 추출
    const { formId: survey_id } = useParams();

    // 상태 관리
    const [emails, setEmails] = useState([]);
    const [newEmail, setNewEmail] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [distributionType, setDistributionType] = useState('email');
    const [surveyUrl, setSurveyUrl] = useState(`http://localhost:5173/surveys/${survey_id || ''}`); 
    const [showCopyToast, setShowCopyToast] = useState(false); 
    const [surveyTitle, setSurveyTitle] = useState("설문 제목");
    const [emailSubject, setEmailSubject] = useState('설문 참여 요청'); 
    const [emailBody, setEmailBody] = useState('안녕하세요. 저희 설문에 참여해 주시면 감사하겠습니다.');
    const [isLoading, setIsLoading] = useState(false); 
    const [apiMessage, setApiMessage] = useState({ show: false, text: '', type: 'success' });

    // 컴포넌트 마운트 시 설문 정보 불러오기
    useEffect(() => {
        const fetchSurveyInfo = async () => {
            try {
                const res = await axios.get(`http://localhost:8081/surveys/${survey_id}`, {
                    withCredentials: true
                });
                setSurveyTitle(res.data.title);
            } catch (error) {
                console.error('설문 정보 로드 실패:', error);
            }
        };

        if (survey_id) {
            fetchSurveyInfo();
        }
    }, [survey_id]);

    // 설문 제목 변경 시 이메일 제목 자동 업데이트
    useEffect(() => {
        setEmailSubject(`[${surveyTitle}] 설문 참여 부탁드립니다.`);
    }, [surveyTitle]);

    // 토스트 자동 숨김 (3초 후)
    useEffect(() => {
        if (showCopyToast || apiMessage.show) {
            const timer = setTimeout(() => {
                setShowCopyToast(false);
                setApiMessage({ show: false, text: '', type: 'success' });
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [showCopyToast, apiMessage.show]);

    // URL 복사 핸들러
    const handleUrlCopy = (url) => {
        const tempInput = document.createElement('input');
        tempInput.value = url;
        document.body.appendChild(tempInput);
        tempInput.select();
        
        try {
            document.execCommand('copy');
            setShowCopyToast(true);
        } catch (err) {
            console.error('URL 복사 실패:', err);
            setApiMessage({ show: true, text: 'URL 복사에 실패했습니다. 직접 복사해주세요.', type: 'error' });
        }
        
        document.body.removeChild(tempInput);
    };
    
    // 이메일 추가 핸들러
    const handleAddEmail = () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!newEmail) {
            return;
        }
        
        if (!emailRegex.test(newEmail)) {
            setApiMessage({ show: true, text: "유효한 이메일 주소를 입력해주세요.", type: 'error' });
            return;
        }
        
        if (emails.includes(newEmail)) {
            setApiMessage({ show: true, text: "이미 추가된 이메일 주소입니다.", type: 'error' });
            return;
        }
        
        setEmails([...emails, newEmail]);
        setNewEmail('');
    };
    
    // 이메일 삭제 핸들러
    const handleDeleteEmail = (emailToDelete) => {
        setEmails(emails.filter(email => email !== emailToDelete));
    };

    // 설문 발송 API 호출
    const sendSurveyByEmail = async () => {
        if (emails.length === 0) {
            setApiMessage({ show: true, text: "발송할 이메일 주소를 입력해주세요.", type: 'error' });
            setIsLoading(false); 
            return;
        }
        
        if (!survey_id) {
            setApiMessage({ show: true, text: "설문 ID가 누락되었습니다. 올바른 경로로 접근해주세요.", type: 'error' });
            setIsLoading(false); 
            return;
        }

        setIsLoading(true); 
        
        const finalBody = emailBody.replace('[설문 URL 자리]', surveyUrl);

        const dataForPost = {
            recipient_email: emails, 
            title: emailSubject, 
            content: finalBody, 
            survey_id: survey_id
        };

        const apiUrl = 'http://localhost:8081/emails/create_logs_and_send'; 
        const token = localStorage.getItem("access_token");

        try {
            await axios.post(
                apiUrl, 
                dataForPost, 
                { 
                    headers: { 
                        'Content-Type': 'application/json',
                        ...(token && { 'Authorization': `Bearer ${token}` }) 
                    },
                    withCredentials: true 
                }
            );

            setApiMessage({ show: true, text: '설문 발송이 완료되었습니다.', type: 'success' });
            
        } catch (error) {
            console.error('설문 발송 오류:', error);
            
            let errorMessage = '알 수 없는 오류가 발생했습니다.';

            if (error.code === 'ERR_NETWORK') {
                errorMessage = '서버 연결에 실패했습니다. 백엔드 서버를 확인해주세요.';
            } else if (error.response) {
                const status = error.response.status; 
                const serverMessage = error.response.data?.message || error.response.data?.detail || '서버 오류';

                if (status === 422 || status === 400) {
                    errorMessage = `요청 오류 (${status}): ${serverMessage}`;
                } else if (status === 401) {
                    errorMessage = `인증 오류 (${status}): 로그인이 필요합니다.`;
                } else {
                    errorMessage = `서버 오류 (${status}): ${serverMessage}`;
                }
            }
            
            setApiMessage({ show: true, text: errorMessage, type: 'error' });
            
        } finally {
            setIsLoading(false); 
            setShowPopup(false); 
        }
    };
    
    // 설문 발송 확인 팝업 표시
    const handleSendSurvey = () => {
        if (emails.length === 0) {
            setApiMessage({ show: true, text: "발송할 이메일 주소를 최소 하나 이상 추가해주세요.", type: 'error' });
            return;
        }
        setShowPopup(true);
    };

    // 팝업 확인/취소 핸들러
    const handlePopupConfirm = (confirm) => {
        setShowPopup(false);
        if (confirm) {
            sendSurveyByEmail();
        }
    };

    return (
        <div className="min-h-screen bg-neutral-50 py-8">
            <div className="max-w-4xl mx-auto px-4 relative">
                
                {/* 페이지 헤더 */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-800">설문지 배포</h1>
                    <p className="text-gray-600">설문을 이메일 또는 URL을 통해 응답자에게 전달하세요.</p>
                </div>
                
                {/* 배포 방법 탭 (이메일/URL) */}
                <div className="flex border-b border-gray-300 mb-6">
                    <button
                        onClick={() => setDistributionType('email')}
                        className={`py-2 px-4 text-lg font-medium transition-colors ${
                            distributionType === 'email' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800'
                        }`}
                    >
                        이메일 배포
                    </button>
                    <button
                        onClick={() => setDistributionType('url')}
                        className={`py-2 px-4 text-lg font-medium transition-colors ${
                            distributionType === 'url' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800'
                        }`}
                    >
                        URL/링크
                    </button>
                </div>

                {/* 탭별 콘텐츠 */}
                {distributionType === 'email' ? (
                    <EmailDistributionArea 
                        emails={emails}
                        newEmail={newEmail}
                        onNewEmailChange={(e) => setNewEmail(e.target.value)}
                        onAddEmail={handleAddEmail}
                        onDeleteEmail={handleDeleteEmail}
                        emailSubject={emailSubject}
                        onSubjectChange={(e) => setEmailSubject(e.target.value)}
                        emailBody={emailBody}
                        onBodyChange={(e) => setEmailBody(e.target.value)}
                    />
                ) : (
                    <UrlDistributionArea 
                        surveyUrl={surveyUrl}
                        onUrlCopy={handleUrlCopy}
                    />
                )}
                
                {/* 발송 버튼 (이메일 탭에서만 표시) */}
                <div className="mt-8 flex justify-end">
                    {distributionType === 'email' && (
                        <button
                            onClick={handleSendSurvey}
                            disabled={emails.length === 0 || isLoading} 
                            className="flex items-center px-6 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 disabled:bg-gray-400 transition-colors"
                        >
                            {isLoading ? (
                                <>
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    발송 중...
                                </>
                            ) : (
                                '설문 발송'
                            )}
                        </button>
                    )}
                </div>

                {/* 발송 확인 팝업 */}
                {showPopup && (
                    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                        <div className="bg-white p-6 rounded-lg shadow-2xl w-full max-w-sm">
                            <h4 className="text-lg font-bold mb-4 text-gray-800">설문지 배포 확인</h4>
                            <p className="text-gray-600 mb-6">
                                {emails.length}명에게 설문지를 발송하시겠습니까?
                            </p>
                            <div className="flex justify-end space-x-3">
                                <button 
                                    onClick={() => handlePopupConfirm(false)} 
                                    className="px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200"
                                >
                                    취소
                                </button>
                                <button 
                                    onClick={() => handlePopupConfirm(true)} 
                                    className="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600"
                                >
                                    확인
                                </button>
                            </div>
                        </div>
                    </div>
                )}
                
                {/* URL 복사 성공 토스트 */}
                {showCopyToast && (
                    <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 p-3 bg-gray-800 text-white text-sm rounded-lg shadow-xl z-50 transition-opacity duration-300">
                        설문 URL이 클립보드에 복사되었습니다.
                    </div>
                )}

                {/* API 상태 토스트 (성공/실패) */}
                {apiMessage.show && (
                    <ApiStatusToast 
                        message={apiMessage.text}
                        type={apiMessage.type}
                        onClose={() => setApiMessage({ show: false, text: '', type: 'success' })}
                    />
                )}
            </div>
        </div>
    );
}