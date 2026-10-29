const products = [
  {
    name: "Tablas de plato",
    category: "madera",
    tag: "MESA Y CORTE",
    image: "tabla-corte.jpg",
    description: "La presentación empieza en la madera.",
    features: [
      "Madera natural",
      "Grabado láser personalizado",
      "Diferentes medidas disponibles",
    ],
  },
  {
    name: "Grillbox",
    category: "parrilla",
    tag: "PARRILLA",
    image: "grillbox-beastown.jpg",
    description: "Toda una experiencia al abrir la mesa.",
    features: [
      "Madera natural y acabado artesanal",
      "Personalización con tu marca",
      "Diferentes configuraciones disponibles",
    ],
    asset: "assets/mayoreo/grillbox-beastown-pedido.webp",
  },
  {
    name: "Delantales y mandiles",
    category: "piel",
    tag: "EL CARÁCTER SE LLEVA",
    image: "mandiles-calle.jpg",
    description: "Para quienes ponen las manos al fuego.",
    features: [
      "Opciones en piel y gabardina",
      "Personalización disponible",
      "Para chefs, parrilleros y equipos",
    ],
    asset: "assets/mayoreo/mandiles-personalizados.webp",
  },
  {
    name: "Tablas para pizza",
    category: "madera",
    tag: "PARA COMPARTIR",
    image: "pizza-redonda.jpg",
    description: "De la primera rebanada a la última.",
    features: [
      "Madera natural",
      "Para servir y cortar pizza",
      "Grabado personalizado",
    ],
  },
  {
    name: "Hierro con tabla",
    category: "parrilla",
    tag: "HIERRO Y MADERA",
    image: "hierro-set.jpg",
    description: "Una combinación con presencia.",
    features: [
      "Piezas de hierro con base de madera",
      "Para presentación y servicio",
      "Personalización disponible",
    ],
    asset: "assets/mayoreo/hierro-restaurantes.webp",
  },
  {
    name: "Tequileros",
    category: "madera",
    tag: "BARRA",
    image: "tequilero-ojo.jpg",
    description: "El brindis también merece su pieza.",
    features: [
      "Madera natural",
      "Diferentes diseños y capacidades",
      "Personalización con grabado",
    ],
    asset: "assets/mayoreo/tequileros-ojo-tigre.webp",
  },
  {
    name: "Tablas variadas",
    category: "madera",
    tag: "VETAS CON PERSONALIDAD",
    image: "endgrain-ajedrez.jpg",
    description: "Una pieza distinta para cada idea.",
    features: [
      "Variedad de diseños",
      "Opciones en maderas naturales",
      "Grabado personalizado",
    ],
    asset: "assets/mayoreo/tablas-cuadros-taller.webp",
  },
  {
    name: "Productos en piel",
    category: "piel",
    tag: "PIEL",
    image: "carpeta-roma.jpg",
    description: "Tu identidad, hasta en los detalles.",
    features: [
      "Piezas en piel para mesa y servicio",
      "Grabado láser con tu marca",
      "Opciones para restaurantes y bares",
    ],
  },
  {
    name: "Porta vasos",
    category: "madera",
    tag: "PEQUEÑOS DETALLES",
    image: "portavasos.jpg",
    description: "Una gran marca en un pequeño formato.",
    features: [
      "Madera natural",
      "Grabado láser personalizado",
      "Para regalos, eventos y servicio",
    ],
  },
  {
    name: "Platos y cubiertos",
    category: "madera",
    tag: "SERVICIO",
    image: "cubiertos-set.jpg",
    description: "La mesa completa habla de ti.",
    features: [
      "Piezas para presentación y servicio",
      "Personalización con logo",
      "Opciones para restaurantes",
    ],
    asset: "assets/mayoreo/sets-mesa-cuchillos.webp",
  },
];
function productImage(product) {
  return product.asset || "assets/img/" + product.image;
}
const wa = (message) =>
  "https://wa.me/524491060573?text=" + encodeURIComponent(message);
document.querySelectorAll("[data-wa]").forEach((link) => {
  link.href = wa(link.dataset.wa);
});
const grid = document.querySelector("#products");
if (!grid.children.length)
  products.forEach((product, index) => {
    const card = document.createElement("article");
    card.className = "product";
    card.dataset.category = product.category;
    card.innerHTML = `<div class="product-photo"><img src="${productImage(product)}" alt="${product.name} de Cabra Negra" loading="lazy" width="1050" height="1400"><span class="product-tag">${product.tag}</span><button class="product-open" data-index="${index}" aria-label="Ver ${product.name}"><span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M5 19 19 5M5 5h14v14'/></svg></span></button></div><div class="product-info"><div><h3>${product.name}</h3><p>${product.description}</p></div><span>PERSONALIZABLE</span></div>`;
    grid.append(card);
  });
document.querySelectorAll("[data-filter]").forEach((button) =>
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((item) => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    let visible = 0;
    grid.querySelectorAll(".product").forEach((card) => {
      card.hidden =
        button.dataset.filter !== "todo" &&
        card.dataset.category !== button.dataset.filter;
      if (!card.hidden) visible++;
    });
    document.querySelector("#filter-status").textContent =
      `Mostrando ${visible} líneas de productos: ${button.textContent}.`;
  }),
);
const dialog = document.querySelector("#product-dialog");
const selection = new Set();
function updateSelection() {
  const container = document.querySelector("#selected-products");
  container.replaceChildren();
  selection.forEach((name) => {
    const chip = document.createElement("span");
    chip.className = "selection-chip";
    chip.append(document.createTextNode(name));
    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "×";
    remove.setAttribute("aria-label", "Quitar " + name);
    remove.addEventListener("click", () => {
      selection.delete(name);
      if (
        name.startsWith("Tablas") &&
        ![...selection].some((piece) => piece.startsWith("Tablas"))
      ) {
        document.querySelector("#board-design").value = "Por definir";
        document.querySelector("#board-wood").value = "Quiero asesoría";
        document.querySelector("#board-size").value = "";
      }
      if (document.querySelector("#piece").value === name)
        document.querySelector("#piece").value = "Quiero asesoría";
      updateSelection();
    });
    chip.append(remove);
    container.append(chip);
  });
}
grid.addEventListener("click", (event) => {
  const button = event.target.closest("[data-index]");
  if (!button) return;
  const product = products[Number(button.dataset.index)];
  document.querySelector("#dialog-content").innerHTML =
    `<img src="${productImage(product)}" alt="${product.name} de Cabra Negra" width="1050" height="1400"><div><p class="eyebrow">${product.tag}</p><h2 id="dialog-title">${product.name}</h2><p>${product.description}</p><ul>${product.features.map((feature) => `<li>${feature}</li>`).join("")}</ul><button class="button" id="add-product">Agregar a mi proyecto <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M5 19 19 5M5 5h14v14'/></svg></span></button><a class="text-link dark" href="${wa("Hola, Cabra Negra. Me interesa cotizar: " + product.name + ".")}" target="_blank" rel="noopener noreferrer">Consultar por WhatsApp <svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M5 19 19 5M5 5h14v14'/></svg></a></div>`;
  document.querySelector("#add-product").addEventListener("click", () => {
    selection.add(product.name);
    document.querySelector("#piece").value = product.name;
    updateSelection();
    dialog.close();
    document.querySelector("#cotizar").scrollIntoView({
      behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "instant"
        : "smooth",
    });
    document.querySelector("#name").focus({ preventScroll: true });
  });
  dialog.showModal();
  document.body.classList.add("dialog-open");
});
document
  .querySelector("#product-dialog .dialog-close")
  .addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) {
    const bounds = dialog.getBoundingClientRect();
    if (
      event.clientX < bounds.left ||
      event.clientX > bounds.right ||
      event.clientY < bounds.top ||
      event.clientY > bounds.bottom
    )
      dialog.close();
  }
});
const menu = document.querySelector(".menu"),
  nav = document.querySelector("#navigation");
