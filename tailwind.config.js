/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["/static/src/css/output.css",
  "./templates/index.html", "./templates/login.html", "./templates/planetarium.html", "./templates/base.html", "./templates/register.html", "./templates/telescope_time.html", "./templates/update_password.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}