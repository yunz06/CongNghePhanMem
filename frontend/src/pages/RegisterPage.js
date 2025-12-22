/**
 * UTH-ConfMS Frontend - Register Page
 * Student: Lâm Minh Phú
 * MSSV: 096206003648
 * Description: Trang đăng ký thành viên mới (Default Role: Author).
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './RegisterPage.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '', password: '', fullname: '', organization: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        alert('Đăng ký thành công! Vui lòng đăng nhập.');
        navigate('/login');
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Lỗi kết nối Server!');
    }
  };

  return (
    <div className="register-container">
      <div className="register-box">
        <form onSubmit={handleSubmit} className="register-form">
          <h2>ĐĂNG KÝ TÀI KHOẢN</h2>
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
          </div>
          <div className="form-group">
            <input type="password" name="password" placeholder="Mật khẩu" onChange={handleChange} required />
          </div>
          <div className="form-group">
            <input type="text" name="fullname" placeholder="Họ và Tên" onChange={handleChange} required />
          </div>
          <div className="form-group">
            <input type="text" name="organization" placeholder="Đơn vị / Trường (Tùy chọn)" onChange={handleChange} />
          </div>

          <button type="submit" className="register-button">Đăng Ký</button>

          <div className="register-footer">
            Đã có tài khoản? <Link to="/login">Đăng nhập</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;