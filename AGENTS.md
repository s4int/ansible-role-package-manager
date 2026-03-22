# AGENTS.md

This file contains essential information for agentic coding agents working on this Ansible role repository.

## Project Overview

This is an Ansible role (`ansible-role-package-manager`) that manages packages and repositories on Linux systems, supporting Debian, Ubuntu, Fedora, and Alpine distributions.

## Build, Lint, and Test Commands

### Environment Setup

Install dependencies using uv (recommended)

```shell
uv sync
```

Install pre-commit hooks using uv (recommended)

```shell
uv run prek install
```

### Testing

Run all molecule tests for all scenarios

```shell
uv run molecule test
```

Run specific scenario (e.g., Debian)

```shell
uv run molecule test --scenario-name Debian
```

Run single test step for scenario

```shell
uv run molecule --scenario-name Debian syntax
uv run molecule --scenario-name Debian converge
uv run molecule --scenario-name Debian verify
```

Run idempotence test specifically

```shell
uv run molecule --scenario-name Debian idempotence
```

Run with custom Docker image

```shell
MOLECULE_DISTRO=geerlingguy/docker-ubuntu2404-ansible:latest uv run molecule test --scenario-name Debian
```

### Linting and Validation

Run all linting (as defined in molecule lint step)

```shell
set -e ; uv run yamllint . ; uv run ansible-lint
```

Individual linters

```shell
uv run yamllint .
uv run ansible-lint
```

Run pre-commit hooks (if installed)

```shell
uv run prek run
```

### Code Style Guidelines

#### YAML Structure

- **Line Length**: Maximum 120 characters (warning level, not enforced strictly)
- **Indentation**: 2 spaces for YAML files
- **File Encoding**: UTF-8
- **Line Endings**: LF

#### Ansible Best Practices

- Use fully qualified collection names: `ansible.builtin.include_tasks`, `ansible.builtin.file`, etc.
- Follow the pattern `{{ ansible_facts['distribution'] }}` instead of `{{ ansible_distribution }}`
- Use `ansible_os_family` for family-specific tasks
- Include OS-dependent variables using `with_first_found` pattern
- Tag tasks appropriately: `package-manager`, `repo`, `update`, `upgrade`, `autoremove`

#### File Organization

```markdown
├── defaults/main.yml          # Default variables
├── vars/main.yml              # OS-specific variables
├── vars/Debian.yml           # Debian-specific variables
├── vars/Ubuntu.yml           # Ubuntu-specific variables
├── tasks/
│   ├── main.yml              # Main entry point
│   ├── package-manager.yml   # Package management orchestration
│   ├── repository-Debian.yml # Debian repository management
│   ├── packages-Debian.yml   # Debian package management
│   └── apt_repo_item.yml     # APT repository item template
├── handlers/main.yml         # Task handlers
├── meta/main.yml            # Role metadata
└── molecule/               # Test scenarios
```

#### Variable Naming Conventions

- Use snake_case for all variable names
- Prefix conditional packages: `apt_packages_conditional_*`
- Prefix repositories: `apt_repositories_*`
- OS-specific prefixes: `apt_`, `dnf_`, `apk_`
- Boolean defaults should be explicit: `true`/`false`

#### Error Handling

- Always use `failed_when` and `changed_when` for complex task conditions
- Include proper error messages in task names
- Use `no_log: true` for tasks handling sensitive data
- Implement proper idempotency checks

#### Testing Guidelines

- Use Testinfra for verification tests
- Mark tests with appropriate pytest markers: `@pytest.mark.debian`, `@pytest.mark.ubuntu`
- Test both traditional `.list` and modern `.sources` (deb822) repository formats
- Verify file permissions (644 for repo files, owned by root:root)
- Test package installation, removal, and repository management

#### Molecule Scenarios

- Each distribution should have its own scenario directory
- Shared playbooks should be in `molecule/shared/`
- Use Docker platform images from geerlingguy repository
- Test sequences should include: dependency, cleanup, destroy, syntax, create, prepare, converge, idempotence, side_effect, verify, cleanup, destroy

#### Pre-commit Hooks

- yamllint with custom `.yamllint` configuration
- ansible-lint for Ansible best practices
- Hooks only process `.yml` and `.yaml` files

#### Python Requirements

- Minimum Python version: 3.12
- Test dependencies include: molecule, pytest, testinfra, ansible-lint, yamllint
- Use uv for dependency management (dependency-groups in pyproject.toml)

#### Documentation

- README.md should be comprehensive and up-to-date
- Include example playbooks for different use cases
- Document all variables with descriptions, defaults, and types
- Include platform support matrix

#### Git Workflow

- Branch names should follow feature/description pattern
- Commit messages should follow conventional commit format
- All changes must pass linting and molecule tests before merge

## Common Development Tasks

### Adding New Distribution Support

1. Create `vars/{Distribution}.yml` with distribution-specific variables
2. Create `tasks/repository-{Distribution}.yml` for repository management
3. Create `tasks/packages-{Distribution}.yml` for package management
4. Add distribution to `meta/main.yml` platforms list
5. Create molecule scenario for testing

### Adding New Package Manager Features

1. Define variables in `defaults/main.yml`
2. Implement tasks in appropriate OS-specific task files
3. Add tests in molecule scenario `test_default.py`
4. Update documentation in README.md

### Running Single Tests

Run specific test function

```shell
uv run pytest molecule/Debian/tests/test_default.py::test_apt_sources_list_dir_exists -v
```

Run tests with specific marker

```shell
uv run pytest -m debian molecule/Debian/tests/
```
