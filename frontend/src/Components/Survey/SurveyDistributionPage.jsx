import React, { useState, useEffect } from 'react';

// Email 배포 영역 컴포넌트
const EmailDistributionArea = ({ emails, newEmail, onNewEmailChange, onAddEmail, onDeleteEmail }) => (
    <div className="flex flex-col gap-6">
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
        <div className="p-5 bg-white border rounded-lg shadow-md">
            <h3 className="font-semibold text-lg border-b pb-2 mb-2 text-gray-800">배포 메시지 (선택 사항)</h3>
            <textarea 
                rows="6" 
                placeholder="설문 참여를 유도하는 간단한 메모를 남겨주세요."
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
        </div>
    </div>
);

// URL 배포 영역 컴포넌트
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


export default function SurveyDistributionPage() {
    // 상태 관리
    const [emails, setEmails] = useState(['user1@test.com', 'user2@boss.com']);
    const [newEmail, setNewEmail] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [distributionType, setDistributionType] = useState('email');
    const [surveyUrl, setSurveyUrl] = useState('https://yourdomain.com/survey/formId_XXX'); 
    const [showCopyToast, setShowCopyToast] = useState(false); 

    // 복사 성공 알림 자동 숨김 로직
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
        navigator.clipboard.writeText(url).then(() => {
            setShowCopyToast(true);
        }).catch(err => {
            console.error('URL 복사 실패:', err);
            alert('URL 복사에 실패했습니다. 브라우저 설정을 확인해 주세요.');
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
    // 설문 발송 핸들러
    const handleSendSurvey = () => {
        setShowPopup(true);
    };
    // 팝업 확인/취소 핸들러
    const handlePopupConfirm = (confirm) => {
        setShowPopup(false);
        if (confirm) {
            alert("설문 발송이 요청되었습니다!");
        }
    };


    return (
        <div className="min-h-screen bg-neutral-50 py-8">
            <div className="max-w-4xl mx-auto px-4 relative">
                
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-800">설문지 배포</h1>
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

                {/* 배포 방식에 따른 내용 렌더링 */}
                {distributionType === 'email' ? (
                    <EmailDistributionArea 
                        emails={emails}
                        newEmail={newEmail}
                        onNewEmailChange={(e) => setNewEmail(e.target.value)}
                        onAddEmail={handleAddEmail}
                        onDeleteEmail={handleDeleteEmail}
                    />
                ) : (
                    <UrlDistributionArea 
                        surveyUrl={surveyUrl}
                        onUrlChange={(e) => setSurveyUrl(e.target.value)}
                        onUrlCopy={handleUrlCopy}
                    />
                )}
                
                {/* 하단 발송 버튼 */}
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

                {/* 설문 발송 확인 팝업 */}
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
                        🔗 설문 URL이 클립보드에 복사되었습니다.
                    </div>
                )}
            </div>
        </div>
    );
}