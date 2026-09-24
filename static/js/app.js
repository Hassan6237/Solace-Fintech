// Tiny UI helper: shows a toast when the page loads with a ?earned=N param,
// used to confirm points were just awarded after completing a lesson,
// scenario, or check-in.
(function () {
  const params = new URLSearchParams(window.location.search);
  const earned = params.get("earned");
  if (earned) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = "+" + earned + " points";
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add("show"));
    setTimeout(() => toast.classList.remove("show"), 2200);
  }
})();
