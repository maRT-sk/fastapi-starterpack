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


// This section handles the progress bar animation for HTMX requests.
document.addEventListener('DOMContentLoaded', () => {
    // Select the loading bar element for manipulation and progress variable
    const loadingBar = document.getElementById('loading');
    let progress = 0;

    // Initializes the progress bar to 0% and starts the animation for a new HTMX request.
    function initializeProgressBar() {
        progress = 0;
        loadingBar.style.width = '0%';
        animateProgressBar();
    }

    // Animates the progress bar with random incremental progress until it reaches 80%.
    function animateProgressBar() {
        if (progress < 80) {
            progress = Math.min(progress + Math.random() * 40, 80);
            loadingBar.style.width = `${progress}%`;
            setTimeout(animateProgressBar, 250);
        }
    }

    // Completes the progress bar by setting it to 100% when the HTMX request is done.
    function finalizeProgressBar() {
        loadingBar.style.width = `100%`;
    }

    // Attach event listeners for HTMX lifecycle events.
    document.body.addEventListener('htmx:beforeRequest', initializeProgressBar);  // Before request starts.
    document.body.addEventListener('htmx:afterRequest', finalizeProgressBar); // After request completes.
});
