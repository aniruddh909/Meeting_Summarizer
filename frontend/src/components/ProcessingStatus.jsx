import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ProcessingStatus = ({ stage, error }) => {
  const steps = [
    { id: 'uploading', label: 'Uploading', description: 'Uploading audio file...' },
    { id: 'transcribing', label: 'Transcribing', description: 'Converting speech to text...' },
    { id: 'summarizing', label: 'Summarizing', description: 'Generating summary and action items...' },
    { id: 'complete', label: 'Complete', description: 'Processing complete!' }
  ];

  const currentStepIndex = steps.findIndex(s => s.id === stage);
  const isComplete = stage === 'complete';

  return (
    <div className="w-full space-y-8 py-4">
      {/* Progress Bar */}
      <div className="relative">
        {/* Background Line */}
        <div className="absolute top-1/2 left-0 w-full h-0.5 bg-gray-200 -translate-y-1/2" />
        
        {/* Progress Line */}
        <motion.div
          className="absolute top-1/2 left-0 h-0.5 bg-blue-500 -translate-y-1/2"
          initial={{ width: 0 }}
          animate={{ 
            width: isComplete ? '100%' : `${(currentStepIndex / (steps.length - 1)) * 100}%`
          }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
        />

        {/* Step Indicators */}
        <div className="relative flex justify-between">
          {steps.map((step, index) => {
            const isActive = index <= currentStepIndex;
            const isCurrent = index === currentStepIndex;

            return (
              <div key={step.id} className="flex flex-col items-center">
                {/* Circle */}
                <motion.div
                  className={`
                    w-8 h-8 rounded-full flex items-center justify-center
                    ${isActive ? 'bg-blue-500' : 'bg-gray-200'}
                    ${isCurrent ? 'ring-4 ring-blue-200' : ''}
                  `}
                  initial={{ scale: 0.8 }}
                  animate={{ scale: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  {isActive ? (
                    isComplete && index === steps.length - 1 ? (
                      <motion.svg
                        className="w-5 h-5 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2 }}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </motion.svg>
                    ) : (
                      <motion.div
                        className="w-4 h-4 bg-white rounded-full"
                        animate={{
                          scale: isCurrent ? [1, 1.2, 1] : 1,
                        }}
                        transition={{
                          duration: 1,
                          repeat: isCurrent ? Infinity : 0,
                          ease: "easeInOut"
                        }}
                      />
                    )
                  ) : (
                    <div className="w-4 h-4 bg-white rounded-full" />
                  )}
                </motion.div>

                {/* Label */}
                <motion.div
                  className={`
                    mt-2 text-sm font-medium
                    ${isActive ? 'text-blue-600' : 'text-gray-400'}
                  `}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  {step.label}
                </motion.div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Status Text */}
      <AnimatePresence mode="wait">
        <motion.div
          key={stage}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="text-center text-sm text-gray-600"
        >
          {steps[currentStepIndex]?.description}
        </motion.div>
      </AnimatePresence>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="p-4 text-sm text-red-700 bg-red-100 rounded-md"
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ProcessingStatus; 