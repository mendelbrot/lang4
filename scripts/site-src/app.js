(() => {
  const pages = Array.from(document.querySelectorAll(".page[data-page]"));
  const pageMap = new Map(pages.map((el) => [el.dataset.page, el]));

  const themeToggle = document.getElementById("theme-toggle");

  const modal = document.getElementById("word-modal");
  const closeBtn = document.getElementById("modal-close");
  const modalGlyph = document.getElementById("modal-glyph");
  const modalSpelling = document.getElementById("modal-spelling");
  const modalShort = document.getElementById("modal-short");
  const modalDefinition = document.getElementById("modal-definition");

  const sectionModal = document.getElementById("section-modal");
  const sectionNavOpen = document.getElementById("section-nav-open");
  const sectionModalClose = document.getElementById("section-modal-close");
  const sectionModalHome = document.getElementById("section-modal-home");
  const sectionModalTop = document.getElementById("section-modal-top");
  const sectionModalContent = document.getElementById("section-modal-content");

  const glyphPopup = document.getElementById("glyph-popup");
  const glyphPopupSpelling = document.getElementById("glyph-popup-spelling");
  const glyphPopupShort = document.getElementById("glyph-popup-short");

  let activePageEl = null;
  let lastTrigger = null;
  let activeGlyphBtn = null;

  function positionGlyphPopup() {
    if (!activeGlyphBtn || !glyphPopup || glyphPopup.hidden) {
      return;
    }
    const btnRect = activeGlyphBtn.getBoundingClientRect();
    const bodyRect = document.body.getBoundingClientRect();
    const bodyStyle = window.getComputedStyle(document.body);
    const bodyPaddingRight = parseFloat(bodyStyle.paddingRight) || 0;
    const bodyPaddingLeft = parseFloat(bodyStyle.paddingLeft) || 0;
    const bodyContentRight = bodyRect.right - bodyPaddingRight;
    const bodyContentLeft = bodyRect.left + bodyPaddingLeft;
    const popupWidth = glyphPopup.offsetWidth;

    let leftViewport = btnRect.left;
    if (leftViewport + popupWidth > bodyContentRight) {
      leftViewport = Math.max(bodyContentLeft, bodyContentRight - popupWidth);
    }

    const topViewport = btnRect.bottom + 6;
    glyphPopup.style.left = `${leftViewport + window.scrollX}px`;
    glyphPopup.style.top = `${topViewport + window.scrollY}px`;
  }

  function closeGlyphPopup() {
    if (activeGlyphBtn) {
      activeGlyphBtn.classList.remove("is-active");
      activeGlyphBtn = null;
    }
    if (glyphPopup) {
      glyphPopup.hidden = true;
    }
  }

  function toggleGlyphPopup(btn) {
    if (activeGlyphBtn === btn) {
      closeGlyphPopup();
      return;
    }
    if (activeGlyphBtn) {
      activeGlyphBtn.classList.remove("is-active");
    }
    activeGlyphBtn = btn;
    activeGlyphBtn.classList.add("is-active");

    if (!glyphPopup) {
      return;
    }
    glyphPopupSpelling.textContent = btn.dataset.spelling || "";
    glyphPopupShort.textContent = btn.dataset.short || "";
    glyphPopup.style.left = "0px";
    glyphPopup.style.top = "0px";
    glyphPopup.hidden = false;
    positionGlyphPopup();
  }

  function openModal(card) {
    closeGlyphPopup();
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

  function populateSectionModal() {
    if (!sectionModalContent || !activePageEl || !activePageEl.dataset.jump) {
      return false;
    }
    sectionModalContent.textContent = "";
    const groups = new Map();

    if (activePageEl.dataset.jump === "words") {
      const targets = activePageEl.querySelectorAll("[data-jump-label]");
      for (const el of targets) {
        const groupName = el.dataset.jumpGroup || "";
        if (!groups.has(groupName)) {
          groups.set(groupName, []);
        }
        groups.get(groupName).push({
          targetId: el.id,
          label: el.dataset.jumpLabel || "",
        });
      }
    } else {
      const groupName = activePageEl.dataset.title || "";
      const items = [];
      const targets = activePageEl.querySelectorAll("[data-jump-label]");
      for (const el of targets) {
        items.push({
          targetId: el.id,
          label: el.dataset.jumpLabel || "",
        });
      }
      groups.set(groupName, items);
    }

    for (const [groupTitle, items] of groups) {
      const groupEl = document.createElement("div");
      groupEl.className = "section-group";

      const titleEl = document.createElement("h3");
      titleEl.className = "section-group-title";
      titleEl.textContent = groupTitle;
      groupEl.appendChild(titleEl);

      const scrollEl = document.createElement("div");
      scrollEl.className = "section-grid-scroll";

      const listEl = document.createElement("ul");
      listEl.className = "toc-sublist";

      for (const item of items) {
        const li = document.createElement("li");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "section-chip";
        btn.dataset.jumpTarget = item.targetId;
        btn.textContent = item.label;
        li.appendChild(btn);
        listEl.appendChild(li);
      }

      scrollEl.appendChild(listEl);
      groupEl.appendChild(scrollEl);
      sectionModalContent.appendChild(groupEl);
    }

    return groups.size > 0;
  }

  function openSectionModal() {
    if (!sectionModal || !populateSectionModal()) {
      return;
    }
    closeGlyphPopup();
    sectionModal.hidden = false;
    document.body.style.overflow = "hidden";
    if (sectionModalClose) {
      sectionModalClose.focus();
    }
  }

  function closeSectionModal() {
    if (!sectionModal || sectionModal.hidden) {
      return;
    }
    sectionModal.hidden = true;
    document.body.style.overflow = "";
    if (sectionNavOpen) {
      sectionNavOpen.blur();
    }
  }

  function showPage() {
    closeModal();
    closeSectionModal();
    closeGlyphPopup();
    const rawHash = decodeURIComponent(window.location.hash.replace(/^#/, ""));
    const targetSlug = pageMap.has(rawHash) ? rawHash : "home";

    for (const page of pages) {
      page.hidden = page.dataset.page !== targetSlug;
    }

    activePageEl = pageMap.get(targetSlug) || null;
    if (sectionNavOpen) {
      sectionNavOpen.hidden = !(activePageEl && activePageEl.dataset.jump);
    }

    const title = activePageEl ? activePageEl.dataset.title : "";
    document.title = targetSlug === "home" || !title
      ? "zirkekpemim"
      : `zirkekpemim — ${title}`;

    window.scrollTo(0, 0);
  }

  window.addEventListener("hashchange", showPage);
  window.addEventListener("resize", positionGlyphPopup);
  showPage();

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const root = document.documentElement;
      if (root.dataset.theme === "light") {
        delete root.dataset.theme;
      } else {
        root.dataset.theme = "light";
      }
      themeToggle.blur();
    });
  }

  document.addEventListener("click", (event) => {
    const glyphBtn = event.target.closest(".script-glyph-btn");
    if (glyphBtn) {
      toggleGlyphPopup(glyphBtn);
      return;
    }

    if (activeGlyphBtn && !event.target.closest("#glyph-popup")) {
      closeGlyphPopup();
    }

    const card = event.target.closest(".word-card");
    if (card) {
      openModal(card);
      return;
    }

    const chip = event.target.closest(".section-chip");
    if (chip) {
      const targetId = chip.dataset.jumpTarget;
      closeSectionModal();
      if (targetId) {
        const target = document.getElementById(targetId);
        if (target) {
          target.scrollIntoView();
        }
      }
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }

  if (sectionNavOpen) {
    sectionNavOpen.addEventListener("click", openSectionModal);
  }

  if (sectionModalClose) {
    sectionModalClose.addEventListener("click", closeSectionModal);
  }

  if (sectionModalHome) {
    sectionModalHome.addEventListener("click", () => {
      closeSectionModal();
      if (window.location.hash && window.location.hash !== "#") {
        window.location.hash = "#";
      } else {
        showPage();
      }
    });
  }

  if (sectionModalTop) {
    sectionModalTop.addEventListener("click", () => {
      closeSectionModal();
      window.scrollTo(0, 0);
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    if (modal && !modal.hidden) {
      closeModal();
    } else if (sectionModal && !sectionModal.hidden) {
      closeSectionModal();
    } else if (activeGlyphBtn) {
      closeGlyphPopup();
    }
  });
})();
