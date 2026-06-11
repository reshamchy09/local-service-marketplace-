// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== AOS Initialization ====================
    if (typeof AOS !== 'undefined') {
        AOS.init({ 
            duration: 800, 
            once: true, 
            offset: 100,
            disable: window.innerWidth < 768 // Disable on mobile for performance
        });
    } else {
        console.warn('AOS library not loaded');
    }

    // ==================== Sticky Navbar ====================
    const nav = document.querySelector('.navbar'); // Changed from .sticky-navbar
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                nav.classList.add('shadow-lg');
                nav.classList.add('bg-white');
            } else {
                nav.classList.remove('shadow-lg');
                nav.classList.remove('bg-white');
            }
        });
    }

    // ==================== Scroll to Top Button ====================
    const scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                scrollBtn.style.display = 'flex';
                scrollBtn.style.opacity = '1';
            } else {
                scrollBtn.style.display = 'none';
                scrollBtn.style.opacity = '0';
            }
        });
        
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({ 
                top: 0, 
                behavior: 'smooth' 
            });
        });
    }

    // ==================== Dark Mode Toggle ====================
    const darkToggle = document.getElementById('darkModeToggle');
    if (darkToggle) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
        
        darkToggle.addEventListener('click', function() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            showToast(newTheme === 'dark' ? 'Dark mode activated 🌙' : 'Light mode activated ☀️', 'success');
        });
    }

    // ==================== Toast Notifications ====================
    // Create toast container if it doesn't exist
    if (!document.querySelector('.toast-container')) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
    }
    
    window.showToast = function(message, type = 'info') {
        const container = document.querySelector('.toast-container');
        if (!container) return;
        
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${getToastColor(type)} border-0 fade show`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${getToastIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        container.appendChild(toastEl);
        
        // Initialize Bootstrap toast if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
            const bsToast = new bootstrap.Toast(toastEl, { delay: 3000 });
            bsToast.show();
        } else {
            // Fallback if Bootstrap JS not loaded
            toastEl.style.display = 'block';
            setTimeout(() => {
                toastEl.remove();
            }, 3000);
        }
        
        // Auto-remove after animation
        toastEl.addEventListener('hidden.bs.toast', function() {
            toastEl.remove();
        });
        
        // Fallback removal
        setTimeout(() => {
            if (toastEl.parentNode) toastEl.remove();
        }, 3500);
    };
    
    // Helper function for toast colors
    function getToastColor(type) {
        const colors = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'primary'
        };
        return colors[type] || 'primary';
    }
    
    // Helper function for toast icons
    function getToastIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || 'fa-info-circle';
    }

    // ==================== Loading Spinner ====================
    window.showLoader = function(show) {
        let spinner = document.getElementById('loadingSpinner');
        
        if (!spinner) {
            // Create spinner if it doesn't exist
            spinner = document.createElement('div');
            spinner.id = 'loadingSpinner';
            spinner.className = 'd-none';
            spinner.innerHTML = `
                <div class="position-fixed top-50 start-50 translate-middle z-3">
                    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="position-fixed top-0 start-0 w-100 h-100 bg-dark opacity-25 z-2"></div>
            `;
            document.body.appendChild(spinner);
        }
        
        if (show) {
            spinner.classList.remove('d-none');
        } else {
            spinner.classList.add('d-none');
        }
    };

    // ==================== Animated Counters ====================
    const counters = document.querySelectorAll('.counter');
    
    if (counters.length > 0) {
        const animateCounter = (el) => {
            const target = parseInt(el.getAttribute('data-target'));
            const duration = 2000; // 2 seconds
            const step = Math.ceil(target / (duration / 16)); // 60fps
            let current = 0;
            
            const updateCounter = () => {
                current += step;
                if (current < target) {
                    el.innerText = current;
                    requestAnimationFrame(updateCounter);
                } else {
                    el.innerText = target;
                }
            };
            
            updateCounter();
        };
        
        // Use Intersection Observer for counters
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            counters.forEach(counter => observer.observe(counter));
        } else {
            // Fallback for older browsers
            counters.forEach(counter => animateCounter(counter));
        }
    }

    // ==================== Newsletter Subscription ====================
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = form.querySelector('input[type="email"]')?.value;
            
            if (email) {
                showToast(`Thanks for subscribing! (Demo)`, 'success');
                form.reset();
                
                // You can add AJAX call here to save email to database
                // Example:
                // try {
                //     const response = await fetch('/api/newsletter/subscribe/', {
                //         method: 'POST',
                //         headers: { 'Content-Type': 'application/json' },
                //         body: JSON.stringify({ email: email })
                //     });
                //     if (response.ok) showToast('Subscribed successfully!', 'success');
                // } catch (error) {
                //     showToast('Subscription failed. Please try again.', 'error');
                // }
            } else {
                showToast('Please enter a valid email address', 'warning');
            }
        });
    });

    // ==================== Smooth Scrolling for Anchor Links ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            // Skip if it's just "#" or empty
            if (targetId === "#" || targetId === "" || targetId === "#0") {
                return;
            }
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without jumping (optional)
                history.pushState(null, null, targetId);
            }
        });
    });

    // ==================== Testimonial Carousel ====================
    if (document.querySelector('#testimonialCarousel')) {
        if (typeof bootstrap !== 'undefined' && bootstrap.Carousel) {
            new bootstrap.Carousel('#testimonialCarousel', { 
                interval: 4000,
                ride: 'carousel',
                pause: 'hover'
            });
        }
    }

    // ==================== Search Functionality Demo ====================
    const searchIcon = document.querySelector('.search-icon');
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            showToast('Search functionality coming soon!', 'info');
        });
    }
    
    // ==================== Provider Card Hover Effect ====================
    const providerCards = document.querySelectorAll('.provider-card, .category-card');
    providerCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ==================== Modal Back Handler ====================
    // Handle browser back button when modal is open
    window.addEventListener('popstate', function() {
        const modal = document.querySelector('.modal.show');
        if (modal) {
            window.location.href = window.location.pathname;
        }
    });
    
    // ==================== Lazy Loading Images ====================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ==================== Console Log for Debug (Remove in production) ====================
    console.log('✅ LocalServiceHub JS initialized successfully');
});