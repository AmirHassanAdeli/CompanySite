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

// === Add Project Functionality ===
function addProject() {
    const title = document.getElementById('projectTitle').value.trim();
    const description = document.getElementById('projectDescription').value.trim();
    const tech = document.getElementById('projectTech').value.trim();
    const icon = document.getElementById('projectIcon').value.trim() || 'fas fa-cog';
    const color = document.getElementById('projectColor').value.trim() || 'linear-gradient(135deg, #00d4ff 0%, #6a5acd 50%, #c0c0c0 100%)';

    if (!title || !description) {
        showNotification('لطفاً عنوان و توضیحات پروژه را وارد کنید.', 'error');
        return;
    }

    const techTags = tech.split(',').map(t => t.trim()).filter(t => t);

    if (techTags.length === 0) {
        techTags.push('AI', 'Machine Learning');
    }

    const projectHTML = `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="portfolio-card">
                <div class="portfolio-image" style="background: ${color};">
                    <i class="${icon}"></i>
                </div>
                <div class="portfolio-content">
                    <h3 class="portfolio-title">${title}</h3>
                    <p class="portfolio-description">${description}</p>
                    <div class="tech-tags">
                        ${techTags.map(tag => `<span class="tech-tag">${tag}</span>`).join('')}
                    </div>
                    <a href="#" class="btn-primary-custom">مشاهده جزئیات</a>
                </div>
            </div>
        </div>
    `;

    const portfolioContainer = document.getElementById('portfolioContainer');
    portfolioContainer.insertAdjacentHTML('beforeend', projectHTML);

    // Animation for new project
    const newProject = portfolioContainer.lastElementChild;
    newProject.style.opacity = '0';
    newProject.style.transform = 'translateY(20px)';

    setTimeout(() => {
        newProject.style.transition = 'all 0.5s ease';
        newProject.style.opacity = '1';
        newProject.style.transform = 'translateY(0)';
    }, 100);

    // Clear form and close modal
    document.getElementById('addProjectForm').reset();
    const modal = bootstrap.Modal.getInstance(document.getElementById('addProjectModal'));
    modal.hide();

    showNotification('پروژه با موفقیت اضافه شد!', 'success');
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
             style="top: 100px; right: 20px; z-index: 9999; background: ${bgColor}; border: 1px solid ${borderColor}; color: #ffffff; border-radius: 12px; backdrop-filter: blur(10px);" 
             role="alert">
            <div class="d-flex align-items-center">
                <i class="${icon} me-2" style="font-size: 1.2rem;"></i>
                <span>${message}</span>
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
document.addEventListener('DOMContentLoaded', function () {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top';
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    });

    scrollBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// === Intersection Observer for Animations ===
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.classList.contains('hero-section')) {
                animateCounters();
            }
            entry.target.classList.add('animate-in');
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

// Observe sections for animation
document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => observer.observe(section));

    const cards = document.querySelectorAll('.service-card, .portfolio-card');
    cards.forEach(card => observer.observe(card));

    // Initialize form submission
    const addProjectForm = document.getElementById('addProjectForm');
    if (addProjectForm) {
        addProjectForm.addEventListener('submit', function (e) {
            e.preventDefault();
            addProject();
        });
    }
});

// === Form Validation ===
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#f44336';
            isValid = false;
        } else {
            input.style.borderColor = 'rgba(0, 212, 255, 0.2)';
        }
    });

    return isValid;
}

// === Initialize when page loads ===
document.addEventListener('DOMContentLoaded', function () {
    console.log('Portfolio website loaded successfully!');
});