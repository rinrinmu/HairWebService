// RecordsPage.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../NavBar/NavBar';
import './RecordsPage.css';

const RecordsPage = () => {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState('');

  const BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/records`);
        const recordsWithImages = response.data.map(record => ({
          ...record,
          imageUrl: `${BASE_URL}/static/images/resized_${record.image_filename}`
        }));
        setRecords(recordsWithImages);
      } catch (error) {
        console.error("Error fetching records:", error);
        setError('기록을 불러오는데 실패했습니다.');
      }
    };

    fetchRecords();
  }, []);

  const handleDownloadPDF = async (pdfFilename) => {
    if (!pdfFilename) {
      setError('PDF 파일이 존재하지 않습니다.');
      return;
    }

    try {
      const response = await axios.get(`${BASE_URL}/download-pdf/${pdfFilename}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', pdfFilename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setError('');
    } catch (error) {
      console.error("Error downloading PDF:", error);
      setError('PDF 다운로드에 실패했습니다.');
    }
  };

  return (
    <div className="container">
      <Navbar />
      <div className="content">
        <h2 className="header-text">분석 기록</h2>
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}
        <div className="records-list">
          {records.map((record) => (
            <div className="record-item" key={record.id}>
              <h3 className="record-name">{record.name}</h3>
              <div className="record-info">
                <p>
                  <span>판정 결과:</span>
                  <span className={`prediction-tag prediction-${record.prediction}`}>
                    {record.prediction}
                  </span>
                </p>
                <p>
                  <span>점수:</span>
                  <span>{record.score}점</span>
                </p>
                <p>
                  <span>날짜:</span>
                  <span>{new Date(record.created_at).toLocaleDateString()}</span>
                </p>
              </div>
              {record.pdf_filename && (
                <button
                  className="download-button"
                  onClick={() => handleDownloadPDF(record.pdf_filename)}
                >
                  PDF 다운로드
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecordsPage;