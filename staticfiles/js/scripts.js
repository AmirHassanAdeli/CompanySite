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

// === Add Project Modal Handler ===
function initializeProjectModal() {
    const addProjectForm = document.getElementById('addProjectForm');
    const addProjectModal = document.getElementById('addProjectModal');

    if (addProjectForm) {
        addProjectForm.addEventListener('submit', function (e) {
            e.preventDefault();
            submitProjectForm();
        });
    }

    // ریست فرم وقتی مدال بسته می‌شود
    if (addProjectModal) {
        addProjectModal.addEventListener('hidden.bs.modal', function () {
            resetProjectForm();
        });
    }
}

// === Submit Project Form ===
function submitProjectForm() {
    const form = document.getElementById('addProjectForm');
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    // نمایش حالت لودینگ
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال افزودن...';
    submitBtn.disabled = true;

    // ارسال درخواست AJAX
    fetch('/projects/ajax-add/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken(),
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // موفقیت آمیز
                showNotification(data.message, 'success');

                // اضافه کردن پروژه به لیست
                addProjectToDOM(data.project);

                // بستن مدال
                const modal = bootstrap.Modal.getInstance(document.getElementById('addProjectModal'));
                if (modal) {
                    modal.hide();
                }

                // ریست فرم
                resetProjectForm();

            } else {
                // نمایش خطاها
                if (data.errors) {
                    displayFormErrors(data.errors);
                } else {
                    showNotification(data.error || 'خطایی رخ داده است', 'error');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('خطا در ارتباط با سرور', 'error');
        })
        .finally(() => {
            // بازگشت دکمه به حالت عادی
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
}

// === Add Project to DOM ===
function addProjectToDOM(project) {
    const portfolioContainer = document.getElementById('portfolioContainer');

    if (portfolioContainer) {
        const projectHTML = `
            <div class="col-lg-4 col-md-6 mb-4" data-project-id="${project.id}">
                <div class="portfolio-card new-project">
                    <div class="portfolio-image" style="background: ${project.color};">
                        <i class="${project.icon}"></i>
                    </div>
                    <div class="portfolio-content">
                        <h3 class="portfolio-title">${project.title}</h3>
                        <p class="portfolio-description">${project.description}</p>
                        <div class="tech-tags">
                            ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                        </div>
                        <div class="project-actions mt-3">
                            <span class="badge bg-warning">در انتظار تایید</span>
                            <button class="btn-outline-custom btn-sm view-details-btn" data-project-id="${project.id}">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        portfolioContainer.insertAdjacentHTML('afterbegin', projectHTML);

        // انیمیشن برای پروژه جدید
        animateNewProject(portfolioContainer.firstElementChild);

        // اضافه کردن event listener برای دکمه جزئیات
        const viewDetailsBtn = portfolioContainer.querySelector(`[data-project-id="${project.id}"] .view-details-btn`);
        if (viewDetailsBtn) {
            viewDetailsBtn.addEventListener('click', function() {
                viewProjectDetails(project.id);
            });
        }
    }
}

// === Display Form Errors ===
function displayFormErrors(errors) {
    // پاک کردن خطاهای قبلی
    clearFormErrors();

    // نمایش خطاهای جدید
    for (const field in errors) {
        const input = document.getElementById(`project${field.charAt(0).toUpperCase() + field.slice(1)}`);
        if (input) {
            input.style.borderColor = '#f44336';
            const errorElement = document.createElement('div');
            errorElement.className = 'form-error show';
            errorElement.textContent = errors[field];
            input.parentNode.appendChild(errorElement);
        }
    }
}

// === Clear Form Errors ===
function clearFormErrors() {
    const errorElements = document.querySelectorAll('.form-error');
    errorElements.forEach(element => element.remove());

    const inputs = document.querySelectorAll('#addProjectForm .form-control');
    inputs.forEach(input => {
        input.style.borderColor = 'rgba(0, 212, 255, 0.3)';
    });
}

// === Reset Project Form ===
function resetProjectForm() {
    const form = document.getElementById('addProjectForm');
    if (form) {
        form.reset();
        clearFormErrors();
    }
}

// === Get CSRF Token ===
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
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

// === Animate New Project ===
function animateNewProject(element) {
    if (!element) return;

    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'all 0.5s ease';

    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

// === View Project Details ===
function viewProjectDetails(projectId) {
    // این تابع می‌تواند برای نمایش جزئیات پروژه استفاده شود
    console.log('Viewing project details:', projectId);
    // می‌توانید اینجا modal جدیدی برای نمایش جزئیات باز کنید
    // یا کاربر را به صفحه جزئیات پروژه هدایت کنید
    window.location.href = `/projects/${projectId}/`;
}

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

// === Form Validation ===
function initializeFormValidation() {
    const formInputs = document.querySelectorAll('#addProjectForm input, #addProjectForm textarea, #addProjectForm select');
    formInputs.forEach(input => {
        input.addEventListener('input', function () {
            if (this.value.trim()) {
                this.style.borderColor = 'rgba(0, 212, 255, 0.3)';
                const errorElement = this.nextElementSibling;
                if (errorElement && errorElement.classList.contains('form-error')) {
                    errorElement.remove();
                }
            }
        });

        // اضافه کردن اعتبارسنجی بلادرنگ
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#f44336';
            }
        });
    });
}

// === Contact Form Handler ===
function initializeContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('#submitBtn');
            const submitText = this.querySelector('#submitText');
            const loadingSpinner = this.querySelector('#loadingSpinner');

            if (submitBtn && submitText && loadingSpinner) {
                submitText.textContent = 'در حال ارسال...';
                loadingSpinner.style.display = 'inline-block';
                submitBtn.disabled = true;
            }
        });
    }
}

// === Initialize when page loads ===
document.addEventListener('DOMContentLoaded', function () {
    console.log('Portfolio website loaded successfully!');

    // Initialize all components
    initializeProjectModal();
    initializeScrollToTop();
    initializePortfolioAnimations();
    initializeFormValidation();
    initializeContactForm();

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
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('خطایی در اجرای صفحه رخ داده است', 'error');
});