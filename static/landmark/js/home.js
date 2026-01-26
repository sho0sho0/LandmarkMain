// Comment Card Scrolling (Right and Left Arrows)
const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');
const commentContainer = document.querySelector('.comments-container');

let scrollPosition = 0;
const commentWidth = document.querySelector('.comment-card').offsetWidth;
const visibleComments = 3; // Show 3 comments initially

// Event listener for scrolling to the right
rightArrow.addEventListener('click', () => {
    if (scrollPosition < commentContainer.scrollWidth - commentContainer.offsetWidth) {
        scrollPosition += commentWidth * visibleComments;
        commentContainer.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    }
});

// Event listener for scrolling to the left
leftArrow.addEventListener('click', () => {
    if (scrollPosition > 0) {
        scrollPosition -= commentWidth * visibleComments;
        commentContainer.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    }
});



const TleftArrow = document.querySelector('.left-arrow');
const TrightArrow = document.querySelector('.right-arrow');
const trainingImageContainer = document.querySelector('.training-images-container');

let TscrollPosition = 0;
const imageWidth = document.querySelector('.training-image-card').offsetWidth;
const visibleImages = 3; // Show 3 images at once

// Event listener for scrolling to the right
TrightArrow.addEventListener('click', () => {
    if (TscrollPosition < trainingImageContainer.scrollWidth - trainingImageContainer.offsetWidth) {
        TscrollPosition += imageWidth * visibleImages;
        trainingImageContainer.scrollTo({
            left: TscrollPosition,
            behavior: 'smooth'
        });
    }
});

// Event listener for scrolling to the left
TleftArrow.addEventListener('click', () => {
    if (scrollPosition > 0) {
        scrollPosition -= imageWidth * visibleImages;
        trainingImageContainer.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    }
});


// function subscribe() {
//     const email = document.getElementById('email').value;

//     if (email) {
//         // Send the email to the backend
//         fetch('/api/subscribe/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken() // Add CSRF token for secure requests
//             },
//             body: JSON.stringify({ email })
//         })
//         .then(response => {
//             if (response.ok) {
//                 showSuccessPopup();
//             } else {
//                 showErrorPopup();
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showErrorPopup();
//         });
//     } else {
//         showErrorPopup();
//     }
// }

// // CSRF Token helper function for Django
// function getCSRFToken() {
//     const cookieValue = document.cookie
//         .split('; ')
//         .find(row => row.startsWith('csrftoken='))
//         ?.split('=')[1];
//     return cookieValue;
// }

// // Function to show the success pop-up
// function showSuccessPopup() {
//     const successPopup = document.getElementById('successPopup');
//     successPopup.style.display = 'block';
    
//     // Hide after 3 seconds
//     setTimeout(() => {
//         successPopup.style.display = 'none';
//     }, 3000);
// }

// // Function to show the error pop-up
// function showErrorPopup() {
//     const errorPopup = document.getElementById('errorPopup');
//     errorPopup.style.display = 'block';
    
//     // Hide after 3 seconds
//    setTimeout(() => {
//         errorPopup.style.display = 'none';
//     }, 3000);
// }
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// function subscribe() {
//     const emailInput = document.getElementById('email');
//     const email = emailInput.value;

//     // Email validation regex pattern
//     const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

//     if (email && emailPattern.test(email)) {
//         // Send the email to the backend
//         fetch('api/subscribe/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCSRFToken() // Add CSRF token for secure requests
//             },
//             body: JSON.stringify({ email })
//         })
//         .then(response => {
//             if (response.ok) {
//                 // If the subscription was successful
//                 showSuccessPopup();
//                 emailInput.value = "";  // Clear the input field after a successful subscription
//             } else {
//                 // If there was an error with the subscription
//                 response.json().then(data => {
//                     // If the error is that the email is already subscribed
//                     if (data.message === 'Already subscribed') {
//                         showAlreadySubscribedPopup();
//                     } else {
//                         showErrorPopup(data.message || "An error occurred.");
//                     }
//                 });
//             }
//         })
//         .catch(error => {
//             // Catch network errors or other issues
//             console.error('Error:', error);
//             showErrorPopup("Network error or unexpected issue.");
//         });
//     } else {
//         // If the email doesn't match the pattern, show "Invalid Email" error
//         showErrorPopup("Invalid email format. Please enter a valid email address.");
//     }
// }

// // Function to show the 'Already Subscribed' error message
// function showAlreadySubscribedPopup() {
//     const errorPopup = document.getElementById('errorPopup');
//     const errorMessage = errorPopup.querySelector('p');
//     const errorTitle = errorPopup.querySelector('h3');

//     // Update the message to reflect the "Already Subscribed" state
//     errorTitle.textContent = "You're Already Subscribed!";
//     errorMessage.textContent = "You have already subscribed with this email address.";

//     errorPopup.style.display = 'block';

    
//     setTimeout(() => {
//         errorPopup.style.display = 'none';
//     }, 3000);
// }


function showErrorPopup(message) {
    const errorPopup = document.getElementById('errorPopup');
    const errorMessage = errorPopup.querySelector('p');
    const errorTitle = errorPopup.querySelector('h3');

    errorTitle.textContent = "Subscription Failed";
    errorMessage.textContent = message;

    errorPopup.style.display = 'block';

    setTimeout(() => {
        errorPopup.style.display = 'none';
    }, 3000);
}

function showSuccessPopup() {
    const successPopup = document.getElementById('successPopup');
    successPopup.style.display = 'block';
    
    setTimeout(() => {
        successPopup.style.display = 'none';
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
    // Email validation regex
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Form submit handler
    const form = document.querySelector(".contact-form");
    form.addEventListener("submit", function (event) {
        const emailInput = document.getElementById("email");
        const nameInput = document.getElementById("name");
        const phoneInput = document.getElementById("phone");
        const programInput = document.getElementById("program");
        const questionInput = document.getElementById("question");

        const email = emailInput.value;
        const name = nameInput.value;
        const phone = phoneInput.value;
        const program = programInput.value;
        const question = questionInput.value;

        // Reset any previous popups
        const successPopup = document.getElementById("successPopup");
        const errorPopup = document.getElementById("errorPopup");

        successPopup.style.display = 'none';
        errorPopup.style.display = 'none';

        // Check if all required fields are filled
        if (!email || !name || !phone || !question) {
            event.preventDefault();
            showErrorPopup("Please fill in all required fields.");
            return;
        }

        // Validate email format
        if (!emailRegex.test(email)) {
            event.preventDefault();
            showErrorPopup("Please enter a valid email address.");
            return;
        }

        // Optionally validate phone (check for valid phone format, e.g., minimum 10 digits)
        if (!phone || phone.length < 10) {
            event.preventDefault();
            showErrorPopup("Please enter a valid phone number.");
            return;
        }

        // If everything is valid, show success
        showSuccessPopup();
    });
});
