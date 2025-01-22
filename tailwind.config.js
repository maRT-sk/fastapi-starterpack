// const colors = require('tailwindcss/colors'); // Import Tailwind's color palette

module.exports = {
    darkMode: 'class',
    content: [
        './app/templates/**/*.html',
        './app/static/js/**/*.js',
        './app/**/*.py',
    ],
    theme: {
        extend: {
            // colors: {
            //     custom: {
            //         bg: {
            //             light: colors.slate[50],
            //             dark: colors.slate[800],
            //         },
            //         text: {
            //             light: colors.slate[800],
            //             dark: colors.slate[50],
            //         },
            //     },
            // },
        },
    },
    plugins: [],
};
