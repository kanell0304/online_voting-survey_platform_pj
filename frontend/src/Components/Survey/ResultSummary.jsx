import React, { useMemo } from 'react';

export default function QuestionChart({ question, responses, questionIndex }) {
    const chartData = useMemo(() => {
        if (question.type === 'short_answer' || question.type === 'paragraph') {
            // 주관식 답변 목록
            return responses
                .map(response => response.answers?.[questionIndex])
                .filter(answer => answer && answer.trim() !== '');
        }

        // 객관식 답변 통계
        const answerCounts = {};
        question.options?.forEach(option => {
            answerCounts[option] = 0;
        });

        responses.forEach(response => {
            const answer = response.answers?.[questionIndex];
            if (question.type === 'multiple_choice') {
                // 다중 선택
                if (Array.isArray(answer)) {
                    answer.forEach(opt => {
                        if (answerCounts[opt] !== undefined) {
                            answerCounts[opt]++;
                        }
                    });
                }
            } else {
                // 단일 선택
                if (answer && answerCounts[answer] !== undefined) {
                    answerCounts[answer]++;
                }
            }
        });

        const total = Object.values(answerCounts).reduce((sum, count) => sum + count, 0);
        
        return Object.entries(answerCounts).map(([option, count]) => ({
            option,
            count,
            percentage: total > 0 ? Math.round((count / total) * 100) : 0
        }));
    }, [question, responses, questionIndex]);

    const getQuestionTypeLabel = (type) => {
        const labels = {
            'short_answer': '단답형',
            'paragraph': '장문형',
            'single_choice': '단일 선택',
            'multiple_choice': '다중 선택'
        };
        return labels[type] || type;
    };

    const renderShortAnswers = () => (
        <div className="space-y-2 max-h-96 overflow-y-auto">
            {chartData.length === 0 ? (
                <p className="text-gray-500 text-center py-4">아직 응답이 없습니다.</p>
            ) : (
                chartData.map((answer, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                        <p className="text-gray-800">{answer}</p>
                    </div>
                ))
            )}
        </div>
    );

    const renderBarChart = () => {
        const maxCount = Math.max(...chartData.map(item => item.count), 1);

        return (
            <div className="space-y-4">
                {chartData.map((item, index) => (
                    <div key={index}>
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-sm font-medium text-gray-700">
                                {item.option}
                            </span>
                            <span className="text-sm text-gray-600">
                                {item.count}명 ({item.percentage}%)
                            </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-8 overflow-hidden">
                            <div
                                className="bg-blue-600 h-full rounded-full flex items-center justify-end pr-2 transition-all duration-500"
                                style={{ width: `${(item.count / maxCount) * 100}%` }}
                            >
                                {item.count > 0 && (
                                    <span className="text-xs text-white font-semibold">
                                        {item.percentage}%
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            {/* 질문 헤더 */}
            <div className="mb-6">
                <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-gray-800">
                        Q{questionIndex + 1}. {question.text}
                    </h3>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-600">
                        {getQuestionTypeLabel(question.type)}
                    </span>
                </div>
                {question.required && (
                    <span className="text-red-500 text-sm">* 필수</span>
                )}
            </div>

            {/* 차트/응답 목록 */}
            <div>
                {question.type === 'short_answer' || question.type === 'paragraph'
                    ? renderShortAnswers()
                    : renderBarChart()
                }
            </div>

            {/* 총 응답 수 */}
            <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                    총 응답: <span className="font-semibold">{responses.length}명</span>
                </p>
            </div>
        </div>
    );
}