(() => {
  const pages = Array.from(document.querySelectorAll(".page[data-page]"));
  const pageMap = new Map(pages.map((el) => [el.dataset.page, el]));

  const modal = document.getElementById("word-modal");
  const closeBtn = document.getElementById("modal-close");
  const modalGlyph = document.getElementById("modal-glyph");
  const modalSpelling = document.getElementById("modal-spelling");
  const modalShort = document.getElementById("modal-short");
  const modalDefinition = document.getElementById("modal-definition");
  const sectionNav = document.getElementById("section-nav");
  let lastTrigger = null;

  function openModal(card) {
    lastTrigger = card;
    const glyph = card.querySelector(".glyph");
    modalGlyph.innerHTML = glyph ? glyph.innerHTML : "";
    modalSpelling.textContent = card.dataset.spelling || "";
    modalShort.textContent = card.dataset.short || "";
    modalDefinition.textContent = card.dataset.definition || "";
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    closeBtn.focus();
  }

  function closeModal() {
    if (!modal || modal.hidden) {
      return;
    }
    modal.hidden = true;
    document.body.style.overflow = "";
    if (lastTrigger) {
      lastTrigger.focus();
      lastTrigger = null;
    }
  }

  function showPage() {
    closeModal();
    const rawHash = decodeURIComponent(window.location.hash.replace(/^#/, ""));
    const targetSlug = pageMap.has(rawHash) ? rawHash : "home";

    for (const page of pages) {
      page.hidden = page.dataset.page !== targetSlug;
    }

    const active = pageMap.get(targetSlug);
    const title = active ? active.dataset.title : "";
    document.title = targetSlug === "home" || !title
      ? "zirkekpemim"
      : `zirkekpemim — ${title}`;

    window.scrollTo(0, 0);
  }

  window.addEventListener("hashchange", showPage);
  showPage();

  document.addEventListener("click", (event) => {
    const card = event.target.closest(".word-card");
    if (card) {
      openModal(card);
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal && !modal.hidden) {
      closeModal();
    }
  });

  if (sectionNav) {
    sectionNav.addEventListener("change", () => {
      const targetId = sectionNav.value;
      if (!targetId) {
        return;
      }
      const target = document.getElementById(`words-${targetId}`);
      if (target) {
        target.scrollIntoView();
      }
      sectionNav.selectedIndex = 0;
    });
  }
})();
