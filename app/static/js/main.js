// This script initializes an Alpine.js component called `themeManager` to manage themes.
// - It checks the user's theme preference stored in `localStorage` or defaults to the system's color scheme preference.
// - When the dark/light mode state changes, it updates the `localStorage` to persist the user's preference.
document.addEventListener('alpine:init', () => {
    Alpine.data('themeManager', () => ({
        // Determine the initial theme
        darkMode: localStorage.getItem('theme') === 'dark'
            || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches),

        // Save the theme preference whenever it changes
        init() {
            this.$watch('darkMode', (isDarkMode) => {
                localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
            });
        },
    }));
});

// TODO: Improve animation for fast-loading websites, especially when the loading completes very quickly.
// This section handles the progress bar animation for HTMX requests.
document.addEventListener('DOMContentLoaded', () => {
    // Select the loading bar element for manipulation and progress variable
    const loadingBar = document.getElementById('loading');
    let progress = 0;
    let progressInterval;

    // Initializes the progress bar to 0% and starts the animation for a new HTMX request.
    function initializeProgressBar() {
        progress = 0;
        loadingBar.style.width = `${progress}%`;
        clearInterval(progressInterval)
        progressInterval = setInterval(animateProgressBar, 150);
    }

    // Animates the progress bar with random incremental progress until it reaches 80%.
    function animateProgressBar() {
        if (progress < 80) {
            // Increment progress by a random amount between 2 and 10
            const randomIncrement = Math.floor(Math.random() * 9) + 2;
            progress = Math.min(progress + randomIncrement, 80);
            loadingBar.style.width = `${progress}%`;
        }
    }

    // Completes the progress bar by setting it to 100% when the HTMX request is done.
    function completeProgressBar() {
        clearInterval(progressInterval); // Stop the interval when the request completes
        progress = 100
        loadingBar.style.width = '100%';

    }

    // Handles HTMX error where the user cannot reach our server or went offline
    function handleSendError(event) {
        console.error('Network error occurred during HTMX request:', event.detail);
        window.location.reload();  // Force reload
    }

    // Attach event listeners for HTMX lifecycle events.
    document.body.addEventListener('htmx:beforeRequest', initializeProgressBar);  // Before request starts.
    document.body.addEventListener('htmx:load', completeProgressBar); // After request completes.
    document.body.addEventListener('htmx:sendError', handleSendError);

});