menu.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  menu.setAttribute("aria-expanded", String(open));
  menu.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  menu.innerHTML = open
    ? "<svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='m6 6 12 12M6 18 18 6'/></svg>"
    : "<svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M4 6h16M4 12h16M4 18h16'/></svg>";
  nav.classList.toggle("open", open);
});
nav.querySelectorAll("a").forEach((link) =>
  link.addEventListener("click", () => {
    nav.classList.remove("open");
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-label", "Abrir menú");
    menu.innerHTML =
      "<svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M4 6h16M4 12h16M4 18h16'/></svg>";
  }),
);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    nav.classList.remove("open");
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-label", "Abrir menú");
    menu.innerHTML =
      "<svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M4 6h16M4 12h16M4 18h16'/></svg>";
  }
});
document.querySelector("#quote-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  if (!String(data.get("name")).trim()) {
    document
      .querySelector("#name")
      .setCustomValidity("Escribe tu nombre para preparar la cotización.");
    document.querySelector("#name").reportValidity();
    return;
  }
  const chosen = new Set(selection);
  const piece = data.get("piece");
  if (piece !== "Quiero asesoría") chosen.add(piece);
  const message = [
    "Hola, Cabra Negra. Soy " + data.get("name").trim() + ".",
    "Me gustaría cotizar un proyecto.",
    "Piezas: " +
      (chosen.size
        ? [...chosen].join(", ")
        : "Me gustaría asesoría para elegir") +
      ".",
    "Cantidad: " + (data.get("quantity") || "Por definir") + ".",
    "Ciudad de envío: " + (data.get("city").trim() || "Por definir") + ".",
    "Personalización: " + data.get("engraving") + ".",
    "Tipo de proyecto: " + data.get("project-type") + ".",
    data.get("board-design") !== "Por definir"
      ? "Diseño de tabla: " + data.get("board-design") + "."
      : "",
    data.get("board-wood") !== "Quiero asesoría"
      ? "Madera: " + data.get("board-wood") + "."
      : "",
    data.get("board-size").trim()
      ? "Medidas solicitadas: " + data.get("board-size").trim() + "."
      : "",
    data.get("details").trim() ? "Mi idea: " + data.get("details").trim() : "",
    "¿Me ayudan con opciones, precio y tiempo de producción?",
  ]
    .filter(Boolean)
    .join("\n");
  document.querySelector("#quote-message").textContent = message;
  document.querySelector("#quote-send").href = wa(message);
  document.querySelector("#quote-dialog").showModal();
  document.body.classList.add("dialog-open");
});

const reelButton = document.querySelector(".reel-load");
reelButton.addEventListener("click", () => {
  if (!window.cabraPrivacy.instagramAllowed()) {
    window.cabraPrivacy.open();
    return;
  }
  const frame = document.querySelector("#reel-frame");
  frame.hidden = false;
  document.querySelector(".reel-help").hidden = false;
  reelButton.innerHTML =
    "Reel cargado <svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M12 4v16M5 13l7 7 7-7'/></svg>";
  reelButton.disabled = true;
  const embed = document.createElement("iframe");
  embed.src = "https://www.instagram.com/reel/DOMkJ0mgXOy/embed/";
  embed.title = "Reel destacado de Cabra Negra: el ritual de la parrilla";
  embed.allow = "encrypted-media; fullscreen; picture-in-picture";
  embed.referrerPolicy = "no-referrer";
  embed.setAttribute(
    "sandbox",
    "allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox",
  );
  embed.setAttribute("allowfullscreen", "");
  frame.replaceChildren(embed);
});

// Cotización: vista previa accesible, sin depender de ventanas emergentes.
const quoteDialog = document.querySelector("#quote-dialog");
document
  .querySelector("#name")
  .addEventListener("input", (event) => event.target.setCustomValidity(""));
for (const button of quoteDialog.querySelectorAll(".quote-close, #quote-edit"))
  button.addEventListener("click", () => quoteDialog.close());
