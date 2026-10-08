/* Progressive enhancement: navigation and content work without JavaScript. */
const header = document.querySelector(".site-header");
const menu = document.querySelector(".menu-toggle");
const nav = document.querySelector("#navigation");
if (header && menu && nav) {
  header.classList.add("js-menu");
  const close = () => {
    menu.setAttribute("aria-expanded", "false");
    nav.classList.remove("open");
  };
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("open", open);
  });
  nav
    .querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", close));
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menu.getAttribute("aria-expanded") === "true"
    ) {
      close();
      menu.focus();
    }
  });
}
document.querySelectorAll(".flow-window").forEach((window) => {
  const button = window.querySelector(".flow-next");
  const message = window.querySelector("[data-flow-message]");
  let state = 0;
  const messages = [
    "Order queued. Ready for the executor.",
    "Print command sent. Monitoring the spooler.",
    "Completion event received. State updated.",
  ];
  button.addEventListener("click", () => {
    state = (state + 1) % 3;
    window
      .querySelectorAll("[data-stage]")
      .forEach((stage) =>
        stage.classList.toggle("active", Number(stage.dataset.stage) === state),
      );
    message.textContent = messages[state];
    button.firstChild.textContent =
      state === 2 ? "Replay the model " : "Run next event ";
  });
});
const search = document.querySelector("#site-search");
if (search) {
  const status = document.querySelector("[data-search-status]");
  const results = document.querySelector("[data-search-results]");
  let entries;
  let indexPromise;
  let revision = 0;
  search.addEventListener("input", async () => {
    const current = ++revision;
    const query = search.value.trim().toLowerCase();
    results.replaceChildren();
    if (!query) {
      status.textContent = "Start typing to explore projects and articles.";
      return;
    }
    status.textContent = "Searching…";
    try {
      if (!entries) {
        indexPromise ||= fetch(search.dataset.index)
          .then((response) => {
            if (!response.ok) throw new Error("Search index unavailable");
            return response.json();
          })
          .catch((error) => {
            indexPromise = undefined;
            throw error;
          });
        entries = await indexPromise;
      }
      if (current !== revision) return;
      const words = query.split(/\s+/);
      const matches = entries.filter((entry) =>
        words.every((word) =>
          `${entry.title} ${entry.content}`.toLowerCase().includes(word),
        ),
      );
      status.textContent = matches.length
        ? `${matches.length} result${matches.length === 1 ? "" : "s"} for “${search.value.trim()}”`
        : "No matches. Try a different technology or project name.";
      for (const entry of matches) {
        const link = document.createElement("a");
        const url = new URL(entry.permalink, location.href);
        link.href = url.pathname + url.search + url.hash;
        link.className = "writing-row";
        const kind = document.createElement("span");
        kind.className = "mono";
        kind.textContent = url.pathname.startsWith("/projects/")
          ? "PROJECT"
          : "WRITING";
        const body = document.createElement("div");
        const title = document.createElement("h2");
        title.textContent = entry.title;
        const excerpt = document.createElement("p");
        excerpt.textContent = (entry.summary || entry.content || "").slice(
          0,
          160,
        );
        const arrow = document.createElement("span");
        arrow.className = "row-arrow";
        arrow.setAttribute("aria-hidden", "true");
        arrow.innerHTML =
          '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19 19 5M5 5h14v14"/></svg>';
        body.append(title, excerpt);
        link.append(kind, body, arrow);
        results.append(link);
      }
    } catch (error) {
      if (current === revision)
        status.textContent =
          "Search is temporarily unavailable. You can still browse Work and Writing above.";
    }
  });
}
