"use strict";
(() => {
  const key = "cabra-media-consent-v1";
  const banner = document.querySelector("#privacy-banner");
  const dialog = document.querySelector("#privacy-dialog");
  let choice = null;
  try {
    const saved = localStorage.getItem(key);
    if (["allowed", "denied"].includes(saved)) choice = saved;
  } catch {}
  function updateStatus() {
    document.querySelector("#privacy-status").textContent =
      choice === "allowed"
        ? "Instagram está autorizado. El reel se carga solo cuando lo solicitas."
        : "Instagram está desactivado. Solo usamos recursos necesarios.";
  }
  function open() {
    updateStatus();
    if (!dialog.open) {
      dialog.showModal();
      document.body.classList.add("dialog-open");
    }
  }
  function choose(value) {
    choice = value;
    try {
      localStorage.setItem(key, value);
    } catch {}
    banner.hidden = true;
    if (value === "denied") {
      const frame = document.querySelector("#reel-frame");
      frame.replaceChildren();
      frame.hidden = true;
      document.querySelector(".reel-help").hidden = true;
      const reel = document.querySelector(".reel-load");
      reel.disabled = false;
      reel.textContent = "Ver el reel";
    }
    updateStatus();
    dialog.close();
  }
  document
    .querySelectorAll("[data-open-privacy]")
    .forEach((button) => button.addEventListener("click", open));
  document
    .querySelectorAll("[data-privacy-choice]")
    .forEach((button) =>
      button.addEventListener("click", () =>
        choose(button.dataset.privacyChoice),
      ),
    );
  document
    .querySelector("#privacy-close")
    .addEventListener("click", () => dialog.close());
  window.cabraPrivacy = Object.freeze({
    instagramAllowed: () => choice === "allowed",
    open,
  });
  banner.hidden = choice !== null;
  if (location.hash === "#preferencias") open();
})();
