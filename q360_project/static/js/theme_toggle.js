/**
 * Universal Dark Mode Toggle for Q360 Platform
 * Works across all user-facing pages (not just admin)
 * Supports: localStorage persistence, system preference detection, smooth transitions
 */

(function() {
    'use strict';

    const STORAGE_KEY = 'q360-theme';
    const DARK_CLASS = 'dark';

    /**
     * Apply theme to document
     * @param {string} theme - 'dark' or 'light'
     */
    function applyTheme(theme) {
        const isDark = theme === 'dark';
        const html = document.documentElement;

        if (isDark) {
            html.classList.add(DARK_CLASS);
        } else {
            html.classList.remove(DARK_CLASS);
        }

        // Store preference
        localStorage.setItem(STORAGE_KEY, theme);

        // Update meta theme-color for mobile browsers
        updateMetaThemeColor(isDark);

        // Dispatch custom event for other scripts to listen
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    /**
     * Update mobile browser theme color
     * @param {boolean} isDark
     */
    function updateMetaThemeColor(isDark) {
        let metaTheme = document.querySelector('meta[name="theme-color"]');
        if (!metaTheme) {
            metaTheme = document.createElement('meta');
            metaTheme.name = 'theme-color';
            document.head.appendChild(metaTheme);
        }
        metaTheme.content = isDark ? '#1f2937' : '#2563eb';
    }

    /**
     * Toggle between dark and light mode
     */
    function toggleDarkMode() {
        const currentTheme = localStorage.getItem(STORAGE_KEY) || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }

    /**
     * Get initial theme based on preference
     * Priority: 1. localStorage 2. system preference 3. default light
     */
    function getInitialTheme() {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            return stored;
        }

        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }

        return 'light';
    }

    /**
     * Initialize theme on page load
     */
    function initializeTheme() {
        const theme = getInitialTheme();
        applyTheme(theme);

        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                // Only auto-switch if user hasn't set manual preference
                if (!localStorage.getItem(STORAGE_KEY)) {
                    applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    // Initialize immediately to prevent flash
    initializeTheme();

    // Make toggleDarkMode globally available
    window.toggleDarkMode = toggleDarkMode;

    // Reinitialize on DOMContentLoaded for any dynamic elements
    document.addEventListener('DOMContentLoaded', () => {
        // Add smooth transition after initial load (prevents flash on page load)
        setTimeout(() => {
            document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        }, 100);
    });

})();
