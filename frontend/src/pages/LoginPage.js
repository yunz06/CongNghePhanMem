/**
 * UTH-ConfMS Frontend - Login Page
 * Student: Lâm Minh Phú
 * MSSV: 096206003648
 * Description: Trang đăng nhập, xử lý token và phân quyền cơ bản.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // Gọi API Backend (Khớp với app.py)
      const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        // 1. Lưu Token và Info vào LocalStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));

        // 2. Kiểm tra Role để chuyển hướng
        if (data.user.role === 'admin') {
          alert(`Xin chào Admin ${data.user.fullname}! Đang vào trang quản trị...`);
          navigate('/admin/dashboard'); 
        } else {
          alert(`Đăng nhập thành công! Xin chào ${data.user.fullname}`);
          navigate('/dashboard');
        }
      } else {
        setError(data.message || 'Đăng nhập thất bại');
      }
    } catch (err) {
      setError('Lỗi kết nối Server! Hãy kiểm tra Backend.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <form onSubmit={handleSubmit} className="login-form">
          <h2>ĐĂNG NHẬP HỆ THỐNG</h2>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <input 
              type="email" 
              name="email" 
              placeholder="Email (VD: admin@uth.edu.vn)" 
              onChange={handleChange} 
              required 
            />
          </div>
          
          <div className="form-group">
            <input 
              type="password" 
              name="password" 
              placeholder="Mật khẩu" 
              onChange={handleChange} 
              required 
            />
          </div>

          <button type="submit" className="login-button">Đăng Nhập</button>
          
          <div className="login-footer">
            Chưa có tài khoản? <Link to="/register">Đăng ký ngay</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;