/* =========================================================
   BUSINESS MANAGER
   Dashboard JavaScript
========================================================= */


/* =========================================================
   MOBILE SIDEBAR
========================================================= */

const mobileMenu = document.getElementById("mobileMenu");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebarOverlay");


if (mobileMenu && sidebar) {

    mobileMenu.addEventListener("click", function () {

        sidebar.classList.toggle("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle("show");
        }

    });

}


/* Close sidebar */

if (sidebarOverlay) {

    sidebarOverlay.addEventListener("click", function () {

        sidebar.classList.remove("open");

        sidebarOverlay.classList.remove("show");

    });

}


/* Close sidebar after clicking a link */

document.querySelectorAll(".side-link").forEach(function (link) {

    link.addEventListener("click", function () {

        if (window.innerWidth <= 950) {

            sidebar.classList.remove("open");

            if (sidebarOverlay) {
                sidebarOverlay.classList.remove("show");
            }

        }

    });

});



/* =========================================================
   SCROLL REVEAL
========================================================= */

const revealElements =
    document.querySelectorAll(".reveal");


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
            threshold: 0.08
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
   SMALL 3D EFFECT
========================================================= */

const moduleCards =
    document.querySelectorAll(".module-card");


moduleCards.forEach(function (card) {

    card.addEventListener("mousemove", function (event) {

        if (window.innerWidth <= 950) {
            return;
        }

        const rect =
            card.getBoundingClientRect();


        const x =
            event.clientX - rect.left;


        const y =
            event.clientY - rect.top;


        const centerX =
            rect.width / 2;


        const centerY =
            rect.height / 2;


        const rotateX =
            ((y - centerY) / centerY) * -1.2;


        const rotateY =
            ((x - centerX) / centerX) * 1.2;


        card.style.transform =
            `perspective(700px)
             rotateX(${rotateX}deg)
             rotateY(${rotateY}deg)
             translateY(-3px)`;

    });


    card.addEventListener("mouseleave", function () {

        card.style.transform = "";

    });

});



/* =========================================================
   CURRENT YEAR
========================================================= */

const yearElement =
    document.getElementById("currentYear");


if (yearElement) {

    yearElement.textContent =
        new Date().getFullYear();

}



/* =========================================================
   NOTIFICATION BUTTON
========================================================= */

const notificationBtn =
    document.getElementById("notificationBtn");


if (notificationBtn) {

    notificationBtn.addEventListener("click", function () {

        notificationBtn.classList.toggle("clicked");

    });

}



/* =========================================================
   CLOSE MOBILE MENU ON RESIZE
========================================================= */

window.addEventListener("resize", function () {

    if (window.innerWidth > 950) {

        if (sidebar) {
            sidebar.classList.remove("open");
        }

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("show");
        }

    }

});