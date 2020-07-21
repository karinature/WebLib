// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
window.onscroll = function () {
    scrollFunction()
};

function scrollFunction() {
    let navbar = document.getElementsByClassName("navbar")[0];
    let logo = document.getElementById("logo");
    let title = document.getElementsByClassName("navbar-title")[0];

    if (document.body.scrollTop > 120 || document.documentElement.scrollTop > 120) {
        navbar.style.padding = "5px 10px 5px 10px";

        // logo.style.padding = "5px 10px 5px 10px";
        // logo.style.margin = "5px 10px 5px 10px";
        logo.style.height = "5em";
        logo.style.width = "5em";

        title.style.padding = "5px 10px 5px 10px";
        document.getElementById("title").style.fontSize = "1em";
        // document.getElementById("subtitle").style.fontSize = "1em";

    } else {
        navbar.style.padding = "30px 10px 30px 10px";

        // logo.style.padding = "30px 10px 30px 10px";
        // logo.style.margin = "30px 10px 30px 10px";
        logo.style.height = "10em";
        logo.style.width = "10em";

        title.style.padding = "30px 10px 30px 10px";
        document.getElementById("title").style.fontSize = "2em";
        // document.getElementById("subtitle").style.fontSize = "1em";
    }
}