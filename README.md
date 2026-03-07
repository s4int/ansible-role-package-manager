# ansible-role-package-manager

Ansible role to manage packages and repositories on Linux systems.

## Supported Platforms

- **Debian**: bullseye, bookworm, trixie

## Requirements

- Ansible >= 2.20.1

## Debian/Ubuntu Specifics

### APT Configuration (Debian/Ubuntu)

| Variable | Default | Description |
|----------|---------|-------------|
| `apt_keyrings_dir` | `/etc/apt/keyrings` | Directory for storing GPG keys |
| `apt_deb822` | `false` | Use deb822 format for repositories (modern format) |
| `apt_repositories_remove` | `false` | Remove repository files not managed by this role |
| `apt_update` | `true` | Update package cache |
| `apt_update_cache_valid_time` | `3600` | Cache validity time in seconds |
| `apt_upgrade_type` | `dist` | Upgrade type (`dist`, `full`, `safe`) |
| `apt_autoremove` | `true` | Automatically remove unused packages |
| `apt_remove_purge` | `true` | Purge configuration files when removing packages |

### Package Management

Define packages to install using the `apt_packages` variable:

```yaml
apt_packages:
  - vim
  - curl
  - htop
```

Define packages to remove using the `apt_packages_remove` variable:

```yaml
apt_packages_remove:
  - nano
```

### Conditional Package Installation

Use variables prefixed with `apt_packages_conditional_*` for conditional package installation:

```yaml
apt_packages_conditional_docker:
  - packages:
      - docker-ce
      - docker-ce-cli
    condition: "{{ install_docker | default(false) }}"
    state: present
```

### Repository Management

Define repositories using variables prefixed with `apt_repositories_*`:

```yaml
apt_repositories_docker:
  - name: docker
    types:
      - deb
    uris:
      - "https://download.docker.com/linux/{{ ansible_distribution | lower }}"
    suites:
      - "{{ ansible_distribution_release }}"
    components:
      - stable
    signed_by: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"
    architectures:
      - amd64
```

#### Repository Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `name` | Yes | - | Repository identifier |
| `types` | Yes | - | Repository types (e.g., `['deb']`, `['deb', 'deb-src']`) |
| `uris` | Yes | - | Repository URLs |
| `suites` | Yes | - | Distribution codenames |
| `components` | No | `['main']` | Repository components |
| `signed_by` | No | - | URL to GPG key |
| `architectures` | No | - | Supported architectures |
| `state` | No | `present` | Repository state (`present`, `absent`) |
| `enabled` | No | `true` | Enable/disable repository (deb822 only) |

## RedHat Specifics

## Example Playbook

### Basic Usage

```yaml
- hosts: servers
  roles:
    - role: s4int.package_manager
      vars:
        apt_packages:
          - vim
          - curl
          - git
```

### With Custom Repository

```yaml
- hosts: servers
  pre_tasks:
    - name: Set repository configuration
      set_fact:
        apt_repositories_custom:
          - name: docker
            types: ['deb']
            uris:
              - "https://download.docker.com/linux/{{ ansible_distribution | lower }}"
            suites:
              - "{{ ansible_distribution_release }}"
            components: ['stable']
            signed_by: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"
  roles:
    - role: s4int.package_manager
      vars:
        apt_packages:
          - docker-ce
          - docker-ce-cli
          - containerd.io
```

### Using deb822 Format

```yaml
- hosts: servers
  roles:
    - role: s4int.package_manager
      vars:
        apt_deb822: true
        apt_repositories_custom:
          - name: example
            types: ['deb']
            uris:
              - "https://example.com/repo"
            suites:
              - "{{ ansible_distribution_release }}"
            components: ['main']
```

## Tags

The role supports the following tags for selective execution:

| Tag | Description |
|-----|-------------|
| `package-manager` | Run all tasks |
| `repo` | Repository management tasks |
| `repo-remove` | Remove unmanaged repositories |
| `update` | Update package cache |
| `upgrade` | Upgrade packages |
| `autoremove` | Autoremove unused packages |

### Example Tag Usage

```bash
# Only update repositories
ansible-playbook playbook.yml --tags repo

# Only upgrade packages
ansible-playbook playbook.yml --tags upgrade

# Skip autoremove
ansible-playbook playbook.yml --skip-tags autoremove
```
