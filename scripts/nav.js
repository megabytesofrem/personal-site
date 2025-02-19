document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelector(".menu-icon");
    const siteNav = document.querySelector(".site-nav");

    // Toggle the nav's inline display style when the hamburger icon is clicked.
    menuIcon.addEventListener('click', function () {
        siteNav.classList.toggle('show');
    });

    document.addEventListener('click', function (event) {
        if (!siteNav.contains(event.target) && !menuIcon.contains(event.target)) {
            siteNav.classList.remove('show');
        }
    });
});