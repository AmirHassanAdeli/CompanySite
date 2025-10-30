// === تمام کدهای قبلی + فرم تماس (بدون jQuery) ===

document.addEventListener('DOMContentLoaded', function () {
    console.log('Portfolio website loaded successfully!');

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        });
    });

    // Navbar Effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.background = window.scrollY > 50
                ? 'rgba(10, 10, 10, 0.98)'
                : 'rgba(10, 10, 10, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
    });

    // Counter Animation
    function animateCounters() {
        document.querySelectorAll('.stat-number').forEach(counter => {
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

    // Notification System
    window.showNotification = function (message, type = 'success') {
        const existing = document.querySelectorAll('.custom-alert');
        existing.forEach(a => a.remove());

        const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
        const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
        const bg = type === 'success' ? 'rgba(0, 200, 83, 0.1)' : 'rgba(244, 67, 54, 0.1)';
        const border = type === 'success' ? 'rgba(0, 200, 83, 0.3)' : 'rgba(244, 67, 54, 0.3)';

        const alertHTML = `
            <div class="custom-alert alert ${alertClass} position-fixed fade show"
                 style="top: 100px; right: 20px; z-index: 9999; background: ${bg}; border: 1px solid ${border}; color: #fff; border-radius: 12px; backdrop-filter: blur(10px); min-width: 300px; max-width: 400px;"
                 role="alert">
                <div class="d-flex align-items-center p-3">
                    <i class="${icon} me-2" style="font-size: 1.2rem;"></i>
                    <span style="flex: 1;">${message}</span>
                    <button type="button" class="btn-close btn-close-white ms-3" onclick="this.parentElement.parentElement.remove()"></button>
                </div>
            </div>`;

        document.body.insertAdjacentHTML('beforeend', alertHTML);

        setTimeout(() => {
            const alert = document.querySelector('.custom-alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100px)';
                alert.style.transition = 'all 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        }, 4000);
    };

    // Scroll to Top
    initializeScrollToTop();

    function initializeScrollToTop() {
        const btn = document.createElement('button');
        btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        btn.className = 'scroll-to-top';
        document.body.appendChild(btn);

        window.addEventListener('scroll', () => {
            btn.classList.toggle('show', window.pageYOffset > 300);
        });

        btn.addEventListener('click', () => {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }

    // Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('hero-section')) {
                    animateCounters();
                }
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, {threshold: 0.1});

    document.querySelectorAll('section, .service-card, .portfolio-card').forEach(el => {
        observer.observe(el);
    });

    // Portfolio Animations
    document.querySelectorAll('.portfolio-card').forEach((card, i) => {
        card.style.animationDelay = `${i * 0.1}s`;
        card.classList.add('new-project');
        card.addEventListener('click', function (e) {
            if (!e.target.closest('a') && !e.target.closest('button')) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => this.style.transform = '', 150);
            }
        });
    });

    // === فرم تماس ===
    const contactForm = document.querySelector('.contact-form-card');
    if (contactForm) {
        const submitBtn = document.getElementById('submitBtn');
        const submitText = document.getElementById('submitText');
        const loadingSpinner = document.getElementById('loadingSpinner');

        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            document.querySelectorAll('.form-error').forEach(el => {
                el.textContent = '';
                el.style.display = 'none';
            });

            const formData = new FormData(this);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

            submitBtn.disabled = true;
            submitText.textContent = 'در حال ارسال...';
            loadingSpinner.style.display = 'inline-block';

            fetch("{% url 'contact' %}", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then(r => r.ok ? r.json() : Promise.reject())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        this.reset();
                    } else {
                        Object.keys(data.errors).forEach(field => {
                            const el = document.getElementById(field + 'Error');
                            if (el) {
                                el.textContent = Array.isArray(data.errors[field]) ? data.errors[field][0] : data.errors[field];
                                el.style.display = 'block';
                            }
                        });
                    }
                })
                .catch(() => showNotification('خطا در ارتباط با سرور.', 'error'))
                .finally(() => {
                    submitBtn.disabled = false;
                    submitText.textContent = 'ارسال پیام';
                    loadingSpinner.style.display = 'none';
                });
        });
    }
});

// Global Error Handling
window.addEventListener('error', e => {
    console.error('Global JS Error:', e.error);
    showNotification('خطایی در صفحه رخ داد.', 'error');
});