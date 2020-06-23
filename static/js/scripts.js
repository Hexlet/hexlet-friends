// Activate Bootstrap tooltips
$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// Language selector
function switchLanguage(e) {
  e.preventDefault();
  const langForm = document.querySelector('#language-form');
  const selector = langForm.querySelector('select');
  selector.value = e.target.innerText.trim().toLowerCase();
  langForm.submit();
}

const langLinks = document.querySelectorAll('.inactive-lang-link');
langLinks.forEach((link) => link.addEventListener('click', switchLanguage));
