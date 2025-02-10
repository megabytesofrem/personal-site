document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelector(".menu-icon");
    const siteNav = document.querySelector(".site-nav");

    // Toggle the nav's inline display style when the hamburger icon is clicked.
    menuIcon.addEventListener("click", function () {
        if (siteNav.style.display === "flex") {
            siteNav.style.display = "none";
        } else {
            siteNav.style.display = "flex";
        }
    });

    window.addEventListener("resize", function () {
        // When viewport is wider than 600px, force the nav to display as flex.
        if (window.innerWidth > 1000) {
            siteNav.style.display = "flex";
        } else {
            // On mobile, hide it by default.
            siteNav.style.display = "none";
        }
    });
});