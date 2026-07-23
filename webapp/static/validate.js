// Frontend mirror of OWASP Proactive Controls C7 / ASVS V2.1.1-2.1.2 (Level 1):
// length bounds only. The breach/common-password check (ASVS 2.1.7) needs the
// server-side database, so it is enforced authoritatively in the backend.
const MIN_LENGTH = 12;
const MAX_LENGTH = 128;

function isValidPassword(password) {
  return password.length >= MIN_LENGTH && password.length <= MAX_LENGTH;
}

function attachValidation(formId, passwordId, errorId) {
  document.getElementById(formId).addEventListener("submit", (event) => {
    const password = document.getElementById(passwordId).value;
    if (!isValidPassword(password)) {
      event.preventDefault();
      document.getElementById(errorId).textContent =
        `Password must be ${MIN_LENGTH}-${MAX_LENGTH} characters long.`;
    }
  });
}
