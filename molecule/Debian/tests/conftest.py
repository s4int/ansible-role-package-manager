import pytest


@pytest.fixture(scope="session")
def os_id(host):
    """Get OS ID from /etc/os-release."""
    cmd = host.run("grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '\"'")
    return cmd.stdout.strip().lower()


def pytest_runtest_setup(item):
    """Skip tests based on OS markers."""
    supported_os = {"debian", "ubuntu"}
    os_markers = supported_os.intersection(m.name for m in item.iter_markers())

    if os_markers:
        host = item.funcargs.get("host")
        if host:
            cmd = host.run("grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '\"'")
            current_os = cmd.stdout.strip().lower()
            if current_os not in os_markers:
                pytest.skip(f"Test requires {os_markers}, running on {current_os}")


@pytest.fixture(scope="session")
def ansible_vars(host):
    """Get Ansible variables."""
    return host.ansible.get_variables()


@pytest.fixture(scope="session")
def apt_repositories(ansible_vars):
    """Get apt repositories from inventory."""
    return ansible_vars.get('apt_repositories_host', [])


def pytest_generate_tests(metafunc):
    """Generate dynamic test parameters from Ansible inventory."""
    if "repo_config" in metafunc.fixturenames:
        # Pobierz host fixture
        host = metafunc.config.pluginmanager.getplugin("testinfra").get_host(
            metafunc.config.option.hosts
        )
        ansible_vars = host.ansible.get_variables()
        repos = ansible_vars.get("apt_repositories_host", [])

        metafunc.parametrize(
            "repo_config", repos, ids=[r.get("name", "") for r in repos]
        )
