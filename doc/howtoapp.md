# Application Roadmap

1. Stabilize the command-line pipeline and configuration.
2. Expose playlist analysis through a small service API.
3. Replace placeholder recommendations with a validated model.
4. Add a web interface only after the analysis and creation contracts are stable.

Each layer should depend on explicit input and output schemas so the user interface does not become coupled to individual scripts.
