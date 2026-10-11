# Network Automation Lab

A lightweight, self-hosted network configuration management and
automation platform built with Podman, Python, Git, and Ansible.

## Architecture

- Pod 1: Forgejo and local CI runner
- Pod 2: Nginx, FastAPI, and SQLite
- Pod 3: Network inventory and configuration management

## Initial scope

- Device and location inventory
- Reusable network configuration templates
- Configuration validation and revision history
- Approval-gated configuration publishing
- Local CI/CD for application code
- Ansible integration in a later phase

## Safety

Draft configurations must not overwrite approved configurations.
Live network deployment is outside the initial scope.

## Development

See docs/ for architecture and implementation notes.
