import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './Components/Layout/MainLayout.jsx';
import MainPage from './Components/Pages/MainPage.jsx';
import SignupPage from './Components/Auth/SignupPage.jsx';
import LoginPage from './Components/Auth/LoginPage.jsx';
import FindPasswordRequestPage from './Components/Auth/FindPasswordRequestPage.jsx';
import FindPasswordResetPage from './Components/Auth/FindPasswordResetPage.jsx';
import MySurveysPage from './Components/Pages/MySurveysPage.jsx';
import CreateFormPage from './Components/Pages/CreateFormPage.jsx';
import FormPreview from './Components/Forms/FormPreview.jsx';
import EditFormPage from './Components/Pages/EditFormPage.jsx';
import ResponsePage from './Components/Pages/ResponsePage.jsx';
import SurveyDistributionPage from './Components/Survey/SurveyDistributionPage.jsx';
import SurveyResultPage from './Components/Survey/SurveyResultPage.jsx';
import Template from './Components/Forms/Template.jsx';
import Profile from './Components/Pages/Profile.jsx';

export default function App() {
  const [formData, setFormData] = useState({ title: "", description: "", questions: [] }); //생성 <-> 미리보기 데이터 연결용

  return (
    <Router>
      <Routes>
        {/* 메인페이지 */}
        <Route path="/" element={<MainLayout><MainPage /></MainLayout>} />
        <Route path="/profile" element={<MainLayout><Profile /></MainLayout>} />

        {/* 로그인 관련 */}
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/find-password" element={<FindPasswordRequestPage />} />
        <Route path="/reset-password" element={<FindPasswordResetPage />} />
        
        {/* 설문 관리(생성,수정,삭제 등) */}
        <Route path="/my-surveys" element={<MainLayout><MySurveysPage /></MainLayout>} />
        <Route path="/create" element={<MainLayout><CreateFormPage formData={formData} setFormData={setFormData} /></MainLayout>} />
        <Route path="/preview" element={<MainLayout><FormPreview formData={formData} /></MainLayout>} />
        <Route path="/templates" element={<MainLayout><Template formData={formData} setFormData={setFormData}/></MainLayout>} />
        <Route path="/edit/:formId" element={<MainLayout><EditFormPage /></MainLayout>} />

        {/* 설문 배포, 설문참여, 설문결과 */}
        <Route path="/distribute/:formId" element={<MainLayout><SurveyDistributionPage /></MainLayout>} />
        <Route path="/surveys/:formId" element={<ResponsePage />} />
        <Route path="/survey-result/:formId" element={<MainLayout><SurveyResultPage /></MainLayout>} />
      </Routes>
    </Router>
  );
}
