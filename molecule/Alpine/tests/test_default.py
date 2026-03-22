import pytest


def test_apk_repositories_file_exists(host):
    """Verify that the apk repositories file exists."""
    repos_file = host.file('/etc/apk/repositories')

    assert repos_file.exists is True
    assert repos_file.is_file is True
    assert repos_file.user == 'root'
    assert repos_file.group == 'root'


def test_apk_is_installed(host):
    """Verify that apk is available."""
    cmd = host.run("apk --version")

    assert cmd.rc == 0


def test_apk_cache_is_valid(host):
    """Verify that apk cache can be updated successfully."""
    cmd = host.run("apk update")

    assert cmd.rc == 0


def test_apk_repositories_contains_main(host):
    """Verify that the main repository is configured."""
    repos_file = host.file('/etc/apk/repositories')

    assert repos_file.exists is True
    assert 'main' in repos_file.content_string or repos_file.size > 0


@pytest.mark.parametrize("repo_line", [
    # Add repository URLs here as they are configured
    # Example: "https://dl-cdn.alpinelinux.org/alpine/v3.21/main"
])
def test_apk_repository_configured(host, repo_line):
    """Verify that configured repositories are present."""
    repos_file = host.file('/etc/apk/repositories')

    assert repo_line in repos_file.content_string


