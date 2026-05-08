const menuButton = document.querySelector('[data-menu-button]');
const menu = document.querySelector('[data-menu]');
if (menuButton && menu) {
  menuButton.addEventListener('click', () => menu.classList.toggle('is-open'));
}
setTimeout(() => {
  document.querySelectorAll('.message').forEach((item) => item.remove());
}, 5000);