for (const modal of document.querySelectorAll("dialog")) {
  modal.addEventListener("close", () => {
    if (!document.querySelector("dialog[open]"))
      document.body.classList.remove("dialog-open");
  });
  modal.addEventListener("click", (event) => {
    if (event.target !== modal) return;
    const rect = modal.getBoundingClientRect();
    if (
      event.clientX < rect.left ||
      event.clientX > rect.right ||
      event.clientY < rect.top ||
      event.clientY > rect.bottom
    )
      modal.close();
  });
}
// Portada cinematográfica: video original, brasa y profundidad al deslizar.
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const film = document.querySelector("#hero-film");
const cinema = document.querySelector(".hero-cinema");
const motionToggle = document.querySelector("#motion-toggle");
let motionPaused = reducedMotion.matches;
let framePending = false;
function syncMotion() {
  document.body.classList.toggle("motion-paused", motionPaused);
  motionToggle.setAttribute("aria-pressed", String(motionPaused));
  motionToggle.innerHTML = motionPaused
    ? "Activar animación <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='m8 5 11 7-11 7Z'/></svg></span>"
    : "Pausar animación <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M8 5v14M16 5v14'/></svg></span>";
  if (motionPaused) {
    film.pause();
  } else if (!document.hidden) {
    film.play().catch(() => {
      film.classList.add("film-fallback");
    });
  }
  updateHero();
}
function updateHero() {
  framePending = false;
  const rect = cinema.getBoundingClientRect();
  const max = Math.max(1, cinema.offsetHeight - innerHeight + 91);
  const progress = Math.min(1, Math.max(0, -rect.top / max));
  cinema.style.setProperty("--story-progress", motionPaused ? 0 : progress);
}
function scheduleHero() {
  if (framePending) return;
  framePending = true;
  requestAnimationFrame(updateHero);
}
motionToggle.addEventListener("click", () => {
  motionPaused = !motionPaused;
  syncMotion();
});
reducedMotion.addEventListener("change", (event) => {
  motionPaused = event.matches;
  syncMotion();
});
film.addEventListener("playing", () => film.classList.add("film-ready"));
film.addEventListener("error", () => film.classList.add("film-fallback"));
addEventListener("scroll", scheduleHero, { passive: true });
addEventListener("resize", () => {
  scheduleHero();
  if (innerWidth > 780) {
    nav.classList.remove("open");
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-label", "Abrir menú");
    menu.innerHTML =
      "<svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M4 6h16M4 12h16M4 18h16'/></svg>";
  }
});
const heroVisibility = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting && !motionPaused && !document.hidden)
        film.play().catch(() => {});
      else film.pause();
    }
  },
  { threshold: 0 },
);
heroVisibility.observe(cinema);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) film.pause();
  else syncMotion();
});
syncMotion();
const revealObserver = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        revealObserver.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.08 },
);
document
  .querySelectorAll(".section-heading,.custom-copy,.steps article")
  .forEach((el) => {
    el.classList.add("reveal");
    revealObserver.observe(el);
  });

// Reproducción solicitada por el visitante; pausa el fondo y el reel al reproducir.
const creatorsVideo = document.querySelector("#creators-video");
const watchCreators = document.querySelector(".watch-creators");
watchCreators.addEventListener("click", () => {
  if (!creatorsVideo.paused) {
    creatorsVideo.pause();
    return;
  }
  creatorsVideo.scrollIntoView({
    behavior: reducedMotion.matches ? "instant" : "smooth",
    block: "center",
  });
  creatorsVideo.play().catch(() => {
    creatorsVideo.focus();
  });
});
creatorsVideo.addEventListener("play", () => {
  film.pause();
  document.querySelector("#reel-frame").replaceChildren();
  const reelAction = document.querySelector(".reel-load");
  reelAction.disabled = false;
  reelAction.innerHTML =
    "Ver el reel <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='m8 5 11 7-11 7Z'/></svg></span>";
  watchCreators.innerHTML =
    "Pausar video <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M8 5v14M16 5v14'/></svg></span>";
});
creatorsVideo.addEventListener("pause", () => {
  watchCreators.innerHTML =
    "Continuar video <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='m8 5 11 7-11 7Z'/></svg></span>";
});
creatorsVideo.addEventListener("ended", () => {
  watchCreators.innerHTML =
    "Volver a ver <span><svg class='ui-icon' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true' focusable='false'><path d='M20 8a9 9 0 1 0 1 7M20 3v6h-6'/></svg></span>";
});
const creatorsVisibility = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting && !creatorsVideo.paused) creatorsVideo.pause();
    }
  },
  { threshold: 0 },
);
creatorsVisibility.observe(creatorsVideo);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) creatorsVideo.pause();
});

