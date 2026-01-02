function toggleNotes(button) {
  const mainRow = button.closest("tr");
  const notesRow = mainRow.nextElementSibling;

  notesRow.classList.toggle("hidden");
}

document.querySelectorAll("td.status").forEach(td => {
    const status = parseInt(td.textContent.trim());

    if (status >= 200 && status < 300) {
        td.classList.add("status-2xx");
    } else if (status >= 300 && status < 400) {
        td.classList.add("status-3xx");
    } else if (status >= 400 && status < 500) {
        td.classList.add("status-4xx");
    } else if (status >= 500) {
        td.classList.add("status-5xx");
    }
});