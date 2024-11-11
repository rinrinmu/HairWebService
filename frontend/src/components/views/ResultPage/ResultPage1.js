import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../NavBar/NavBar';
import { useLocation } from 'react-router-dom';
import Chart from 'chart.js/auto';
import '../style/resultStyle.css';

const ResultPage1 = () => {
  const location = useLocation();
  const [resultData, setResultData] = useState(null);
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (location.state) {
      setResultData(location.state);
      console.log('백엔드에서 받은 결과 데이터:', location.state);
    } else {
      console.error('결과 데이터를 전달받지 못했습니다.');
    }
  }, [location.state]);

  useEffect(() => {
    if (resultData && resultData.probabilities && chartRef.current) {
      // 이전 차트 인스턴스가 있다면 제거
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');
      
      // 차트 생성
      chartInstance.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['양호', '경증', '중증'],
          datasets: [
            {
              label: '확률',
              data: resultData.probabilities.map(prob => (prob * 100).toFixed(2)),
              backgroundColor: [
                'rgba(76, 175, 80, 0.8)',  // 양호 - 녹색
                'rgba(255, 193, 7, 0.8)',  // 경증 - 노란색
                'rgba(244, 67, 54, 0.8)'   // 중증 - 빨간색
              ],
              borderColor: [
                'rgba(76, 175, 80, 1)',
                'rgba(255, 193, 7, 1)',
                'rgba(244, 67, 54, 1)'
              ],
              borderWidth: 2,
              borderRadius: 8,
              borderSkipped: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false // 범례 숨기기
            },
            tooltip: {
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              titleColor: '#333',
              titleFont: {
                size: 14,
                weight: 'bold'
              },
              bodyColor: '#666',
              bodyFont: {
                size: 13
              },
              borderColor: '#ddd',
              borderWidth: 1,
              padding: 12,
              displayColors: true,
              callbacks: {
                label: function(context) {
                  return `${context.raw}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)',
                drawBorder: false
              },
              ticks: {
                font: {
                  size: 12
                },
                color: '#666',
                padding: 10,
                callback: function(value) {
                  return value + '%';
                }
              }
            },
            x: {
              grid: {
                display: false
              },
              ticks: {
                font: {
                  size: 13,
                  weight: 'bold'
                },
                color: '#333',
                padding: 8
              }
            }
          },
          animation: {
            duration: 1500,
            easing: 'easeInOutQuart'
          },
          layout: {
            padding: {
              top: 20,
              right: 20,
              bottom: 20,
              left: 20
            }
          }
        },
      });
    }

    // 컴포넌트 언마운트 시 차트 정리
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
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
              <p className={`prediction-result ${resultData.prediction.toLowerCase()}`}>
                판정 결과: {resultData.prediction}
              </p>
              <p>두피 점수: {resultData.score}점</p>
              <p className="solution">솔루션: {resultData.solution}</p>
              
              {resultData.pdf_url && (
                <a 
                  href={resultData.pdf_url} 
                  download 
                  className="download-btn"
                >
                  상세 분석 보고서 다운로드
                </a>
              )}
            </>
          ) : (
            <p>결과를 불러오는 중...</p>
          )}
        </div>

        <div className="result-box">
          <h3 className="chart-title">상태별 확률 분포</h3>
          <div className="chart-container">
            <canvas ref={chartRef}></canvas>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage1;