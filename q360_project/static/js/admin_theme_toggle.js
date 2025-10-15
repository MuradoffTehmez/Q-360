(function () {
  function setTheme(theme) {
    var body = document.body;
    var isDark = theme === "dark";
    body.classList.toggle("q360-dark", isDark);
    body.classList.toggle("dark-mode", isDark);
    document.documentElement.setAttribute(
      "data-theme",
      isDark ? "dark" : "light"
    );
    if (isDark) {
      localStorage.setItem("q360-admin-theme", "dark");
    } else {
      localStorage.setItem("q360-admin-theme", "light");
    }
    var button = document.querySelector(".q360-theme-toggle");
    if (button) {
      button.innerHTML = isDark
        ? "☀️\u00a0Aydın rejim"
        : "🌙\u00a0Qaranlıq rejim";
      button.setAttribute("aria-pressed", String(isDark));
      button.setAttribute(
        "title",
        isDark ? "Aydın rejimə keç" : "Qaranlıq rejimə keç"
      );
    }
  }

  function toggleTheme() {
    var isDark = document.body.classList.contains("q360-dark");
    setTheme(isDark ? "light" : "dark");
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (
      !document.body.classList.contains("jazzmin") &&
      !document.body.classList.contains("login-page")
    ) {
      return;
    }

    var savedTheme = localStorage.getItem("q360-admin-theme");
    if (savedTheme === "dark") {
      setTheme("dark");
    } else if (savedTheme === "light") {
      setTheme("light");
    } else if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      setTheme("dark");
    } else {
      setTheme("light");
    }

    var navContainers = document.querySelectorAll(".navbar .navbar-nav");
    if (navContainers.length > 0) {
      var navContainer = navContainers[navContainers.length - 1];
      var existingToggle = navContainer.querySelector(".q360-theme-toggle");
      if (!existingToggle) {
        var listItem = document.createElement("li");
        listItem.className = "nav-item d-flex align-items-center px-2";

        var button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn-sm q360-theme-toggle";
        button.addEventListener("click", toggleTheme);
        listItem.appendChild(button);
        navContainer.appendChild(listItem);
      }
    } else {
      var loginCard = document.querySelector(".login-card-body");
      if (loginCard && !loginCard.querySelector(".q360-theme-toggle")) {
        var wrapper = document.createElement("div");
        wrapper.className = "d-flex justify-content-center mb-3";

        var loginToggle = document.createElement("button");
        loginToggle.type = "button";
        loginToggle.className = "btn btn-sm q360-theme-toggle";
        loginToggle.addEventListener("click", toggleTheme);

        wrapper.appendChild(loginToggle);
        loginCard.insertBefore(wrapper, loginCard.firstChild);
      }
    }

    setTheme(document.body.classList.contains("q360-dark") ? "dark" : "light");
  });
})();
