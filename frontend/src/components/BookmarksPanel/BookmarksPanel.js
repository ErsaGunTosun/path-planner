import React, { useState, useEffect } from 'react'
import { IoCloseSharp, IoSaveSharp } from "react-icons/io5";
import Bookmarks from '../Bookmarks/Bookmarks';
import Modal from '../Modal/Modal';

function BookmarksPanel({ menuBtn, handleMenuBtnClick, onBookmarkLoad }) {
    const [showPanel, setShowPanel] = useState(false);
    const [bookmarks, setBookmarks] = useState([]);
    const [bookmarkName, setBookmarkName] = useState('');
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    
    // Modal states
    const [modal, setModal] = useState({
        isOpen: false,
        title: '',
        message: '',
        type: 'info',
        confirmText: 'OK',
        cancelText: 'Cancel',
        showCancel: false,
        onConfirm: null,
        onCancel: null
    });

    const showModal = (modalConfig) => {
        setModal({
            isOpen: true,
            title: '',
            message: '',
            type: 'info',
            confirmText: 'OK',
            cancelText: 'Cancel',
            showCancel: false,
            onConfirm: null,
            onCancel: null,
            ...modalConfig
        });
    };

    const closeModal = () => {
        setModal(prev => ({ ...prev, isOpen: false }));
    };

    const handleClosePanel = () => {
        setShowPanel(false);
        handleMenuBtnClick("");
    };

    const loadBookmarks = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/bookmarks/list');
            const data = await response.json();
            if (data.status === 'success') {
                setBookmarks(data.bookmarks);
            } else {
                console.error('Error loading bookmarks:', data.message);
                showModal({
                    title: 'Error',
                    message: 'Error loading bookmarks: ' + data.message,
                    type: 'error'
                });
            }
        } catch (error) {
            console.error('Error loading bookmarks:', error);
            showModal({
                title: 'Error',
                message: 'Error loading bookmarks. Please try again.',
                type: 'error'
            });
        } finally {
            setLoading(false);
        }
    };

    const saveBookmark = async () => {
        if (!bookmarkName.trim()) {
            showModal({
                title: 'Input Required',
                message: 'Please enter a bookmark name',
                type: 'warning'
            });
            return;
        }

        setSaving(true);
        try {
            const formData = new FormData();
            formData.append('name', bookmarkName.trim());

            const response = await fetch('http://127.0.0.1:5000/bookmark/save', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.status === 'success') {
                setBookmarkName('');
                loadBookmarks();
                showModal({
                    title: 'Success',
                    message: `Route "${data.bookmark.name}" saved successfully!`,
                    type: 'success'
                });
            } else {
                showModal({
                    title: 'Error',
                    message: 'Error saving bookmark: ' + data.message,
                    type: 'error'
                });
            }
        } catch (error) {
            console.error('Error saving bookmark:', error);
            showModal({
                title: 'Error',
                message: 'Error saving bookmark. Please try again.',
                type: 'error'
            });
        } finally {
            setSaving(false);
        }
    };

    const loadBookmark = async (bookmarkId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/bookmark/load/${bookmarkId}`, {
                method: 'POST'
            });

            const data = await response.json();
            if (data.status === 'success') {
                showModal({
                    title: 'Success',
                    message: `Route "${data.bookmark.name}" loaded successfully!`,
                    type: 'success'
                });
                // Trigger map refresh
                if (onBookmarkLoad) {
                    onBookmarkLoad();
                }
            } else {
                showModal({
                    title: 'Error',
                    message: 'Error loading bookmark: ' + data.message,
                    type: 'error'
                });
            }
        } catch (error) {
            console.error('Error loading bookmark:', error);
            showModal({
                title: 'Error',
                message: 'Error loading bookmark. Please try again.',
                type: 'error'
            });
        }
    };

    const deleteBookmark = async (bookmarkId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/bookmark/delete/${bookmarkId}`, {
                method: 'DELETE'
            });

            const data = await response.json();
            if (data.status === 'success') {
                loadBookmarks();
                showModal({
                    title: 'Success',
                    message: data.message,
                    type: 'success'
                });
            } else {
                showModal({
                    title: 'Error',
                    message: 'Error deleting bookmark: ' + data.message,
                    type: 'error'
                });
            }
        } catch (error) {
            console.error('Error deleting bookmark:', error);
            showModal({
                title: 'Error',
                message: 'Error deleting bookmark. Please try again.',
                type: 'error'
            });
        }
    };

    useEffect(() => {
        if (menuBtn === "bookmarks") {
            setShowPanel(true);
            loadBookmarks();
        } else {
            setShowPanel(false);
        }
    }, [menuBtn]);

    return (
        <>
            <div id="bookmarks" className={`overlay-panel bg-white fixed bottom-5 left-5 w-80 max-h-96 rounded-lg z-50 pb-5 ${showPanel ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'} transition-all duration-300 ease-in-out`}>
                <div className="panel-header px-4 py-2 flex items-center justify-between bg-gray shadow-sm rounded-t-lg">
                    <span>Bookmarks</span>
                    <button className="close-btn" onClick={() => handleClosePanel()}>
                        <IoCloseSharp />
                    </button>
                </div>
                
                <div className="save-section p-3 border-b border-gray-200">
                    <div className="flex gap-2 mb-2">
                        <input
                            type="text"
                            value={bookmarkName}
                            onChange={(e) => setBookmarkName(e.target.value)}
                            placeholder="Enter route name..."
                            className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
                            onKeyPress={(e) => e.key === 'Enter' && saveBookmark()}
                        />
                        <button
                            onClick={saveBookmark}
                            disabled={saving}
                            className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 disabled:opacity-50 flex items-center gap-1"
                        >
                            <IoSaveSharp />
                            {saving ? 'Saving...' : 'Save'}
                        </button>
                    </div>
                </div>

                <div className="panel-content flex flex-col gap-y-3 p-3 overflow-y-auto max-h-64">
                    {loading ? (
                        <div className="text-center text-gray-500 py-4">Loading bookmarks...</div>
                    ) : bookmarks.length === 0 ? (
                        <div className="text-center text-gray-500 py-4">
                            <p>No saved routes yet</p>
                            <p className="text-xs">Create a path and save it!</p>
                        </div>
                    ) : (
                        bookmarks.map((bookmark) => (
                            <Bookmarks
                                key={bookmark.id}
                                bookmark={bookmark}
                                onLoad={loadBookmark}
                                onDelete={deleteBookmark}
                            />
                        ))
                    )}
                </div>
            </div>

            <Modal
                isOpen={modal.isOpen}
                onClose={closeModal}
                title={modal.title}
                message={modal.message}
                type={modal.type}
                confirmText={modal.confirmText}
                cancelText={modal.cancelText}
                showCancel={modal.showCancel}
                onConfirm={modal.onConfirm}
                onCancel={modal.onCancel}
            />
        </>
    )
}

export default BookmarksPanel