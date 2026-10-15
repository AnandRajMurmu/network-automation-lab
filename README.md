# Network Automation Lab

A lightweight, self-hosted network configuration management and automation platform built with **Podman, Python, FastAPI, PostgreSQL, Git, and Ansible**.

The project provides a central platform for managing network devices, generating configurations from reusable templates, validating changes, and controlling how approved configurations are published. It is designed as a modular lab environment that can run on a resource-constrained Linux system.

## Architecture

The platform is organized into three Podman pods:

- **Pod 1 — DevOps:** Forgejo for self-hosted Git hosting and a local CI runner for application build and deployment workflows.
- **Pod 2 — Application:** Nginx for serving the web dashboard and reverse proxying API requests, FastAPI for backend services, and PostgreSQL for persistent application data.
- **Pod 3 — Network Management:** Network inventory, configuration templates, generated configurations, and configuration revision storage, with Ansible integration planned for a later phase.

## Technology Stack

| Area | Technologies |
|---|---|
| Operating system | Linux |
| Containers | Podman, Podman Pods |
| Frontend | HTML, CSS, JavaScript |
| Backend API | Python, FastAPI, Uvicorn |
| Database | PostgreSQL |
| Configuration templating | Jinja2 |
| Web server and reverse proxy | Nginx |
| Version control | Git, GitHub; Forgejo planned for self-hosting |
| Code quality and testing | Ruff, Python `unittest`, API smoke tests |
| CI/CD | Forgejo Runner planned |
| Network automation | Ansible planned |

## Features

- **Device inventory:** Manage network devices, management IP addresses, device types, locations, and operational status.
- **Configuration generation:** Render network configurations using reusable Jinja2 templates and device-specific variables.
- **Configuration validation:** Detect missing template variables and invalid template paths before producing configuration output.
- **Revision history:** Track configuration changes and preserve previous revisions.
- **Approval workflow:** Separate draft configurations from approved configurations before publishing.
- **Local CI/CD:** Build, test, and deploy application components through a self-hosted workflow.
- **Network automation:** Integrate Ansible in a later phase for controlled configuration deployment and verification.

## Configuration Workflow

1. Select a reusable configuration template.
2. Provide device-specific values and generate a configuration draft.
3. Validate the generated configuration.
4. Review and approve the intended revision.
5. Publish the exact approved configuration to the network configuration store.

## Safety and Design Principles

- Draft configurations must never overwrite approved configurations.
- Publishing must use the exact revision that was reviewed and approved.
- Application deployment and network configuration approval are separate workflows.
- Live network-device deployment is outside the initial scope.
- Keep the architecture modular, lightweight, and suitable for local development.

## Development

The project is developed on Linux using Podman containers and a Git-based workflow.

Run the application locally through the configured Podman environment and access the dashboard at:

`http://127.0.0.1:8080`

API documentation is available at:

`http://127.0.0.1:8080/api/docs`

Refer to the `docs/` directory for architecture notes, implementation details, useful commands, and development progress.

---

**Network Automation Lab** — A practical environment for learning and building safer, version-controlled network automation workflows.
