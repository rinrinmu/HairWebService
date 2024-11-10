import React, { useEffect, useState } from 'react';
import Navbar from '../NavBar/NavBar';
import './RecordsPage.css';

function RecordsPage() {
    const [records, setRecords] = useState([]);

    useEffect(() => {
        // 백엔드에서 기록을 가져오는 비동기 함수
        const fetchRecords = async () => {
            try {
                const response = await fetch('http://localhost:8000/records');
                if (response.ok) {
                    const data = await response.json();
                    setRecords(data);
                } else {
                    console.error('Failed to fetch records');
                }
            } catch (error) {
                console.error('Error fetching records:', error);
            }
        };

        fetchRecords();
    }, []);

    return (
        <div className="records-container">
            <Navbar />
            <div className="records-content">
                <h2 className="title">분석 기록</h2>
                {records.length === 0 ? (
                    <p className="no-records">기록이 없습니다.</p>
                ) : (
                    <div className="records-list">
                        {records.map((record) => (
                            <div key={record.id} className="record-item">
                                <div className="record-header">
                                    <p className="record-name">이름: {record.name}</p>
                                    <p className="record-date">
                                        {new Date(record.created_at).toLocaleString()}
                                    </p>
                                </div>
                                <p className="record-prediction">예측: {record.prediction}</p>
                                <p className="record-score">점수: {record.score}</p>
                                <a
                                    href={record.pdf_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="pdf-link"
                                >
                                    PDF 다운로드
                                </a>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default RecordsPage;
