# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-04-30

### Added
- Basic web interface built with Flask to manage text datasets.
- Dataset list view with the following columns:
  - `Name`, `Description`, `Samples`, `Size`, `Labels`, `Created At`, `Updated At`, `Created By`, `Actions`.
- Actions on datasets:
  - **Create** a new dataset by entering name, description, and labels.
  - **Update** dataset to edit name, description, or labels.
  - **Delete** dataset immediately.
  - **View** dataset to open the sample list.

- Dataset detail view (samples) with the following columns:
  - `Sample ID`, `Text`, `Label`, `Created At`, `Updated At`, `Created By`, `Actions`.

- Actions on samples:
  - **Add** new sample by entering text and selecting a label.
  - **Update** sample text or label.
  - **Delete** sample immediately.

### Notes
- All timestamps are automatically generated.
- Actions are performed without confirmation dialogs.
- No versioning, validation, or role-based restrictions are currently enforced.
