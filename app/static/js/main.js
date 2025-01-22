// This script initializes an Alpine.js component called `themeManager` to manage themes.
// - It checks the user's theme preference stored in `localStorage` or defaults to the system's color scheme preference.
// - When the dark/light mode state changes, it updates the `localStorage` to persist the user's preference.
document.addEventListener('alpine:init', () => {
    Alpine.data('themeManager', () => ({
        darkMode: localStorage.getItem('theme')
            ? localStorage.getItem('theme') === 'dark'
            : window.matchMedia('(prefers-color-scheme: dark)').matches,
        init() {
            this.$watch('darkMode', (value) => {
                localStorage.setItem('theme', value ? 'dark' : 'light');
            });
        },
    }));
});