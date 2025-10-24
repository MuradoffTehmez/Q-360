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
// This will call the getAccessToken function defined in api-utils.js
Storage.prototype.getItem = function(key) {
    // If requesting access_token, try to use our unified getAccessToken function if available
    if (key === 'access_token' && typeof window.getAccessToken === 'function') {
        return window.getAccessToken();
    }
    // Otherwise, use original behavior
    return window._originalStorageMethods.getItem.call(this, key);
};

// Override localStorage.setItem to sync cookies when access_token is set
Storage.prototype.setItem = function(key, value) {
    // If setting access_token, also set in cookie for server-side access
    if (key === 'access_token') {
        // Set cookie that expires in 1 hour
        const expiration = new Date();
        expiration.setTime(expiration.getTime() + 60 * 60 * 1000); // 1 hour
        document.cookie = `${key}=${value}; expires=${expiration.toUTCString()}; path=/; samesite=lax`;
    }
    // Use original behavior
    return window._originalStorageMethods.setItem.call(this, key, value);
};

// Override localStorage.removeItem to also remove cookie when access_token is removed
Storage.prototype.removeItem = function(key) {
    // If removing access_token, also remove from cookie
    if (key === 'access_token') {
        document.cookie = `${key}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    }
    // Use original behavior
    return window._originalStorageMethods.removeItem.call(this, key);
};

// Helper function: create headers with auth token
window.createAuthHeaders = function() {
    const token = typeof window.getAccessToken === 'function' ? window.getAccessToken() : null;
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': typeof window.getCSRFToken === 'function' ? window.getCSRFToken() : ''
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
        if (typeof window.apiGet === 'function') {
            return await window.apiGet(url);
        }
    } else if (options.method === 'POST' && typeof window.apiPost === 'function') {
        return await window.apiPost(url, options.body ? JSON.parse(options.body) : {});
    } else if (options.method === 'PUT' && typeof window.apiPut === 'function') {
        return await window.apiPut(url, options.body ? JSON.parse(options.body) : {});
    } else if (options.method === 'DELETE' && typeof window.apiDelete === 'function') {
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
        if (typeof window.showToast === 'function') {
            window.showToast('Səlahiyyətiniz bitib. Yenidən daxil olun.', 'error');
        }
        setTimeout(() => {
            window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
        }, 2000);
        throw new Error('Unauthorized');
    }

    if (response.status === 403) {
        if (typeof window.showToast === 'function') {
            window.showToast('Bu əməliyyat üçün icazəniz yoxdur.', 'error');
        }
        throw new Error('Forbidden');
    }

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.message || errorData.detail || 'Xəta baş verdi';
        if (typeof window.showToast === 'function') {
            window.showToast(errorMessage, 'error');
        }
        throw new Error(errorMessage);
    }

    return response.json();
};

console.log('Q360 Auth Fix loaded - unified token access enabled');
