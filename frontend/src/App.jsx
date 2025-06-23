import React, { useState } from 'react';
import MeetingProcessor from './components/MeetingProcessor';
import MeetingHistory from './components/MeetingHistory';

function App() {
  const [selectedMeeting, setSelectedMeeting] = useState(null);

  const handleSelectMeeting = (meeting) => {
    setSelectedMeeting(meeting);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Meeting Assistant</h1>
        <div className="flex gap-6">
          <div className="flex-1">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <MeetingProcessor 
                selectedMeeting={selectedMeeting}
                onClearSelection={() => setSelectedMeeting(null)}
              />
            </div>
          </div>
          <MeetingHistory onSelectMeeting={handleSelectMeeting} />
        </div>
      </div>
    </div>
  );
}

export default App; 