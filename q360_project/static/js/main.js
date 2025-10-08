/**
 * Q360 - Main JavaScript File
 * Handles common functionality across the application
 */

// Document Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize Application
 */
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();

    // Initialize popovers
    initializePopovers();

    // Load notifications
    loadNotifications();

    // Setup AJAX defaults
    setupAjaxDefaults();

    // Auto-hide alerts
    autoHideAlerts();

    // Initialize form validation
    initializeFormValidation();
}

/**
 * Initialize Bootstrap Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap Popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Load Notifications
 */
function loadNotifications() {
    fetch('/api/notifications/?limit=5')
        .then(response => response.json())
        .then(data => {
            updateNotificationBadge(data.count);
            renderNotifications(data.results);
        })
        .catch(error => console.error('Error loading notifications:', error));
}

/**
 * Update Notification Badge
 */
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationCount');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

/**
 * Render Notifications
 */
function renderNotifications(notifications) {
    const notificationList = document.getElementById('notificationList');
    if (!notificationList) return;

    if (notifications.length === 0) {
        notificationList.innerHTML = `
            <li><h6 class="dropdown-header">Bildirişlər</h6></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-muted" href="#">Bildiriş yoxdur</a></li>
        `;
        return;
    }

    let html = '<li><h6 class="dropdown-header">Bildirişlər</h6></li><li><hr class="dropdown-divider"></li>';

    notifications.forEach(notification => {
        const icon = getNotificationIcon(notification.notification_type);
        html += `
            <li>
                <a class="dropdown-item ${!notification.is_read ? 'fw-bold' : ''}" href="#" onclick="markAsRead(${notification.id})">
                    <i class="${icon} me-2"></i>
                    <div>
                        <div>${notification.title}</div>
                        <small class="text-muted">${notification.message.substring(0, 50)}...</small>
                    </div>
                </a>
            </li>
        `;
    });

    html += `
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item text-center small" href="/notifications/">Hamısını Gör</a></li>
    `;

    notificationList.innerHTML = html;
}

/**
 * Get Notification Icon
 */
function getNotificationIcon(type) {
    const icons = {
        'info': 'fas fa-info-circle text-info',
        'success': 'fas fa-check-circle text-success',
        'warning': 'fas fa-exclamation-triangle text-warning',
        'error': 'fas fa-times-circle text-danger'
    };
    return icons[type] || 'fas fa-bell';
}

/**
 * Mark Notification as Read
 */
function markAsRead(notificationId) {
    fetch(`/api/notifications/${notificationId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(() => loadNotifications())
    .catch(error => console.error('Error marking notification as read:', error));
}

/**
 * Setup AJAX Defaults
 */
function setupAjaxDefaults() {
    // Add CSRF token to all AJAX requests
    const csrftoken = getCookie('csrftoken');

    if (window.jQuery) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafe(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    }
}

/**
 * Check if HTTP method is CSRF safe
 */
function csrfSafe(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

/**
 * Get Cookie by Name
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Auto Hide Alerts
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Show Toast Notification
 */
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();

    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: duration });
    toast.show();

    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Create Toast Container
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Confirm Action
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Delete Item with Confirmation
 */
function deleteItem(url, itemName, redirectUrl) {
    if (confirm(`${itemName} silmək istədiyinizdən əminsiniz?`)) {
        fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                showToast('Uğurla silindi', 'success');
                if (redirectUrl) {
                    window.location.href = redirectUrl;
                } else {
                    location.reload();
                }
            } else {
                showToast('Xəta baş verdi', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Xəta baş verdi', 'danger');
        });
    }
}

/**
 * Initialize Form Validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Format Date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('az-AZ', options);
}

/**
 * Format DateTime
 */
function formatDateTime(dateTimeString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateTimeString).toLocaleDateString('az-AZ', options);
}

/**
 * Debounce Function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Copy to Clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Kopyalandı!', 'success', 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Kopyalama xətası', 'danger');
    });
}

/**
 * Export Table to CSV
 */
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');

        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }

        csv.push(row.join(','));
    }

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');

    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Show Loading Spinner
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.className = 'spinner-wrapper';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Yüklənir...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

/**
 * Hide Loading Spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// Global Error Handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    // Optionally send to error tracking service
});

// Expose functions globally
window.Q360 = {
    showToast,
    confirmAction,
    deleteItem,
    formatDate,
    formatDateTime,
    copyToClipboard,
    exportTableToCSV,
    showLoading,
    hideLoading,
    getCookie
};
