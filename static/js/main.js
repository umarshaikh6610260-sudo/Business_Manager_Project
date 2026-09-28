/* =========================================================
   BUSINESSMANAGER
   MAIN WEBSITE JAVASCRIPT
========================================================= */


/* =========================================================
   MOBILE NAVIGATION
========================================================= */

const menuToggle = document.getElementById("menuToggle");
const mainNav = document.getElementById("mainNav");

if (menuToggle && mainNav) {

    menuToggle.addEventListener("click", function () {

        mainNav.classList.toggle("show");

        if (mainNav.classList.contains("show")) {
            menuToggle.innerHTML = "✕";
        } else {
            menuToggle.innerHTML = "☰";
        }

    });


    const navLinks = mainNav.querySelectorAll("a");

    navLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            mainNav.classList.remove("show");

            menuToggle.innerHTML = "☰";

        });

    });

}


/* =========================================================
   SCROLL REVEAL
========================================================= */

const revealElements = document.querySelectorAll(".reveal");


if ("IntersectionObserver" in window) {

    const revealObserver = new IntersectionObserver(
        function (entries) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("active");

                    revealObserver.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.12
        }
    );


    revealElements.forEach(function (element) {

        revealObserver.observe(element);

    });

} else {

    revealElements.forEach(function (element) {

        element.classList.add("active");

    });

}


/* =========================================================
   SMALL 3D CARD EFFECT
========================================================= */

const cards = document.querySelectorAll(
    ".product-card, .feature-card, .module-card"
);


cards.forEach(function (card) {

    card.addEventListener("mousemove", function (event) {

        const rect = card.getBoundingClientRect();

        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX =
            ((y - centerY) / centerY) * -2;

        const rotateY =
            ((x - centerX) / centerX) * 2;

        card.style.transform =
            `perspective(900px)
             rotateX(${rotateX}deg)
             rotateY(${rotateY}deg)
             translateY(-7px)`;

    });


    card.addEventListener("mouseleave", function () {

        card.style.transform = "";

    });

});


/* =========================================================
   CURRENT YEAR
========================================================= */

const yearElement = document.getElementById("currentYear");

if (yearElement) {

    yearElement.textContent =
        new Date().getFullYear();

}