import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const DataUploadComponent = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [fileName] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(''); // Clear previous messages
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('请先选择文件。');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);  // Set loading state to true
    try {
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Response Data:', response.data);


//      setMessage(response.data.message);
//      if (response.data.file_name) {
//        setFileName(response.data.file_name);
//      }
      navigate('/map', { state: { htmlContent: response.data } });
      setFile(null); // Clear the file input after upload
    } catch (error) {
      console.error(error);
      const errorMessage = error.response?.data?.error || '文件上传时发生错误。';
      setMessage(errorMessage); // 保留消息状态
      alert(errorMessage); // 弹窗显示错误信息
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  return (
    <div style={styles.container}>
      <input type="file" onChange={handleFileChange} style={styles.input} />
      <button onClick={handleUpload} style={styles.button} disabled={loading}>
        {loading ? '上传中...' : '上传'}
      </button>
      {message && <p style={styles.message}>{message}</p>}

      {fileName && <p style={styles.fileName}>已上传文件: {fileName}</p>}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
    boxSizing: 'border-box'
  },
  input: {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc'
  },
  button: {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    margin: '10px 0'
  },
  message: {
    marginTop: '20px',
    fontSize: '16px',
    color: '#333'
  }
};

export default DataUploadComponent;