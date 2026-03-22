import pytest


def test_yum_repos_dir_exists(host):
    """Verify that the yum.repos.d directory exists."""
    repos_dir = host.file("/etc/yum.repos.d")

    assert repos_dir.exists is True
    assert repos_dir.is_directory is True
    assert repos_dir.user == "root"
    assert repos_dir.group == "root"


def test_dnf_is_installed(host):
    """Verify that dnf is available."""
    dnf = host.package("dnf")

    assert dnf.is_installed is True


@pytest.mark.parametrize(
    "repo_file",
    [
        # Add repository file names here as they are configured
        # Example: "epel.repo"
    ],
)
def test_dnf_repository_file_exists(host, repo_file):
    """Verify that configured repository files exist."""
    f = host.file(f"/etc/yum.repos.d/{repo_file}")

    assert f.exists is True
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


def test_dnf_cache_is_valid(host):
    """Verify that dnf cache can be updated successfully."""
    cmd = host.run("dnf makecache")

    assert cmd.rc == 0


def test_rpm_gpg_keys_directory_exists(host):
    """Verify that the RPM GPG keys directory exists."""
    gpg_dir = host.file("/etc/pki/rpm-gpg")

    assert gpg_dir.exists is True
    assert gpg_dir.is_directory is True
