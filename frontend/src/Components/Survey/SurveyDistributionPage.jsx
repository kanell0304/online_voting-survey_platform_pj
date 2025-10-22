import React, { useState, useEffect } from 'react';

// ====================================================
// 1. EmailDistributionArea 컴포넌트
// ====================================================
const EmailDistributionArea = ({ emails, newEmail, onNewEmailChange, onAddEmail, onDeleteEmail, emailSubject, onSubjectChange, emailBody, onBodyChange }) => (
    <div className="flex flex-col gap-6">
        {/* 이메일 주소 입력 및 관리 카드 */}
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
                <button onClick={onAddEmail} className="px-4 py-2 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700 transition-colors">
                    추가
                </button>
            </div>
            <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
                {emails.map((email) => (
                    <div key={email} className="flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
                        {email}
                        <button onClick={() => onDeleteEmail(email)} className="ml-2 font-bold text-blue-600 hover:text-blue-900 leading-none">&times;</button>
                    </div>
                ))}
            </div>
        </div>

        {/* 이메일 제목 입력 필드 */}
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

        {/* 이메일 내용 입력 필드 */}
        <div className="p-5 bg-white border rounded-lg shadow-md">
            <h3 className="font-semibold text-lg border-b pb-2 mb-2 text-gray-800">이메일 내용</h3>
            <textarea 
                rows="8" 
                value={emailBody}
                onChange={onBodyChange}
                placeholder="설문 참여를 유도하는 메시지와 함께 설문 링크를 포함해 주세요."
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
            <p className="mt-2 text-sm text-gray-500">주의: 이메일 본문에 설문 URL이 포함되어야 응답자가 설문에 접근할 수 있습니다.</p>
        </div>
    </div>
);

// ====================================================
// 2. UrlDistributionArea 컴포넌트
// ====================================================
const UrlDistributionArea = ({ surveyUrl, onUrlChange, onUrlCopy }) => (
    <div className="p-5 bg-white border rounded-lg shadow-md">
        <h3 className="font-semibold text-lg border-b pb-2 mb-3 text-gray-800">설문 URL</h3>
        <div className="flex items-center gap-3">
            <input
                type="text"
                value={surveyUrl}
                onChange={onUrlChange}
                className="flex-grow p-2 border border-gray-300 rounded-md bg-neutral-50 text-gray-600 focus:bg-white focus:ring-blue-500 focus:border-blue-500"
            />
            <button 
                className="px-4 py-2 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600 transition-colors"
                onClick={() => onUrlCopy(surveyUrl)}
            >
                URL 복사
            </button>
        </div>
        <p className="mt-3 text-sm text-gray-500">URL을 복사하여 다양한 채널(메신저, SNS 등)에 직접 공유하세요.</p>
    </div>
);


