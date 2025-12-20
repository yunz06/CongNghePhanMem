import React, { useState } from 'react';

const AssignmentPage = () => {
    // Dữ liệu giả lập (Sau này gọi API lấy thật)
    const [papers] = useState([
        { id: 1, title: 'Nghiên cứu AI trong giao thông' },
        { id: 2, title: 'Ứng dụng Blockchain trong Y tế' }
    ]);
    const [reviewers] = useState([
        { id: 101, name: 'TS. Nguyễn Văn A' },
        { id: 102, name: 'ThS. Trần Thị B' }
    ]);

    const [selectedPaper, setSelectedPaper] = useState('');
    const [selectedReviewer, setSelectedReviewer] = useState('');

    const handleAssign = async () => {
        if (!selectedPaper || !selectedReviewer) {
            alert("Vui lòng chọn đầy đủ thông tin!");
            return;
        }

        console.log("Đang gán:", selectedPaper, selectedReviewer);
        
        // Gọi API Backend
        try {
            const response = await fetch('/api/assignments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    paper_id: selectedPaper,
                    user_id: selectedReviewer
                })
            });
            
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
            } else {
                alert("Lỗi: " + data.error);
            }
        } catch (error) {
            console.error("Lỗi kết nối:", error);
            alert("Không thể kết nối đến server");
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <h2>[TP4] Phân công Phản biện</h2>
            
            <div style={{ margin: '15px 0' }}>
                <label><strong>Chọn Bài Báo:</strong></label><br/>
                <select 
                    style={{ padding: '5px', width: '300px' }}
                    onChange={(e) => setSelectedPaper(e.target.value)}
                >
                    <option value="">-- Chọn bài --</option>
                    {papers.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
            </div>

            <div style={{ margin: '15px 0' }}>
                <label><strong>Chọn Người Chấm:</strong></label><br/>
                <select 
                    style={{ padding: '5px', width: '300px' }}
                    onChange={(e) => setSelectedReviewer(e.target.value)}
                >
                    <option value="">-- Chọn giảng viên --</option>
                    {reviewers.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
                </select>
            </div>

            <button 
                onClick={handleAssign}
                style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}
            >
                Gán Người Chấm
            </button>
        </div>
    );
};

export default AssignmentPage;