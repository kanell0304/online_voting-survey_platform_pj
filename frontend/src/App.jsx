import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateFormPage from './Components/Pages/CreateFormPage';
import FormPreview from './Components/Forms/FormPreview';
import ResponsePage from './Components/Pages/ResponsePage';

export default function App() {
  const [formData, setFormData] = useState({ title: "", questions: [] }); // form, preview 데이터 전달용

  return (
    <Router>
        <Routes>
          
          <Route path="/create" element={<CreateFormPage formData={formData} setFormData={setFormData} />} />
          <Route path="/preview" element={<FormPreview formData={formData} />} />
          <Route path="/responses" element={<ResponsePage />} />

        </Routes>
    </Router>
  );
}