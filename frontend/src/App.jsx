import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Layout 컴포넌트 import
import MainLayout from './Components/Layout/MainLayout.jsx';

// 페이지 컴포넌트 import
import MainPage from './Components/Pages/MainPage.jsx';
import LoginPage from './Components/Auth/LoginPage.jsx';
import SignupPage from './Components/Auth/SignupPage.jsx';
import MySurveysPage from './Components/Pages/MySurveysPage.jsx'; // Survey 폴더로 경로 수정
import CreateFormPage from './Components/Pages/CreateFormPage.jsx';
import FormPreview from './Components/Forms/FormPreview.jsx';
import ResponsePage from './Components/Pages/ResponsePage.jsx';

export default function App() {
  const [formData, setFormData] = useState({ title: "", questions: [] });

  return (
    <Router>
      <Routes>
        {/* 헤더가 필요 없는 독립적인 페이지들 */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

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
        <Route path="/responses" element={<MainLayout><ResponsePage /></MainLayout>} />
      </Routes>
    </Router>
  );
}