// ====================================================
// 3. SurveyDistributionPage 메인 컴포넌트
// ====================================================
export default function SurveyDistributionPage() {
    // 상태 관리
    const [emails, setEmails] = useState(['user1@test.com', 'user2@boss.com']);
    const [newEmail, setNewEmail] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [distributionType, setDistributionType] = useState('email');
    const [surveyUrl, setSurveyUrl] = useState('https://yourdomain.com/survey/formId_XXX'); 
    const [showCopyToast, setShowCopyToast] = useState(false); 
    const [emailSubject, setEmailSubject] = useState('[설문 제목] 설문 참여 부탁드립니다.'); 
    const [emailBody, setEmailBody] = useState('안녕하세요. 저희 설문에 참여해 주시면 감사하겠습니다. \n\n[설문 URL 자리]');

    // 복사 성공 알림(Toast) 자동 숨김 로직
    useEffect(() => {
        if (showCopyToast) {
            const timer = setTimeout(() => {
                setShowCopyToast(false);
            }, 2000);
            return () => clearTimeout(timer);
        }
    }, [showCopyToast]);

    // URL 복사 핸들러 함수
    const handleUrlCopy = (url) => {
        // navigator.clipboard.writeText()는 Promise를 반환합니다.
        navigator.clipboard.writeText(url).then(() => {
            setShowCopyToast(true);
        }).catch(err => {
            console.error('URL 복사 실패:', err);
        });
    };
    
    // 이메일 추가 핸들러
    const handleAddEmail = () => {
        if (newEmail && !emails.includes(newEmail)) {
            setEmails([...emails, newEmail]);
            setNewEmail('');
        }
    };
    // 이메일 삭제 핸들러
    const handleDeleteEmail = (emailToDelete) => {
        setEmails(emails.filter(email => email !== emailToDelete));
    };

    // 설문 발송 (API 호출) 핸들러 함수 - Mock 버전
    const sendSurveyByEmail = async () => {
        if (emails.length === 0) {
            alert("발송할 이메일 주소를 입력해주세요.");
            return;
        }

        console.log("설문 발송 데이터:", {
            recipients: emails,
            subject: emailSubject,
            body: emailBody,
            surveyLink: surveyUrl
        });

        // 실제 API 호출 로직 대신 비동기 처리를 시뮬레이션합니다.
        try {
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const simulatedSuccess = true; 

            if (simulatedSuccess) {
                alert('설문 발송 요청이 성공적으로 처리되었습니다.');
            } else {
                alert(`발송 실패`);
            }
        } catch (error) {
            console.error('시뮬레이션 중 오류:', error);
            alert('설문 발송 중 시뮬레이션 오류 발생.');
        } finally {
            setShowPopup(false); 
        }
    };
    
    // 설문 발송 (팝업 띄우기) 핸들러
    const handleSendSurvey = () => {
        setShowPopup(true);
    };

    // 팝업 확인/취소 핸들러
    const handlePopupConfirm = (confirm) => {
        setShowPopup(false);
        if (confirm) {
            sendSurveyByEmail(); // 확인 시 시뮬레이션 호출
        }
    };


    return (
        <div className="min-h-screen bg-neutral-50 py-8">
            <div className="max-w-4xl mx-auto px-4 relative">
                
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-800">설문지 배포/배송</h1>
                    <p className="text-gray-600">설문을 이메일 또는 URL을 통해 응답자에게 전달하세요.</p>
                </div>
                
                {/* 배포 방법 탭 버튼 */}
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

                {/* 배포 방식에 따른 내용 렌더링 (조건부 렌더링) */}
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
                        onUrlChange={(e) => setSurveyUrl(e.target.value)}
                        onUrlCopy={handleUrlCopy}
                    />
                )}
                
                {/* 하단 발송 버튼 (URL 탭에서는 버튼 렌더링 안 함) */}
                <div className="mt-8 flex justify-end">
                    {distributionType === 'email' && (
                        <button
                            onClick={handleSendSurvey}
                            disabled={emails.length === 0}
                            className="px-6 py-2 font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 disabled:bg-gray-400 transition-colors"
                        >
                            설문 발송
                        </button>
                    )}
                </div>

                {/* 설문 발송 확인 팝업 (모달) */}
                {showPopup && (
                    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                        <div className="bg-white p-6 rounded-lg shadow-2xl w-full max-w-sm">
                            <h4 className="text-lg font-bold mb-4 text-gray-800">설문지 배포 확인</h4>
                            <p className="text-gray-600 mb-6">선택하신 대상에게 설문지를 발송하시겠습니까?</p>
                            <div className="flex justify-end space-x-3">
                                <button onClick={() => handlePopupConfirm(false)} className="px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200">취소</button>
                                <button onClick={() => handlePopupConfirm(true)} className="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600">확인</button>
                            </div>
                        </div>
                    </div>
                )}
                
                {/* URL 복사 성공 토스트 메시지 */}
                {showCopyToast && (
                    <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 p-3 bg-gray-800 text-white text-sm rounded-lg shadow-xl z-50 transition-opacity duration-300">
                        설문 URL이 클립보드에 복사되었습니다.
                    </div>
                )}
            </div>
        </div>
    );
}
