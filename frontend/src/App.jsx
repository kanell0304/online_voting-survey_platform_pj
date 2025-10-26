import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Layout 컴포넌트 import
import MainLayout from './Components/Layout/MainLayout.jsx';

// 페이지 컴포넌트 import
import MainPage from './Components/Pages/MainPage.jsx';
import LoginPage from './Components/Auth/LoginPage.jsx';
import SignupPage from './Components/Auth/SignupPage.jsx';

import FindPasswordRequestPage from './Components/Auth/FindPasswordRequestPage.jsx';
import FindPasswordResetPage from './Components/Auth/FindPasswordResetPage.jsx';
import MySurveysPage from './Components/Pages/MySurveysPage.jsx'; // Survey 폴더로 경로 수정
import CreateFormPage from './Components/Pages/CreateFormPage.jsx';
import FormPreview from './Components/Forms/FormPreview.jsx';
import ResponsePage from './Components/Pages/ResponsePage.jsx';
import SurveyResultPage from './Components/Survey/SurveyResultPage.jsx';
import SurveyDistributionPage from './Components/Survey/SurveyDistributionPage.jsx';
import EditFormPage from './Components/Pages/EditFormPage.jsx';

export default function App() {
  const [formData, setFormData] = useState({ title: "", questions: [] });

  return (
    <Router>
      <Routes>
        {/* 헤더가 필요 없는 독립적인 페이지들 */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* ----- 2. (여기 추가!) 비밀번호 찾기 라우트 2개 ----- */}
        <Route path="/find-password" element={<FindPasswordRequestPage />} />
        <Route path="/reset-password" element={<FindPasswordResetPage />} />
        {/* ----------------------------------------------- */}

        {/* MainLayout을 사용해 헤더를 공통으로 적용할 페이지들 */}
        <Route path="/" element={<MainLayout><MainPage /></MainLayout>} />
        <Route path="/my-surveys" element={<MainLayout><MySurveysPage /></MainLayout>} />
        <Route path="/create" element={
          <MainLayout>
            <CreateFormPage formData={formData} setFormData={setFormData} />
          </MainLayout>
        } />
        <Route path="/preview" element={
          <MainLayout>
            <FormPreview formData={formData} />
          </MainLayout>
        } />
        <Route path="/surveys/:formId" element={<MainLayout><ResponsePage /></MainLayout>} />
        <Route path="/edit/:formId" element={<MainLayout><EditFormPage /></MainLayout>} />

        <Route path="/survey-result/:formId" element={<MainLayout><SurveyResultPage /></MainLayout>} />
        <Route path="/distribute/:formId" element={<MainLayout><SurveyDistributionPage /></MainLayout>} />
      </Routes>
    </Router>
  );
}
