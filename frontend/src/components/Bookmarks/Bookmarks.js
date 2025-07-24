import React, { useState } from 'react'
import { IoTrashSharp } from "react-icons/io5";
import Modal from '../Modal/Modal';

function Bookmarks({ bookmark, onLoad, onDelete }) {
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleLoad = () => {
    if (onLoad) {
      onLoad(bookmark.id);
    }
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = () => {
    if (onDelete) {
      onDelete(bookmark.id);
    }
    setShowDeleteModal(false);
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
  };

  return (
    <>
      <div className="bookmark-item flex justify-between p-2 bg-gray-100 rounded-lg shadow-sm">
        <div className='flex flex-col items-start'>
          <span className="bookmark-title font-semibold">{bookmark.name}</span>
          <div className="bookmark-description text-xs text-gray-600">
            <div>Created: {formatDate(bookmark.created_at)}</div>
            <div>Markers: {bookmark.marker_count} | Obstacles: {bookmark.obstacle_count}</div>
          </div>
          <button 
            className="bookmark-edit-btn text-sm bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 transition-colors duration-200 mt-1"
            onClick={handleLoad}
          >
            Apply to Map
          </button>
        </div>
        <div className="bookmark-actions flex justify-between items-center gap-x-2 pt-2">
          <button 
            className="bookmark-delete-btn text-red-500 hover:text-red-700"
            onClick={handleDeleteClick}
          >
            <IoTrashSharp />
          </button>
        </div>
      </div>

      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Route"
        message={`Are you sure you want to delete "${bookmark.name}"? This action cannot be undone.`}
        type="warning"
        confirmText="Delete"
        cancelText="Cancel"
        showCancel={true}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      />
    </>
  )
}

export default Bookmarks