// Get the login form
const loginForm = document.querySelector('#login-form');

// Add an event listener to the form submit button
loginForm.addEventListener('submit', (event) => {
  // Prevent the form from submitting
  event.preventDefault();

  // Get the user inputs from the form
  const username = loginForm.elements['username'].value;
  const password = loginForm.elements['password'].value;

  // Send a POST request to the server to validate the user
  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => {
    // Check the response status
    if (response.status === 200) {
      // Redirect the user to the chat page
      window.location.replace('/chat');
    } else {
      // Display an error message
      const errorMessage = document.querySelector('#error-message');
      errorMessage.textContent = 'Invalid username or password';
      errorMessage.classList.remove('d-none');
    }
  })
  .catch(error => {
    console.error(error);
  });
});