// La configuración se incorpora al mismo mensaje de WhatsApp.
function focusProject() {
  document
    .querySelector("#cotizar")
    .scrollIntoView({ behavior: reducedMotion.matches ? "instant" : "smooth" });
  document.querySelector("#name").focus({ preventScroll: true });
}
document.querySelectorAll(".board-configure").forEach((button) =>
  button.addEventListener("click", () => {
    selection.add(button.dataset.piece);
    document.querySelector("#piece").value = button.dataset.piece;
    document.querySelector("#board-design").value = button.dataset.board;
    updateSelection();
    focusProject();
  }),
);
document.querySelector("#wholesale-quote").addEventListener("click", () => {
  document.querySelector("#project-type").value = "Restaurante o negocio";
  focusProject();
});

// Galería de trabajos: fotos completas, navegación por teclado y solicitud contextual.
const workPhotos = [
  {
    file: "tablas-produccion.webp",
    category: "produccion",
    caption: "Tablas personalizadas en producción",
    piece: "Tablas de plato",
    width: 1200,
    height: 1600,
  },
  {
    file: "tequileros-ojo-tigre.webp",
    category: "servicio",
    caption: "Tequileros para Ojo de Tigre",
    piece: "Tequileros",
    width: 900,
    height: 1600,
  },
  {
    file: "hierro-burro.webp",
    category: "produccion",
    caption: "Piezas de hierro con bases personalizadas",
    piece: "Hierro con tabla",
    width: 1200,
    height: 1600,
  },
  {
    file: "tablas-cuadros-taller.webp",
    category: "produccion",
    caption: "Diseños en cuadros y tiras desde el taller",
    piece: "Tablas variadas",
    width: 1200,
    height: 1600,
  },
  {
    file: "tablas-redondas-lote.webp",
    category: "produccion",
    caption: "Tablas redondas por pedido",
    piece: "Tablas variadas",
    width: 1200,
    height: 1600,
  },
  {
    file: "sets-mesa-cuchillos.webp",
    category: "servicio",
    caption: "Tablas, cubiertos y accesorios con la misma identidad",
    piece: "Platos y cubiertos",
    width: 1282,
    height: 1600,
  },
  {
    file: "hierro-hummo.webp",
    category: "servicio",
    caption: "Hierro y madera para el servicio",
    piece: "Hierro con tabla",
    width: 1200,
    height: 1600,
  },
  {
    file: "rodajas-naturales.webp",
    category: "servicio",
    caption: "Rodajas naturales y detalles para la barra",
    piece: "Tablas variadas",
    width: 1200,
    height: 1600,
  },
  {
    file: "pedido-las-alitas.webp",
    category: "produccion",
    caption: "Tablas para Las Alitas preparadas por lote",
    piece: "Tablas de plato",
    width: 1200,
    height: 1600,
  },
  {
    file: "cajas-madera.webp",
    category: "accesorios",
    caption: "Cajas de madera con tapa y grabado",
    piece: "Cajas de madera",
    width: 1200,
    height: 1600,
  },
  {
    file: "cuchillos-grabados.webp",
    category: "accesorios",
    caption: "Cuchillos con grabado en el mango",
    piece: "Cuchillos",
    width: 900,
    height: 1600,
  },
  {
    file: "portapanuelos-personalizados.webp",
    category: "accesorios",
    caption: "Portapañuelos personalizados para negocios",
    piece: "Portapañuelos",
    width: 1200,
    height: 1600,
  },
  {
    file: "mandiles-equipo-restaurante.webp",
    category: "accesorios",
    caption: "Mandiles para el equipo completo",
    piece: "Delantales y mandiles",
    width: 1440,
    height: 1078,
  },
  {
    file: "grillbox-beastown-pedido.webp",
    category: "servicio",
    caption: "Grillbox personalizadas para The Beastown",
    piece: "Grillbox",
    width: 1200,
    height: 1600,
  },
  {
    file: "platos-las-alitas.webp",
    category: "servicio",
    caption: "Platos de madera personalizados para Las Alitas",
    piece: "Platos y cubiertos",
    width: 1200,
    height: 1600,
  },
  {
    file: "sets-regalo-personalizados.webp",
    category: "servicio",
    caption: "Tablas y cuchillos con grabados individuales",
    piece: "Platos y cubiertos",
    width: 900,
    height: 1600,
  },
  {
    file: "hierro-restaurantes.webp",
    category: "servicio",
    caption: "Bases de madera y piezas de hierro para restaurantes",
    piece: "Hierro con tabla",
    width: 900,
    height: 1600,
  },
  {
    file: "tablas-el-mayor.webp",
    category: "produccion",
    caption: "Tablas con grabado para El Mayor",
    piece: "Tablas de plato",
    width: 1200,
    height: 1600,
  },
  {
    file: "tablas-bodega-carnes.webp",
    category: "servicio",
    caption: "Tablas y cuchillos para Bodega Carnes",
    piece: "Tablas de plato",
    width: 900,
    height: 1600,
  },
  {
    file: "mandiles-personalizados.webp",
    category: "accesorios",
    caption: "Mandiles con la marca de tu negocio",
    piece: "Delantales y mandiles",
    width: 1200,
    height: 1600,
  },
  {
    file: "cuchillos-surtido.webp",
    category: "accesorios",
    caption: "Cuchillos para mesa y servicio",
    piece: "Cuchillos",
    width: 1600,
    height: 1206,
  },
];
const workDialog = document.querySelector("#work-dialog");
let workIndex = 0;
let workCategory = "produccion";
function showWork(index) {
  workIndex = index;
  const photo = workPhotos[index];
  const image = document.querySelector("#work-photo");
  image.src = "assets/mayoreo/" + photo.file;
  image.alt = photo.caption;
  document.querySelector("#work-title").textContent = photo.caption;
}
function moveWork(direction) {
  const indices = workPhotos
    .map((p, index) => (p.category === workCategory ? index : -1))
    .filter((index) => index >= 0);
  const current = indices.indexOf(workIndex);
  showWork(indices[(current + direction + indices.length) % indices.length]);
}
document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-work-index]");
  if (!opener) return;
  const index = Number(opener.dataset.workIndex);
  workCategory = workPhotos[index].category;
  showWork(index);
  workDialog.showModal();
  document.body.classList.add("dialog-open");
});
document.querySelectorAll("[data-work-filter]").forEach((button) =>
  button.addEventListener("click", () => {
    workCategory = button.dataset.workFilter;
    document.querySelectorAll("[data-work-filter]").forEach((item) => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    let count = 0;
    document.querySelectorAll(".work-card").forEach((card) => {
      card.hidden = card.dataset.workCategory !== workCategory;
      if (!card.hidden) count++;
    });
    document.querySelector("#works-status").textContent =
      count + " fotografías: " + button.textContent;
  }),
);
document
  .querySelector(".work-close")
  .addEventListener("click", () => workDialog.close());
document
  .querySelector("#work-prev")
  .addEventListener("click", () => moveWork(-1));
document
  .querySelector("#work-next")
  .addEventListener("click", () => moveWork(1));
workDialog.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") {
    event.preventDefault();
    moveWork(-1);
  }
  if (event.key === "ArrowRight") {
    event.preventDefault();
    moveWork(1);
  }
});
document.querySelector("#work-quote").addEventListener("click", () => {
  const photo = workPhotos[workIndex];
  selection.add(photo.piece);
  document.querySelector("#piece").value = photo.piece;
  document.querySelector("#project-type").value = "Restaurante o negocio";
  const details = document.querySelector("#details");
  const reference = "Me interesa un proyecto similar a: " + photo.caption + ".";
  if (!details.value.includes(reference))
    details.value = [details.value.trim(), reference]
      .filter(Boolean)
      .join("\n");
  updateSelection();
  workDialog.close();
  focusProject();
});

// El formulario no puede enviarse por HTTP si JavaScript está desactivado.
document.querySelector("#quote-form button[type=submit]").disabled = false;
