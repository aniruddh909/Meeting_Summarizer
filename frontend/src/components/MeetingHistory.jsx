import React, { useState, useEffect } from 'react';

const MeetingHistory = ({ onSelectMeeting }) => {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    // Load meetings from localStorage on component mount
    const storedMeetings = JSON.parse(localStorage.getItem('meetings') || '[]');
    setMeetings(storedMeetings);
  }, []);

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="w-1/4 bg-gray-50 p-4 border-l border-gray-200">
      <h2 className="text-xl font-semibold mb-4">Meeting History</h2>
      <div className="space-y-2 max-h-[calc(100vh-8rem)] overflow-y-auto">
        {meetings.length === 0 ? (
          <p className="text-gray-500 text-sm">No meetings recorded yet</p>
        ) : (
          meetings.map((meeting, index) => (
            <div
              key={index}
              className="p-3 bg-white rounded-lg shadow-sm hover:shadow-md cursor-pointer transition-shadow"
              onClick={() => onSelectMeeting(meeting)}
            >
              <div className="text-sm font-medium text-gray-900">
                Meeting {meetings.length - index}
              </div>
              <div className="text-xs text-gray-500">
                {formatDate(meeting.timestamp)}
              </div>
              <div className="text-xs text-gray-600 mt-1 line-clamp-2">
                {meeting.summary}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default MeetingHistory; 