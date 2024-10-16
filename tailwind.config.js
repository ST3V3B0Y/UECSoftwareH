/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/src/**/*.js"
  ],
  theme: {
    extend: {
      aspectRatio: {
        '3/2': '3 / 2',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
/**npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --watch */