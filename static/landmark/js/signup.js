document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const successPopup = document.getElementById("successPopup");
    const errorPopup = document.getElementById("errorPopup");

    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission


        const formData = {
            username: document.getElementById("username").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
            rePassword: document.getElementById("re-password").value,
        };

        try {
            // Send data to backend
            const response = await fetch("YOUR_BACKEND_URL/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
               
                successPopup.style.display = "block";
                setTimeout(() => {
                    successPopup.style.display = "none";
                }, 3000); 
            } else {
               
                errorPopup.style.display = "block";
                setTimeout(() => {
                    errorPopup.style.display = "none";
                }, 3000);
            }
        } catch (error) {
            
            errorPopup.style.display = "block";
            setTimeout(() => {
                errorPopup.style.display = "none";
            }, 3000);
            console.error("Error:", error);
        }
    });
});