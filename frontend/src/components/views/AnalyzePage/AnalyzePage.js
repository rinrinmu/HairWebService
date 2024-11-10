import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../style/style.css';
import Navbar from '../NavBar/NavBar';
import { useDropzone } from 'react-dropzone';

const AnalyzePage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [userName, setUserName] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
    console.log('Selected files:', files);
  };

  const onDrop = (acceptedFiles) => {
    setSelectedFiles(acceptedFiles);
    console.log('Dropped files:', acceptedFiles);
  };

  const handleFileUpload = async () => {
    if (selectedFiles.length === 0) {
      alert('파일을 선택하세요!');
      return;
    }

    if (!userName) {
      alert('이름을 입력하세요!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFiles[0]);
    formData.append('name', userName);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        alert('파일 업로드 성공!');
        console.log('서버 응답:', result);

        navigate('/ResultPage1', { state: result });
      } else {
        const error = await response.json();
        alert(`파일 업로드 실패! 상태 코드: ${response.status}, 에러 메시지: ${error.detail}`);
      }
    } catch (error) {
      console.error('파일 업로드 중 에러:', error);
      alert('파일 업로드 중 문제가 발생했습니다.');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/jpeg, image/png',
    multiple: false,
  });

  return (
    <div className="container">
      <Navbar />
      <div className="content">
        <p className="header-text">머리카락 보일라</p>
        <p className="description">
          두피 사진을 사용하여 현재 나의 두피 상태를 확인 할 수 있습니다.
        </p>

        {/* 사용자 이름 입력 필드 */}
        <div className="form-section">
          <div className="name-input-section">
            <label className="form-label">
              사용자 이름
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                placeholder="이름을 입력하세요"
                className="name-input"
              />
            </label>
          </div>

          {/* 드롭존 섹션 */}
          <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
            <input {...getInputProps()} />
            {isDragActive ? (
              <p>여기에 이미지를 놓아주세요...</p>
            ) : (
              <p>여기에 이미지를 드래그하거나 클릭하여 업로드하세요.</p>
            )}
          </div>

          {/* 이미지 선택 버튼 */}
          <div className="upload-section">
            <label className="upload-button">
              이미지 선택
              <input type="file" onChange={handleFileChange} />
            </label>
          </div>

          {/* 파일 업로드 버튼 */}
          <div className="upload-button-container">
            <button className="upload-button" onClick={handleFileUpload}>
              파일 업로드
            </button>
          </div>
        </div>

        {/* 선택된 파일 리스트 */}
        {selectedFiles.length > 0 && (
          <div className="file-list">
            <h4>선택한 파일:</h4>
            <ul>
              {selectedFiles.map((file, index) => (
                <li key={index}>{file.name}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalyzePage;
