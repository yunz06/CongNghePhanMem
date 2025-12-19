import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AssignmentPage = () => {
  const [paperId, setPaperId] = useState('');
  const [paperTitle, setPaperTitle] = useState('');
  const [reviewers, setReviewers] = useState([]);
  const [selectedReviewer, setSelectedReviewer] = useState('');
  const [aiReasoning, setAiReasoning] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Gọi AI Gợi ý
  const handleGetAiSuggestion = async () => {
    if (!paperId) return alert("Vui lòng nhập ID bài báo!");
    setLoading(true);
    setAiReasoning('');
    setMessage('');
    
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/auto-assign', { paper_id: paperId });
      setPaperTitle(res.data.paper_title);
      setAiReasoning(res.data.ai_suggestion);
      fetchAvailableReviewers();
    } catch (err) {
      console.error(err);
      setMessage('Lỗi: ' + (err.response?.data?.error || "Không gọi được AI"));
    } finally {
      setLoading(false);
    }
  };

  // Lấy danh sách Reviewer
  const fetchAvailableReviewers = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/reviewers-available/${paperId}`);
      setReviewers(res.data);
    } catch (err) { console.error(err); }
  };

  // Lưu phân công
  const handleAssign = async () => {
    if (!selectedReviewer) return alert("Chưa chọn Reviewer!");
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/assign', {
        paper_id: paperId,
        reviewer_id: selectedReviewer
      });
      setMessage("✅ " + res.data.message);
    } catch (err) {
      setMessage("❌ " + (err.response?.data?.error || "Lỗi server"));
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', fontFamily: 'Arial' }}>
      <h1>🎓 Phân Công Phản Biện (AI Support)</h1>
      <div style={{ marginBottom: '20px' }}>
        <label>Nhập ID Bài báo: </label>
        <input type="number" value={paperId} onChange={(e) => setPaperId(e.target.value)} placeholder="VD: 1" style={{ padding: '8px', margin: '0 10px' }} />
        <button onClick={handleGetAiSuggestion} disabled={loading} style={{ padding: '8px 15px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
          {loading ? "AI đang đọc..." : "🤖 Hỏi ý kiến AI"}
        </button>
      </div>

      {paperTitle && (
        <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
          <h3>📄 Bài: {paperTitle}</h3>
          <div style={{ backgroundColor: '#e2e3e5', padding: '10px', borderRadius: '5px', marginBottom: '15px', borderLeft: '5px solid #28a745' }}>
            <strong>💡 AI Gemini đề xuất:</strong>
            <p style={{ whiteSpace: 'pre-line', marginTop: '5px' }}>{aiReasoning}</p>
          </div>
          <div>
            <select value={selectedReviewer} onChange={(e) => setSelectedReviewer(e.target.value)} style={{ padding: '8px', width: '60%' }}>
              <option value="">-- Chọn Giám Khảo --</option>
              {reviewers.map((r) => (<option key={r.id} value={r.id}>ID {r.id} - {r.name}</option>))}
            </select>
            <button onClick={handleAssign} style={{ marginLeft: '10px', padding: '8px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>💾 Lưu</button>
          </div>
          {message && <p style={{ marginTop: '15px', fontWeight: 'bold', color: message.includes('✅') ? 'green' : 'red' }}>{message}</p>}
        </div>
      )}
    </div>
  );
};

export default AssignmentPage;