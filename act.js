// 滚动动画
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.section').forEach((section) => {
    observer.observe(section);
});

// 导航栏交互
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.nav');
    if(window.scrollY > 50) {
        nav.style.background = 'rgba(10, 10, 10, 0.95)';
    } else {
        nav.style.background = 'rgba(10, 10, 10, 0.85)';
    }
});