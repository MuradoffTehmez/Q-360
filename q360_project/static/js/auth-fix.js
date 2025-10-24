/**
 * Q360 Authentication Fix - Universal token helper
 * Auto-fixes all pages that use localStorage.getItem('access_token')
 */

// Save original Storage methods globally BEFORE any override
window._originalStorageMethods = {
    getItem: Storage.prototype.getItem,
    setItem: Storage.prototype.setItem,
    removeItem: Storage.prototype.removeItem
};

// Override localStorage.getItem to use getAccessToken when available
if (window.getAccessToken && window.Storage) {
    Storage.prototype.getItem = function(key) {
        // If requesting access_token, use our unified getAccessToken function
        if (key === 'access_token' && window.getAccessToken) {
            return window.getAccessToken();
        }
        // Otherwise, use original behavior
        return window._originalStorageMethods.getItem.call(this, key);
    };
}

// Helper function: create headers with auth token
window.createAuthHeaders = function() {
    const token = window.getAccessToken ? window.getAccessToken() : null;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': window.getCSRFToken ? window.getCSRFToken() : ''
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
};

// Helper: unified fetch with auth and error handling
window.unifiedFetch = async function(url, options = {}) {
    // Use apiGet, apiPost, etc. if available
    if (options.method === 'GET' || !options.method) {
        if (window.apiGet) {
            return await window.apiGet(url);
        }
    } else if (options.method === 'POST' && window.apiPost) {
        return await window.apiPost(url, options.body ? JSON.parse(options.body) : {});
    } else if (options.method === 'PUT' && window.apiPut) {
        return await window.apiPut(url, options.body ? JSON.parse(options.body) : {});
    } else if (options.method === 'DELETE' && window.apiDelete) {
        return await window.apiDelete(url);
    }

    // Fallback to regular fetch with auth headers
    const defaultOptions = {
        headers: window.createAuthHeaders(),
        credentials: 'same-origin'
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    const response = await fetch(url, mergedOptions);

    // Handle errors
    if (response.status === 401) {
        if (window.showToast) {
            window.showToast('Səlahiyyətiniz bitib. Yenidən daxil olun.', 'error');
        }
        setTimeout(() => {
            window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
        }, 2000);
        throw new Error('Unauthorized');
    }

    if (response.status === 403) {
        if (window.showToast) {
            window.showToast('Bu əməliyyat üçün icazəniz yoxdur.', 'error');
        }
        throw new Error('Forbidden');
    }

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.message || errorData.detail || 'Xəta baş verdi';
        if (window.showToast) {
            window.showToast(errorMessage, 'error');
        }
        throw new Error(errorMessage);
    }

    return response.json();
};

console.log('Q360 Auth Fix loaded - unified token access enabled');
