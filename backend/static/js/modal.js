function showModal(title, message, type = 'info', showCancel = false) {
    return new Promise((resolve) => {
        const modal = document.getElementById('modal');
        const modalHeader = document.getElementById('modal-header');
        const modalMessage = document.getElementById('modal-message');
        const modalCancel = document.getElementById('modal-cancel');
        const modalConfirm = document.getElementById('modal-confirm');
        
        modalHeader.textContent = title;
        modalMessage.textContent = message;
        
        modalCancel.style.display = showCancel ? 'block' : 'none';
        
        modalConfirm.className = 'modal-btn ' + 
            (type === 'error' ? 'modal-btn-confirm' : 
             type === 'success' ? 'modal-btn-success' : 
             'modal-btn-confirm');
        
        modal.style.display = 'flex';
        
        modalConfirm.onclick = () => {
            modal.style.display = 'none';
            resolve(true);
        };
        
        modalCancel.onclick = () => {
            modal.style.display = 'none';
            resolve(false);
        };
        
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                resolve(false);
            }
        };
    });
} 