import React from 'react';
import { useLocation } from 'react-router-dom';

const MapDisplayComponent = () => {
  const location = useLocation();
  const { htmlContent } = location.state || {}; // 获取传递的 HTML 内容

  return (
    <div>
      <h1>地图显示</h1>
      {htmlContent ? (
         <iframe
          title="KeplerGL Map"
          style={{ width: '100%', height: '800px', border: 'none' }}
          srcDoc={htmlContent}
        ></iframe>
      ) : (
        <p>没有地图可显示。</p>
      )}

    </div>
  );
};

export default MapDisplayComponent;