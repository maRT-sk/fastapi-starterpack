// Initialize Alpine.js components when the Alpine framework is ready.

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