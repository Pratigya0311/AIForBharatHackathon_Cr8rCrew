import React from 'react';
import ContentUploader from '../components/ContentLibrary/ContentUploader';
import ContentList from '../components/ContentLibrary/ContentList';
import { mockContents } from '../data/mockData';

const ContentPage = () => {
  const handleUpload = (file) => {
    console.log('Uploading file:', file);
  };

  return (
    <div className="content-page">
      <h1>Content Library</h1>
      <ContentUploader onUpload={handleUpload} />
      <ContentList contents={mockContents} />
    </div>
  );
};

export default ContentPage;
