import React, { useState } from 'react';
import { FiDownload } from 'react-icons/fi';
import Swal from 'sweetalert2';

export default function DataExportButton({ formId, responses, surveyTitle }) {
    const [exporting, setExporting] = useState(false);

    const convertToCSV = (data) => {
        if (!data || data.length === 0) return '';

        // 헤더 생성
        const headers = ['응답 번호', '응답 시간', ...Object.keys(data[0].answers).map((_, i) => `질문 ${i + 1}`)];
        
        // 데이터 행 생성
        const rows = data.map((response, index) => {
            const answers = Object.values(response.answers).map(answer => {
                if (Array.isArray(answer)) {
                    return answer.join('; ');
                }
                return answer || '';
            });
            
            const timestamp = response.createdAt 
                ? new Date(response.createdAt).toLocaleString('ko-KR')
                : '-';

            return [index + 1, timestamp, ...answers];
        });

        // CSV 문자열 생성
        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        ].join('\n');

        return csvContent;
    };

    const handleExportCSV = () => {
        if (!responses || responses.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: '데이터 없음',
                text: '내보낼 응답 데이터가 없습니다.'
            });
            return;
        }

        setExporting(true);

        try {
            const csv = convertToCSV(responses);
            const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            const filename = `${surveyTitle || 'survey'}_결과_${new Date().toISOString().split('T')[0]}.csv`;
            
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            Swal.fire({
                icon: 'success',
                title: '내보내기 완료',
                text: 'CSV 파일이 다운로드되었습니다.',
                timer: 1500,
                showConfirmButton: false
            });
        } catch (error) {
            console.error('Export error:', error);
            Swal.fire({
                icon: 'error',
                title: '내보내기 실패',
                text: '데이터 내보내기에 실패했습니다.'
            });
        } finally {
            setExporting(false);
        }
    };

    const handleExportJSON = () => {
        if (!responses || responses.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: '데이터 없음',
                text: '내보낼 응답 데이터가 없습니다.'
            });
            return;
        }

        setExporting(true);

        try {
            const jsonData = JSON.stringify(responses, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            const filename = `${surveyTitle || 'survey'}_결과_${new Date().toISOString().split('T')[0]}.json`;
            
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            Swal.fire({
                icon: 'success',
                title: '내보내기 완료',
                text: 'JSON 파일이 다운로드되었습니다.',
                timer: 1500,
                showConfirmButton: false
            });
        } catch (error) {
            console.error('Export error:', error);
            Swal.fire({
                icon: 'error',
                title: '내보내기 실패',
                text: '데이터 내보내기에 실패했습니다.'
            });
        } finally {
            setExporting(false);
        }
    };

    const showExportMenu = () => {
        Swal.fire({
            title: '데이터 내보내기',
            text: '내보낼 형식을 선택하세요',
            showCancelButton: true,
            showDenyButton: true,
            confirmButtonText: 'CSV',
            denyButtonText: 'JSON',
            cancelButtonText: '취소',
            confirmButtonColor: '#3b82f6',
            denyButtonColor: '#10b981'
        }).then((result) => {
            if (result.isConfirmed) {
                handleExportCSV();
            } else if (result.isDenied) {
                handleExportJSON();
            }
        });
    };

    return (
        <button
            onClick={showExportMenu}
            disabled={exporting}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
            <FiDownload className="text-lg" />
            {exporting ? '내보내는 중...' : '데이터 내보내기'}
        </button>
    );
}