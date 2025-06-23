import React, { useState, useEffect } from 'react';
import ProcessingStatus from './ProcessingStatus';
import StatusMessage from './StatusMessage';
import { jsPDF } from 'jspdf';
import toast, { Toaster } from 'react-hot-toast';

const API_URL = 'http://localhost:8000/api/v1/process';
const ALLOWED_TYPES = ['audio/mp3', 'audio/wav', 'audio/x-m4a'];
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB in bytes

// Helper function to format file size
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

function MeetingProcessor({ selectedMeeting, onClearSelection }) {
  const [file, setFile] = useState(null);
  const [processingStage, setProcessingStage] = useState(null);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [statusMessage, setStatusMessage] = useState(null);

  useEffect(() => {
    if (selectedMeeting) {
      setResult(selectedMeeting);
    }
  }, [selectedMeeting]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Check file type
      if (!ALLOWED_TYPES.includes(selectedFile.type)) {
        const errorMsg = `Please select a valid audio file (MP3, WAV, or M4A). Selected file type: ${selectedFile.type}`;
        setError(errorMsg);
        setStatusMessage({ type: 'error', message: errorMsg });
        toast.error(errorMsg);
        setFile(null);
        return;
      }

      // Check file size
      if (selectedFile.size > MAX_FILE_SIZE) {
        const errorMsg = `File size (${formatFileSize(selectedFile.size)}) exceeds 25MB limit`;
        setError(errorMsg);
        setStatusMessage({ type: 'error', message: errorMsg });
        toast.error(errorMsg);
        setFile(null);
        return;
      }

      setFile(selectedFile);
      setError(null);
      setStatusMessage({ 
        type: 'success', 
        message: `File selected: ${selectedFile.name} (${formatFileSize(selectedFile.size)})` 
      });
      onClearSelection?.();
      toast.success('File selected successfully');
    }
  };

  const saveMeetingToHistory = (meetingData) => {
    const meetings = JSON.parse(localStorage.getItem('meetings') || '[]');
    meetings.unshift({
      ...meetingData,
      timestamp: new Date().toISOString(),
    });
    localStorage.setItem('meetings', JSON.stringify(meetings));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      const errorMsg = 'Please select a file first';
      setError(errorMsg);
      setStatusMessage({ type: 'error', message: errorMsg });
      toast.error(errorMsg);
      return;
    }

    setProcessingStage('uploading');
    setError(null);
    setStatusMessage({ type: 'info', message: 'Uploading file...' });
    toast.loading('Uploading file...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Upload and start processing
      setProcessingStage('transcribing');
      setStatusMessage({ type: 'info', message: 'Transcribing audio...' });
      toast.loading('Transcribing audio...');
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 413) {
          throw new Error('File size exceeds 25MB limit');
        } else if (response.status === 400) {
          throw new Error('Invalid file type. Please select an MP3, WAV, or M4A file.');
        } else {
          throw new Error(errorData.detail || 'Failed to process the meeting');
        }
      }

      // Start summarization
      setProcessingStage('summarizing');
      setStatusMessage({ type: 'info', message: 'Generating summary...' });
      toast.loading('Generating summary...');
      const data = await response.json();
      
      // Validate response data
      if (!data.transcript || !data.summary || !data.action_items) {
        throw new Error('Invalid response format from server');
      }

      setResult(data);
      saveMeetingToHistory(data);
      
      // Show completion state briefly before hiding the progress bar
      setProcessingStage('complete');
      setStatusMessage({ type: 'success', message: 'Meeting processed successfully!' });
      toast.success('Meeting processed successfully!');
      setTimeout(() => {
        setProcessingStage(null);
        setStatusMessage(null);
      }, 2000);
    } catch (err) {
      const errorMsg = err.message || 'An error occurred while processing the meeting';
      setError(errorMsg);
      setStatusMessage({ type: 'error', message: errorMsg });
      toast.error(errorMsg);
      setProcessingStage(null);
    }
  };

  const handleDownloadReport = () => {
    if (!result) return;

    try {
      const doc = new jsPDF();
      const margin = 20;
      let y = margin;
      const lineHeight = 7;
      const pageWidth = doc.internal.pageSize.width;
      const maxWidth = pageWidth - (2 * margin);

      // Add title
      doc.setFontSize(20);
      doc.text('Meeting Report', margin, y);
      y += lineHeight * 2;

      // Add timestamp
      doc.setFontSize(12);
      const timestamp = new Date().toLocaleString();
      doc.text(`Generated on: ${timestamp}`, margin, y);
      y += lineHeight * 2;

      // Add transcript section
      doc.setFontSize(16);
      doc.text('Transcript', margin, y);
      y += lineHeight;
      doc.setFontSize(12);
      const transcriptLines = doc.splitTextToSize(result.transcript, maxWidth);
      doc.text(transcriptLines, margin, y);
      y += (transcriptLines.length * lineHeight) + lineHeight;

      // Add summary section
      doc.setFontSize(16);
      doc.text('Summary', margin, y);
      y += lineHeight;
      doc.setFontSize(12);
      const summaryLines = doc.splitTextToSize(result.summary, maxWidth);
      doc.text(summaryLines, margin, y);
      y += (summaryLines.length * lineHeight) + lineHeight;

      // Add action items section
      doc.setFontSize(16);
      doc.text('Action Items', margin, y);
      y += lineHeight;
      doc.setFontSize(12);
      const actionItemsLines = doc.splitTextToSize(result.action_items, maxWidth);
      doc.text(actionItemsLines, margin, y);

      // Save the PDF
      doc.save('meeting-report.pdf');
      toast.success('Report downloaded successfully!');
    } catch (err) {
      const errorMsg = 'Failed to generate PDF report';
      setStatusMessage({ type: 'error', message: errorMsg });
      toast.error(errorMsg);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <Toaster position="top-right" />
      
      {/* Status Message */}
      {statusMessage && (
        <StatusMessage type={statusMessage.type} message={statusMessage.message} />
      )}
      
      {/* File Upload Section */}
      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Upload Meeting Audio</h2>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            Select Audio File
          </label>
          <input
            type="file"
            accept=".mp3,.wav,.m4a"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100
              transition-colors duration-200"
          />
          <p className="text-xs text-gray-500">
            Supported formats: MP3, WAV, M4A (max 25MB)
          </p>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={processingStage !== null || !file}
          className={`w-full py-3 px-4 rounded-md text-white font-medium
            ${processingStage !== null || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
            }
            transition-colors duration-200`}
        >
          {processingStage ? 'Processing...' : 'Process Meeting'}
        </button>
      </div>

      {/* Processing Status */}
      {processingStage && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <ProcessingStatus stage={processingStage} error={error} />
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Download Report Button */}
          <button
            onClick={handleDownloadReport}
            className="w-full py-3 px-4 rounded-md text-white font-medium 
              bg-green-600 hover:bg-green-700 transition-colors duration-200
              flex items-center justify-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>Download Report (PDF)</span>
          </button>

          {/* Transcript Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Transcript</h3>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-600 whitespace-pre-wrap leading-relaxed">
                {result.transcript}
              </p>
            </div>
          </div>

          {/* Summary Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Summary</h3>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-600 leading-relaxed">
                {result.summary}
              </p>
            </div>
          </div>

          {/* Action Items Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Action Items</h3>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-600 whitespace-pre-wrap leading-relaxed">
                {result.action_items}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MeetingProcessor; 