import React from 'react';
import { IoCloseSharp, IoCheckmarkCircle, IoWarning, IoInformationCircle, IoAlert } from "react-icons/io5";

function Modal({ 
  isOpen, 
  onClose, 
  title, 
  message, 
  type = 'info', 
  confirmText = 'OK', 
  cancelText = 'Cancel', 
  onConfirm, 
  onCancel,
  showCancel = false 
}) {
  if (!isOpen) return null;

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <IoCheckmarkCircle className="text-green-500 text-2xl" />;
      case 'error':
        return <IoAlert className="text-red-500 text-2xl" />;
      case 'warning':
        return <IoWarning className="text-yellow-500 text-2xl" />;
      default:
        return <IoInformationCircle className="text-blue-500 text-2xl" />;
    }
  };

  const getBackgroundColor = () => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200';
      case 'error':
        return 'bg-red-50 border-red-200';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200';
      default:
        return 'bg-blue-50 border-blue-200';
    }
  };

  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    } else {
      onClose();
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <IoCloseSharp className="text-xl" />
          </button>
        </div>

        {/* Content */}
        <div className={`p-4 border-l-4 ${getBackgroundColor()}`}>
          <div className="flex items-start space-x-3">
            {getIcon()}
            <div className="flex-1">
              <p className="text-gray-700">{message}</p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 p-4 bg-gray-50">
          {showCancel && (
            <button
              onClick={handleCancel}
              className="px-4 py-2 text-gray-600 bg-white border border-gray-300 rounded hover:bg-gray-50 transition-colors"
            >
              {cancelText}
            </button>
          )}
          <button
            onClick={handleConfirm}
            className={`px-4 py-2 text-white rounded transition-colors ${
              type === 'error' ? 'bg-red-500 hover:bg-red-600' :
              type === 'success' ? 'bg-green-500 hover:bg-green-600' :
              type === 'warning' ? 'bg-yellow-500 hover:bg-yellow-600' :
              'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Modal; 