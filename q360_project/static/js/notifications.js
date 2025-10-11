// Real-time notifications using WebSockets
class NotificationManager {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.retryCount = 0;
        this.maxRetries = 5;
        this.retryDelay = 1000; // 1 second
        
        this.init();
    }
    
    init() {
        // Only connect if user is authenticated
        if (this.isUserAuthenticated()) {
            this.connectWebSocket();
        }
        
        // Update notification badge on page load
        this.updateNotificationBadge();
        
        // Add event listeners
        this.addEventListeners();
    }
    
    isUserAuthenticated() {
        // Check if user is authenticated (check for token or user session)
        return document.querySelector('[data-user-id]') !== null;
    }
    
    connectWebSocket() {
        // Get CSRF token if needed
        const csrfToken = this.getCookie('csrftoken');
        
        // WebSocket URL - adjust the URL based on your deployment
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = (event) => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.retryCount = 0;
                
                // Update UI to show connection status
                this.updateConnectionStatus(true);
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'notification') {
                    this.handleNotification(data.message);
                }
            };
            
            this.ws.onclose = (event) => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                
                // Attempt to reconnect with exponential backoff
                if (this.retryCount < this.maxRetries) {
                    this.retryCount++;
                    setTimeout(() => {
                        this.connectWebSocket();
                    }, this.retryDelay * this.retryCount);
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateConnectionStatus(false);
            };
            
        } catch (error) {
            console.error('Error connecting to WebSocket:', error);
        }
    }
    
    handleNotification(notification) {
        // Display the notification
        this.displayNotification(notification);
        
        // Update the notification count badge
        this.updateNotificationBadge(true);
        
        // Update recent notifications list if present
        this.updateRecentNotifications(notification);
        
        // Play notification sound if available
        this.playNotificationSound();
    }
    
    displayNotification(notification) {
        // Create notification element
        const notificationEl = document.createElement('div');
        notificationEl.className = `notification-item animate-fade-in-up ${notification.is_read ? 'read' : 'unread'} bg-${notification.type}-50 dark:bg-${notification.type}-500/10 border border-${notification.type}-200 dark:border-${notification.type}-500 rounded-xl p-4 mb-3 cursor-pointer`;
        notificationEl.dataset.notificationId = notification.id;
        
        notificationEl.innerHTML = `
            <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                    <h4 class="text-sm font-semibold text-${notification.type}-700 dark:text-${notification.type}-200 truncate">${notification.title}</h4>
                    <p class="mt-1 text-xs text-gray-600 dark:text-gray-300">${notification.message}</p>
                    <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">${this.formatTime(notification.timestamp)}</p>
                </div>
                <button type="button" class="ml-3 text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400" onclick="notificationManager.markAsRead(${notification.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add click event to mark as read and redirect if link exists
        notificationEl.addEventListener('click', () => {
            this.markAsRead(notification.id);
            if (notification.link) {
                window.location.href = notification.link;
            }
        });
        
        // Insert at the beginning of the notifications container
        const container = document.querySelector('#recent-notifications-container');
        if (container) {
            if (container.firstChild) {
                container.insertBefore(notificationEl, container.firstChild);
            } else {
                container.appendChild(notificationEl);
            }
            
            // Limit to 5 recent notifications
            if (container.children.length > 5) {
                container.removeChild(container.lastChild);
            }
        }
        
        // Also show a toast notification
        this.showToastNotification(notification);
    }
    
    showToastNotification(notification) {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast-notification fixed top-4 right-4 z-50 max-w-sm w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg border-l-4 border-${notification.type}-500 p-4 transform transition-transform duration-300`;
        toast.style.transform = 'translateX(150%)';
        toast.style.animation = 'slideIn 0.3s forwards';
        toast.innerHTML = `
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    <i class="fas fa-${this.getIconForType(notification.type)} text-${notification.type}-500"></i>
                </div>
                <div class="ml-3 flex-1">
                    <h3 class="text-sm font-medium text-gray-900 dark:text-white">${notification.title}</h3>
                    <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">${notification.message}</p>
                </div>
                <button type="button" class="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-500" onclick="this.closest('.toast-notification').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 10);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.transform = 'translateX(150%)';
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
    
    updateNotificationBadge(increment = false) {
        // Update notification count badge
        fetch('/notifications/api/unread-count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.querySelector('[data-notification-badge]');
                if (badge) {
                    const count = data.count || 0;
                    if (count > 0) {
                        badge.textContent = count > 99 ? '99+' : count;
                        badge.classList.remove('hidden');
                    } else {
                        badge.classList.add('hidden');
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching notification count:', error);
            });
    }
    
    updateRecentNotifications(notification) {
        // Update the recent notifications dropdown
        // This is handled by the displayNotification method
    }
    
    updateConnectionStatus(connected) {
        const statusEl = document.querySelector('[data-websocket-status]');
        if (statusEl) {
            statusEl.className = connected ? 
                'w-3 h-3 rounded-full bg-green-500' : 
                'w-3 h-3 rounded-full bg-red-500';
        }
    }
    
    markAsRead(notificationId) {
        // Mark notification as read via AJAX
        fetch(`/notifications/${notificationId}/read/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update UI to mark as read
                const notificationEl = document.querySelector(`[data-notification-id="${notificationId}"]`);
                if (notificationEl) {
                    notificationEl.classList.remove('unread');
                    notificationEl.classList.add('read');
                }
                this.updateNotificationBadge();
            }
        })
        .catch(error => {
            console.error('Error marking notification as read:', error);
        });
    }
    
    playNotificationSound() {
        // Play notification sound if available
        // You can add a notification sound file and play it here
        // Example:
        /*
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.play().catch(e => console.log('Notification sound error:', e));
        */
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.round(diffMs / 60000);
        
        if (diffMins < 1) {
            return 'Az əvvəl';
        } else if (diffMins < 60) {
            return `${diffMins} dəqiqə əvvəl`;
        } else if (diffMins < 1440) { // 24 hours
            const hours = Math.floor(diffMins / 60);
            return `${hours} saat əvvəl`;
        } else {
            const days = Math.floor(diffMins / 1440);
            return `${days} gün əvvəl`;
        }
    }
    
    getIconForType(type) {
        switch(type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            default: return 'bell';
        }
    }
    
    getCookie(name) {
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
    
    addEventListeners() {
        // Add event listener to mark all as read button
        const markAllReadBtn = document.querySelector('[data-mark-all-read]');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', () => {
                fetch('/notifications/mark-all-read/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': this.getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Update UI
                        const notifications = document.querySelectorAll('.notification-item');
                        notifications.forEach(notification => {
                            notification.classList.remove('unread');
                            notification.classList.add('read');
                        });
                        this.updateNotificationBadge();
                    }
                })
                .catch(error => {
                    console.error('Error marking all as read:', error);
                });
            });
        }
    }
}

// Initialize notification manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.notificationManager = new NotificationManager();
});

// Add CSS animations that we use in the JavaScript
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(150%); }
        to { transform: translateX(0); }
    }
    
    .animate-fade-in-up {
        animation: fadeInUp 0.3s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);