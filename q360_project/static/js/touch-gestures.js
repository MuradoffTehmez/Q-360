// Touch gestures for mobile interactions
class TouchGestures {
    constructor() {
        this.swipeThreshold = 50; // Minimum distance for swipe
        this.startX = 0;
        this.startY = 0;
        this.isSwiping = false;
        
        this.init();
    }
    
    init() {
        // Add touch event listeners
        document.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: true });
        document.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        document.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: true });
        
        // Add swipe functionality for side navigation
        this.initSwipeNavigation();
    }
    
    handleTouchStart(e) {
        // Only respond to single touches
        if (e.touches.length > 1) return;
        
        this.startX = e.touches[0].clientX;
        this.startY = e.touches[0].clientY;
        this.isSwiping = true;
    }
    
    handleTouchMove(e) {
        if (!this.isSwiping) return;
        
        // Prevent scrolling when swiping horizontally
        const diffX = e.touches[0].clientX - this.startX;
        const diffY = e.touches[0].clientY - this.startY;
        
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // Horizontal swipe - prevent vertical scrolling
            e.preventDefault();
        }
    }
    
    handleTouchEnd(e) {
        if (!this.isSwiping) return;
        
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;
        
        const diffX = endX - this.startX;
        const diffY = endY - this.startY;
        
        // Check if it was a significant horizontal swipe
        if (Math.abs(diffX) > this.swipeThreshold && Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX > 0) {
                // Swipe right
                this.handleSwipeRight();
            } else {
                // Swipe left
                this.handleSwipeLeft();
            }
        }
        
        this.isSwiping = false;
    }
    
    handleSwipeLeft() {
        // Handle left swipe (e.g., navigate forward)
        // You can customize this based on your app's navigation
        console.log('Swipe left detected');
        
        // Example: Close sidebar on swipe
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && window.innerWidth < 768) { // Mobile view
            sidebar.classList.add('hidden');
        }
    }
    
    handleSwipeRight() {
        // Handle right swipe (e.g., navigate back)
        console.log('Swipe right detected');
        
        // Example: Open sidebar on swipe
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && window.innerWidth < 768) { // Mobile view
            sidebar.classList.remove('hidden');
        }
    }
    
    initSwipeNavigation() {
        // Add swipe navigation to specific elements
        const swipeAreas = document.querySelectorAll('[data-swipe-nav]');
        swipeAreas.forEach(element => {
            element.addEventListener('touchstart', (e) => {
                this.startX = e.touches[0].clientX;
                this.startY = e.touches[0].clientY;
            }, { passive: true });
            
            element.addEventListener('touchend', (e) => {
                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                
                const diffX = endX - this.startX;
                const diffY = endY - this.startY;
                
                if (Math.abs(diffX) > this.swipeThreshold && Math.abs(diffX) > Math.abs(diffY)) {
                    if (diffX > 0) {
                        // Swipe right - navigate back
                        this.triggerSwipeEvent('swipe-back');
                    } else {
                        // Swipe left - navigate forward
                        this.triggerSwipeEvent('swipe-forward');
                    }
                }
            }, { passive: true });
        });
    }
    
    triggerSwipeEvent(type) {
        // Dispatch custom event for swipe actions
        const event = new CustomEvent('q360:swipe', {
            detail: { type: type }
        });
        document.dispatchEvent(event);
    }
}

// Initialize touch gestures when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.touchGestures = new TouchGestures();
});

// Add CSS for mobile-specific styling
const mobileStyles = document.createElement('style');
mobileStyles.textContent = `
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        .mobile-menu-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 9998;
            display: none;
        }
        
        .sidebar-mobile {
            position: fixed;
            top: 0;
            left: -100%;
            width: 80%;
            height: 100vh;
            z-index: 9999;
            transition: left 0.3s ease;
        }
        
        .sidebar-mobile.active {
            left: 0;
        }
    }
    
    /* Touch-friendly elements */
    .touch-target {
        min-height: 44px; /* Minimum touch target size */
        min-width: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Prevent text selection during swipe */
    .swipe-area {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
`;
document.head.appendChild(mobileStyles);