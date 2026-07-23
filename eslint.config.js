const security = require("eslint-plugin-security");

module.exports = [
  { ignores: ["node_modules/**", "db-init/**"] },
  security.configs.recommended,
];
