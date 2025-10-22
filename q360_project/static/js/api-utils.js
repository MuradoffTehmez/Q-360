/**
 * Q360 API Utilities
 * Universal functions for API calls with authentication
 */

/**
 * Get CSRF token from cookies
 */
function getCSRFToken() {
    const name = 'csrftoken';
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
 * Get access token from cookies or localStorage (fallback)
 */
function getAccessToken() {
    // First try cookie (preferred method)
    const name = 'access_token';
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

    // If found in cookie, also sync to localStorage for legacy code
    if (cookieValue) {
        localStorage.setItem('access_token', cookieValue);
        return cookieValue;
    }

    // Fallback to localStorage (for legacy code)
    return localStorage.getItem('access_token');
}

/**
 * Universal API fetch function with authentication
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @param {boolean} useJWT - Whether to use JWT token (default: true)
 * @returns {Promise} - Fetch promise
 */
async function apiFetch(url, options = {}, useJWT = true) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'same-origin', // Include cookies
    };

    // Add JWT token if needed
    if (useJWT) {
        const token = getAccessToken();
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }
    }

    // Merge options
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {}),
        },
    };

    try {
        const response = await fetch(url, mergedOptions);

        // Handle 401 Unauthorized
        if (response.status === 401) {
            showToast('Səlahiyyətiniz bitib. Yenidən daxil olun.', 'error');
            setTimeout(() => {
                window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
            }, 2000);
            throw new Error('Unauthorized');
        }

        // Handle 403 Forbidden
        if (response.status === 403) {
            showToast('Bu əməliyyat üçün icazəniz yoxdur.', 'error');
            throw new Error('Forbidden');
        }

        // Handle other errors
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.message || errorData.detail || 'Xəta baş verdi';
            showToast(errorMessage, 'error');
            throw new Error(errorMessage);
        }

        return response;
    } catch (error) {
        if (error.message !== 'Unauthorized' && error.message !== 'Forbidden') {
            console.error('API Error:', error);
            showToast('Şəbəkə xətası. Zəhmət olmasa yenidən cəhd edin.', 'error');
        }
        throw error;
    }
}

/**
 * Shorthand for GET requests
 */
async function apiGet(url, useJWT = true) {
    const response = await apiFetch(url, { method: 'GET' }, useJWT);
    return response.json();
}

/**
 * Shorthand for POST requests
 */
async function apiPost(url, data, useJWT = true) {
    const response = await apiFetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
    }, useJWT);
    return response.json();
}

/**
 * Shorthand for PUT requests
 */
async function apiPut(url, data, useJWT = true) {
    const response = await apiFetch(url, {
        method: 'PUT',
        body: JSON.stringify(data),
    }, useJWT);
    return response.json();
}

/**
 * Shorthand for DELETE requests
 */
async function apiDelete(url, useJWT = true) {
    const response = await apiFetch(url, { method: 'DELETE' }, useJWT);
    return response.json();
}

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type: success, error, warning, info
 * @param {number} duration - Duration in ms (default: 3000)
 */
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.q360-toast');
    existingToasts.forEach(toast => toast.remove());

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `q360-toast q360-toast-${type}`;

    // Icon based on type
    const icons = {
        success: '<i class="fas fa-check-circle"></i>',
        error: '<i class="fas fa-exclamation-circle"></i>',
        warning: '<i class="fas fa-exclamation-triangle"></i>',
        info: '<i class="fas fa-info-circle"></i>',
    };

    toast.innerHTML = `
        <div class="q360-toast-content">
            <span class="q360-toast-icon">${icons[type] || icons.info}</span>
            <span class="q360-toast-message">${message}</span>
            <button class="q360-toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Add to body
    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add('q360-toast-show'), 10);

    // Auto remove
    setTimeout(() => {
        toast.classList.remove('q360-toast-show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    if (!element) return;

    const spinner = document.createElement('div');
    spinner.className = 'q360-loading-spinner';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    element.style.position = 'relative';
    element.style.opacity = '0.5';
    element.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    if (!element) return;

    const spinner = element.querySelector('.q360-loading-spinner');
    if (spinner) {
        spinner.remove();
    }
    element.style.opacity = '1';
}

// Make functions globally available
window.apiFetch = apiFetch;
window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiPut = apiPut;
window.apiDelete = apiDelete;
window.showToast = showToast;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.getCSRFToken = getCSRFToken;
window.getAccessToken = getAccessToken;
