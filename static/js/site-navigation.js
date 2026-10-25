const toggle = document.querySelector("[data-menu-toggle]");
const panel = document.querySelector("[data-mobile-navigation]");

if (toggle && panel) {
  const desktop = window.matchMedia("(min-width: 64.0625rem)");
  const links = panel.querySelectorAll("a");

  const closeMenu = ({ returnFocus = false } = {}) => {
    panel.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Abrir menú");
    if (returnFocus) toggle.focus();
  };

  const syncViewport = () => {
    if (desktop.matches) {
      closeMenu();
      toggle.hidden = true;
    } else {
      toggle.hidden = false;
      closeMenu();
    }
  };

  toggle.addEventListener("click", () => {
    const opening = panel.hidden;
    panel.hidden = !opening;
    toggle.setAttribute("aria-expanded", String(opening));
    toggle.setAttribute("aria-label", opening ? "Cerrar menú" : "Abrir menú");
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) {
      event.preventDefault();
      closeMenu({ returnFocus: true });
    }
  });

  links.forEach((link) => link.addEventListener("click", () => closeMenu()));
  desktop.addEventListener("change", syncViewport);
  syncViewport();
}
