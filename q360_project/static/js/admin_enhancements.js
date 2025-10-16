/**
 * Q360 - Professional Admin Panel JavaScript Enhancements
 * Modern interactions, animations, and utility functions
 */

(function() {
    'use strict';

    // ===== Wait for DOM to be ready =====
    document.addEventListener('DOMContentLoaded', function() {
        console.log('✨ Q360 Admin Enhancements Loaded');

        // Initialize all enhancements
        initSidebarEnhancements();
        initTableEnhancements();
        initFormEnhancements();
        initNotificationSystem();
        initDashboardAnimations();
        initSearchEnhancements();
        initThemeToggle();
        initTooltips();
        initProgressBars();
        initConfirmDialogs();
    });

    // ===== SIDEBAR ENHANCEMENTS =====
    function initSidebarEnhancements() {
        const sidebar = document.querySelector('.main-sidebar');
        if (!sidebar) return;

        // Add active state indicators
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-sidebar .nav-link').forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
                // Expand parent if in treeview
                const parent = link.closest('.nav-treeview');
                if (parent) {
                    const parentItem = parent.closest('.nav-item');
                    if (parentItem) {
                        parentItem.classList.add('menu-open');
                        const parentLink = parentItem.querySelector('.nav-link');
                        if (parentLink) parentLink.classList.add('active');
                    }
                }
            }
        });

        // Smooth collapse/expand animation for treeview
        document.querySelectorAll('.nav-sidebar .has-treeview > a').forEach(link => {
            link.addEventListener('click', function(e) {
                const parent = this.closest('.nav-item');
                const treeview = parent.querySelector('.nav-treeview');

                if (treeview) {
                    if (parent.classList.contains('menu-open')) {
                        treeview.style.maxHeight = treeview.scrollHeight + 'px';
                        setTimeout(() => {
                            treeview.style.maxHeight = '0';
                        }, 10);
                    } else {
                        treeview.style.maxHeight = treeview.scrollHeight + 'px';
                        setTimeout(() => {
                            treeview.style.maxHeight = 'none';
                        }, 300);
                    }
                }
            });
        });

        // Sidebar hover effect for icons
        document.querySelectorAll('.nav-sidebar .nav-icon').forEach(icon => {
            icon.parentElement.addEventListener('mouseenter', function() {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            });
            icon.parentElement.addEventListener('mouseleave', function() {
                icon.style.transform = 'scale(1) rotate(0deg)';
            });
        });
    }

    // ===== TABLE ENHANCEMENTS =====
    function initTableEnhancements() {
        // Add hover effects and animations
        document.querySelectorAll('.table tbody tr').forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateY(20px)';

            setTimeout(() => {
                row.style.transition = 'all 0.3s ease';
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, index * 50);
        });

        // Add row selection highlight
        document.querySelectorAll('.table tbody tr').forEach(row => {
            row.addEventListener('click', function(e) {
                if (e.target.tagName === 'TD') {
                    this.classList.toggle('table-active');
                }
            });
        });

        // Add sortable indicators to table headers
        document.querySelectorAll('.table thead th').forEach(th => {
            if (th.classList.contains('sortable')) {
                th.style.cursor = 'pointer';
                th.innerHTML += ' <i class="fas fa-sort text-muted"></i>';

                th.addEventListener('click', function() {
                    const icon = this.querySelector('i');
                    if (icon.classList.contains('fa-sort')) {
                        icon.classList.remove('fa-sort');
                        icon.classList.add('fa-sort-up');
                    } else if (icon.classList.contains('fa-sort-up')) {
                        icon.classList.remove('fa-sort-up');
                        icon.classList.add('fa-sort-down');
                    } else {
                        icon.classList.remove('fa-sort-down');
                        icon.classList.add('fa-sort-up');
                    }
                });
            }
        });
    }

    // ===== FORM ENHANCEMENTS =====
    function initFormEnhancements() {
        // Auto-focus first input in forms
        const firstInput = document.querySelector('.card-body form input:not([type="hidden"]):first-of-type');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 300);
        }

        // Add character counter to textareas
        document.querySelectorAll('textarea[maxlength]').forEach(textarea => {
            const maxLength = textarea.getAttribute('maxlength');
            const counter = document.createElement('div');
            counter.className = 'text-muted text-sm mt-1';
            counter.textContent = `0 / ${maxLength}`;

            textarea.parentNode.appendChild(counter);

            textarea.addEventListener('input', function() {
                counter.textContent = `${this.value.length} / ${maxLength}`;
                if (this.value.length > maxLength * 0.9) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            });
        });

        // Validate required fields on blur
        document.querySelectorAll('input[required], select[required], textarea[required]').forEach(field => {
            field.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });

        // Password strength indicator
        document.querySelectorAll('input[type="password"]').forEach(password => {
            if (password.name.includes('password') && !password.name.includes('old')) {
                const strength = document.createElement('div');
                strength.className = 'password-strength mt-2';
                strength.innerHTML = `
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                    </div>
                    <small class="text-muted">Password Strength: <span class="strength-text">-</span></small>
                `;
                password.parentNode.appendChild(strength);

                password.addEventListener('input', function() {
                    const value = this.value;
                    let score = 0;

                    if (value.length >= 8) score++;
                    if (/[a-z]/.test(value) && /[A-Z]/.test(value)) score++;
                    if (/\d/.test(value)) score++;
                    if (/[^a-zA-Z0-9]/.test(value)) score++;

                    const progressBar = strength.querySelector('.progress-bar');
                    const strengthText = strength.querySelector('.strength-text');

                    let width, text, colorClass;
                    if (score === 0) {
                        width = 0; text = '-'; colorClass = '';
                    } else if (score === 1) {
                        width = 25; text = 'Weak'; colorClass = 'bg-danger';
                    } else if (score === 2) {
                        width = 50; text = 'Fair'; colorClass = 'bg-warning';
                    } else if (score === 3) {
                        width = 75; text = 'Good'; colorClass = 'bg-info';
                    } else {
                        width = 100; text = 'Strong'; colorClass = 'bg-success';
                    }

                    progressBar.style.width = width + '%';
                    progressBar.className = 'progress-bar ' + colorClass;
                    strengthText.textContent = text;
                });
            }
        });
    }

    // ===== NOTIFICATION SYSTEM =====
    function initNotificationSystem() {
        window.showNotification = function(message, type = 'info', duration = 3000) {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);';
            notification.innerHTML = `
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            `;

            document.body.appendChild(notification);

            // Auto-remove after duration
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 300);
            }, duration);
        };

        // Example usage in admin actions
        document.querySelectorAll('form[method="post"]').forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing...';
                }
            });
        });
    }

    // ===== DASHBOARD ANIMATIONS =====
    function initDashboardAnimations() {
        // Animate small boxes on dashboard
        document.querySelectorAll('.small-box').forEach((box, index) => {
            box.style.opacity = '0';
            box.style.transform = 'translateY(30px)';

            setTimeout(() => {
                box.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                box.style.opacity = '1';
                box.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Animated counter for numbers
        document.querySelectorAll('.small-box .inner h3').forEach(counter => {
            const target = parseInt(counter.textContent);
            if (!isNaN(target)) {
                let current = 0;
                const increment = target / 50;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    } else {
                        counter.textContent = Math.floor(current);
                    }
                }, 20);
            }
        });

        // Card hover effects
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
            });
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    // ===== SEARCH ENHANCEMENTS =====
    function initSearchEnhancements() {
        const searchInput = document.querySelector('input[name="q"], input[type="search"]');
        if (!searchInput) return;

        // Add clear button to search
        const clearBtn = document.createElement('button');
        clearBtn.className = 'btn btn-sm btn-outline-secondary';
        clearBtn.type = 'button';
        clearBtn.innerHTML = '<i class="fas fa-times"></i>';
        clearBtn.style.cssText = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%);';

        if (searchInput.parentElement.style.position !== 'relative') {
            searchInput.parentElement.style.position = 'relative';
        }

        searchInput.parentElement.appendChild(clearBtn);

        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            searchInput.focus();
            clearBtn.style.display = 'none';
        });

        searchInput.addEventListener('input', () => {
            clearBtn.style.display = searchInput.value ? 'block' : 'none';
        });

        // Initially hide clear button
        clearBtn.style.display = searchInput.value ? 'block' : 'none';

        // Add search suggestions (if applicable)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // You can implement AJAX search suggestions here
                console.log('Searching for:', this.value);
            }, 300);
        });
    }

    // ===== THEME TOGGLE =====
    function initThemeToggle() {
        // Add theme toggle button to navbar (optional)
        const navbar = document.querySelector('.main-header .navbar-nav');
        if (!navbar) return;

        const themeToggle = document.createElement('li');
        themeToggle.className = 'nav-item';
        themeToggle.innerHTML = `
            <a class="nav-link" href="#" id="theme-toggle" title="Toggle Theme">
                <i class="fas fa-adjust"></i>
            </a>
        `;

        navbar.appendChild(themeToggle);

        document.getElementById('theme-toggle').addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('adminTheme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        });

        // Load saved theme
        const savedTheme = localStorage.getItem('adminTheme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
        }
    }

    // ===== TOOLTIPS =====
    function initTooltips() {
        // Initialize Bootstrap tooltips if available
        if (typeof $ !== 'undefined' && $.fn.tooltip) {
            $('[data-toggle="tooltip"]').tooltip();
        }

        // Custom tooltip for elements with title attribute
        document.querySelectorAll('[title]').forEach(element => {
            if (!element.hasAttribute('data-toggle')) {
                element.addEventListener('mouseenter', function(e) {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'q360-tooltip';
                    tooltip.textContent = this.getAttribute('title');
                    tooltip.style.cssText = `
                        position: fixed;
                        background: rgba(0,0,0,0.9);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-size: 12px;
                        z-index: 9999;
                        pointer-events: none;
                        white-space: nowrap;
                    `;

                    document.body.appendChild(tooltip);

                    const rect = this.getBoundingClientRect();
                    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';

                    this._tooltip = tooltip;
                });

                element.addEventListener('mouseleave', function() {
                    if (this._tooltip) {
                        this._tooltip.remove();
                        delete this._tooltip;
                    }
                });
            }
        });
    }

    // ===== PROGRESS BARS =====
    function initProgressBars() {
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const width = bar.style.width || bar.getAttribute('aria-valuenow') + '%';
            bar.style.width = '0%';

            setTimeout(() => {
                bar.style.transition = 'width 1s ease-in-out';
                bar.style.width = width;
            }, 100);
        });
    }

    // ===== CONFIRM DIALOGS =====
    function initConfirmDialogs() {
        // Add confirmation to delete actions
        document.querySelectorAll('a[href*="delete"], button[name*="delete"], .btn-danger').forEach(element => {
            if (element.textContent.toLowerCase().includes('delete') ||
                element.textContent.toLowerCase().includes('sil')) {
                element.addEventListener('click', function(e) {
                    if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                        e.preventDefault();
                        return false;
                    }
                });
            }
        });
    }

    // ===== UTILITY FUNCTIONS =====
    window.Q360Admin = {
        // Show loading overlay
        showLoading: function(message = 'Loading...') {
            const overlay = document.createElement('div');
            overlay.id = 'q360-loading-overlay';
            overlay.innerHTML = `
                <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;">
                    <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
                        <div class="spinner-border text-primary mb-3" role="status"></div>
                        <div>${message}</div>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        },

        // Hide loading overlay
        hideLoading: function() {
            const overlay = document.getElementById('q360-loading-overlay');
            if (overlay) overlay.remove();
        },

        // Copy to clipboard
        copyToClipboard: function(text) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success', 2000);
            });
        },

        // Format number with thousand separators
        formatNumber: function(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },

        // Debounce function
        debounce: function(func, wait) {
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
    };

    // Make showNotification globally accessible
    window.showNotification = function(message, type, duration) {
        Q360Admin.showNotification(message, type, duration);
    };

    console.log('✅ Q360 Admin Enhancements Initialized');
})();
