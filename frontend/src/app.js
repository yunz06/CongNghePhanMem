import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Import từ folder pages (Do bạn mới chuyển file vào đó)
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<h2 style={{textAlign: 'center', marginTop: '50px'}}>Đăng nhập thành công! (Dashboard)</h2>} />
          <Route path="/admin/dashboard" element={<h2 style={{textAlign: 'center', marginTop: '50px'}}>Chào Admin! (Trang quản trị)</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;