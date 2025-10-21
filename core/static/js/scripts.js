// === Smooth Scrolling ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});


// === Navbar Scroll Effect ===
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
    }
});


// === Counter Animation ===
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        let current = 0;
        const increment = target / 30;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target + '+';
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current) + '+';
            }
        }, 30);
    });
}


// === Notification System ===
function showNotification(message, type = 'success') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.custom-alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    const bgColor = type === 'success' ? 'rgba(0, 200, 83, 0.1)' : 'rgba(244, 67, 54, 0.1)';
    const borderColor = type === 'success' ? 'rgba(0, 200, 83, 0.3)' : 'rgba(244, 67, 54, 0.3)';

    const alertHTML = `
        <div class="custom-alert alert ${alertClass} alert-dismissible fade show position-fixed"
             style="top: 100px; right: 20px; z-index: 9999; background: ${bgColor}; border: 1px solid ${borderColor}; color: #ffffff; border-radius: 12px; backdrop-filter: blur(10px); min-width: 300px; max-width: 400px;" 
             role="alert">
            <div class="d-flex align-items-center">
                <i class="${icon} me-2" style="font-size: 1.2rem;"></i>
                <span style="flex: 1;">${message}</span>
                <button type="button" class="btn-close btn-close-white ms-3" data-bs-dismiss="alert" style="filter: brightness(0) invert(1);"></button>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', alertHTML);

    // Auto remove after 4 seconds
    setTimeout(() => {
        const alert = document.querySelector('.custom-alert');
        if (alert) {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100px)';
            alert.style.transition = 'all 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }
    }, 4000);
}


// === Scroll to Top ===
function initializeScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.setAttribute('aria-label', 'بازگشت به بالا');
    document.body.appendChild(scrollBtn);

    function toggleScrollButton() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }

    window.addEventListener('scroll', toggleScrollButton);

    scrollBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Initial check
    toggleScrollButton();
}


// === Intersection Observer for Animations ===
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.classList.contains('hero-section')) {
                animateCounters();
            }
            entry.target.classList.add('animate-in');

            // Stop observing after animation
            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});


// === Initialize Portfolio Animations ===
function initializePortfolioAnimations() {
    const portfolioCards = document.querySelectorAll('.portfolio-card');

    portfolioCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('new-project');
    });

    // Add click animation
    portfolioCards.forEach(card => {
        card.addEventListener('click', function (e) {
            if (!e.target.closest('a') && !e.target.closest('button')) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            }
        });
    });
}


// === Initialize when page loads ===
document.addEventListener('DOMContentLoaded', function () {
    console.log('Portfolio website loaded successfully!');

    // Initialize all components
    initializeScrollToTop();
    initializePortfolioAnimations();

    // Initialize intersection observer for animations
    const sections = document.querySelectorAll('section');
    const cards = document.querySelectorAll('.service-card, .portfolio-card');

    sections.forEach(section => observer.observe(section));
    cards.forEach(card => observer.observe(card));

    // Add loading state to all buttons with loading-spinner
    document.querySelectorAll('button .loading-spinner').forEach(spinner => {
        spinner.style.display = 'none';
    });
});


// === Error Handling ===
window.addEventListener('error', function (e) {
    console.error('Global error:', e.error);
    showNotification('خطایی در اجرای صفحه رخ داده است', 'error');
});