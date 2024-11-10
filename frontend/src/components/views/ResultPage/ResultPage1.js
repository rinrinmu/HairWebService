import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../NavBar/NavBar';
import { useLocation } from 'react-router-dom';
import Chart from 'chart.js/auto';
import '../style/resultStyle.css';

const ResultPage1 = () => {
  const location = useLocation();
  const [resultData, setResultData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (location.state) {
      setResultData(location.state);
      console.log('백엔드에서 받은 결과 데이터:', location.state);
    } else {
      console.error('결과 데이터를 전달받지 못했습니다.');
    }
  }, [location.state]);

  // Chart.js를 사용해 확률 막대 그래프 생성
  useEffect(() => {
    if (resultData && resultData.probabilities) {
      const ctx = chartRef.current.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['양호', '경증', '중증'],
          datasets: [
            {
              label: '확률 (%)',
              data: resultData.probabilities.map(prob => (prob * 100).toFixed(2)),
              backgroundColor: ['#4CAF50', '#FFEB3B', '#F44336'],
              borderColor: '#161616',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
            },
          },
        },
      });
    }
  }, [resultData]);

  return (
    <div>
      <Navbar />
      <div className="container">
        <div className="main-content">
          <div className="image-upload-box">
            {resultData && resultData.image_url ? (
              <img src={resultData.image_url} alt="Processed" className="processed-image" />
            ) : (
              <p>이미지를 불러오는 중...</p>
            )}
          </div>
        </div>

        <div className="result-text">
          {resultData ? (
            <>
              <h2>분석 결과</h2>
              <p>판정 결과: {resultData.prediction}</p>
              <p>두피 점수: {resultData.score}</p>
              <p>솔루션: {resultData.solution}</p>
              
              {resultData.pdf_url && (
                <a href={resultData.pdf_url} download>
                  <button className="download-btn">PDF 다운로드</button>
                </a>
              )}
            </>
          ) : (
            <p>결과를 불러오는 중...</p>
          )}
        </div>

        <div className="result-box">
          <canvas ref={chartRef} width="400" height="200"></canvas>
        </div>
      </div>
    </div>
  );
};

export default ResultPage1;
