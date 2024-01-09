document.addEventListener("DOMContentLoaded", function() {
    var scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
        sessionStorage.removeItem('scrollPosition');
    }

    window.addEventListener('scroll', function() {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    });
});