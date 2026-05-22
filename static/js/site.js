const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const scrollTop = document.querySelector('.scroll-top');

if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', String(isOpen));
    });
}

if (scrollTop) {
    window.addEventListener('scroll', () => {
        scrollTop.classList.toggle('is-visible', window.scrollY > 480);
    });
    scrollTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
