import React from 'react';
import Header from './Header.jsx';
import Footer from './Footer.jsx'; // Footer 컴포넌트도 추가합니다.

export default function MainLayout({ children }) {
  return (
    // min-h-screen: 화면 전체 높이를 최소 높이로 지정
    // flex flex-col: 자식 요소들을 세로(위->아래)로 배치하는 flex 컨테이너
    <div className="flex flex-col min-h-screen bg-neutral-50">
      <Header />

      {/* main 태그가 남은 공간을 모두 차지하도록 flex-grow를 사용합니다.
        이렇게 하면 페이지 내용이 짧아도 푸터가 딸려 올라오지 않습니다.
      */}
      <main className="flex-grow">
        {/*
          모든 페이지 콘텐츠가 일관된 너비와 여백을 갖도록 컨테이너를 설정합니다.
        */}
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}