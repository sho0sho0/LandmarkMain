document.addEventListener("DOMContentLoaded", function () {

    const successPopup = document.getElementById("successPopup");
    const errorPopup = document.getElementById("errorPopup");


    function showPopup(popup) {
        if (popup) {
            popup.style.opacity = "0";
            popup.style.display = "block";

            setTimeout(() => {
                popup.style.transition = "opacity 0.5s";
                popup.style.opacity = "1";

              
                setTimeout(() => {
                    popup.style.opacity = "0";
                    setTimeout(() => {
                        popup.style.display = "none";
                    }, 500); 
                }, 5000);
            }, 100);
        }
    }


    showPopup(successPopup);

    showPopup(errorPopup);
});
