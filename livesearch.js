document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("employee-search");
  const resultsBody = document.getElementById("employee-results-body");
  const noResultsBody = document.getElementById("no-results-body");

  if (!searchInput || !resultsBody || !noResultsBody) {
    return;
  }

  const debounce = (fn, wait = 250) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), wait);
    };
  };

  const renderEmployees = (employees) => {
    if (!Array.isArray(employees) || employees.length === 0) {
      resultsBody.innerHTML = "";
      noResultsBody.style.display = "table-row-group";
      return;
    }

    noResultsBody.style.display = "none";
    resultsBody.innerHTML = employees
      .map((employee) => {
        return `
          <tr>
            <td>${employee.name}</td>
            <td>${employee.email}</td>
            <td>${employee.role}</td>
            <td><span class="badge">${employee.status}</span></td>
          </tr>
        `;
      })
      .join("");
  };

  const fetchEmployees = async (query) => {
    const url = `/employees/search?q=${encodeURIComponent(query)}`;
    try {
      const res = await fetch(url, {
        headers: { "Accept": "application/json" },
      });
      if (!res.ok) {
        throw new Error(`Search failed: ${res.status}`);
      }
      const data = await res.json();
      renderEmployees(data);
    } catch (error) {
      console.error(error);
      resultsBody.innerHTML = "";
      noResultsBody.style.display = "table-row-group";
      noResultsBody.querySelector("td").textContent = "Unable to load search results.";
    }
  };

  const handleSearch = debounce((event) => {
    const query = event.target.value.trim();
    fetchEmployees(query);
  }, 230);

  searchInput.addEventListener("input", handleSearch);
});