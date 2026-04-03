# Concepts

AudioDatasetAudit focuses on dataset quality issues that often stay invisible until after training.

Core ideas:
- **Manifest-first design**: a dataset is described by a table, not by hard-coded assumptions.
- **Checks**: each audit is implemented as a small reusable component.
- **Reports**: outputs should be easy to read by humans and easy to consume by other tools.
- **Reproducibility**: the audit result should be shareable and repeatable.
