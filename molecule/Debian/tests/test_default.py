import pytest


def test_apt_sources_list_dir_exists(host):
    """Verify that the apt sources.list.d directory exists."""
    sources_dir = host.file("/etc/apt/sources.list.d")

    assert sources_dir.exists is True
    assert sources_dir.is_directory is True
    assert sources_dir.user == "root"
    assert sources_dir.group == "root"


def test_apt_keyrings_dir_exists(host):
    """Verify that the apt keyrings directory exists."""
    keyrings_dir = host.file("/etc/apt/keyrings")
    if not keyrings_dir.exists:
        pytest.skip("keyrings directory does not exist")

    assert keyrings_dir.exists is True
    assert keyrings_dir.is_directory is True
    assert keyrings_dir.user == "root"
    assert keyrings_dir.group == "root"


@pytest.mark.parametrize(
    "repo_file",
    [
        # Add repository file names here as they are configured
        # Example: "docker.list", "docker.sources"
    ],
)
def test_apt_repository_file_exists(host, repo_file):
    """Verify that configured repository files exist."""
    f = host.file(f"/etc/apt/sources.list.d/{repo_file}")

    assert f.exists is True
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


def test_apt_cache_is_valid(host):
    """Verify that apt cache can be updated successfully."""
    cmd = host.run("apt-get update")

    assert cmd.rc == 0


def test_apt_repository_sources_files_valid(host):
    """Verify that all .list repository files in sources.list.d are valid."""
    sources_dir = host.file("/etc/apt/sources.list.d")
    if not sources_dir.exists:
        pytest.skip("sources.list.d directory does not exist")

    # Find all .list files
    cmd = host.run("find /etc/apt/sources.list.d -name '*.list' -type f 2>/dev/null")
    if cmd.rc != 0 or not cmd.stdout.strip():
        pytest.skip("No .list repository files found")

    for repo_file_path in cmd.stdout.strip().split("\n"):
        if repo_file_path:
            repo_file = host.file(repo_file_path)
            assert repo_file.exists is True, (
                f"Repository file {repo_file_path} should exist"
            )
            assert repo_file.user == "root", (
                f"Repository file {repo_file_path} should be owned by root"
            )
            assert repo_file.group == "root", (
                f"Repository file {repo_file_path} should have root group"
            )
            assert repo_file.mode == 0o644, (
                f"Repository file {repo_file_path} should have 644 permissions"
            )
            # Verify file is not empty
            assert repo_file.size > 0, (
                f"Repository file {repo_file_path} should not be empty"
            )


def test_apt_repository_deb822_files_valid(host):
    """Verify that all .sources (deb822 format) repository files are valid."""
    sources_dir = host.file("/etc/apt/sources.list.d")
    if not sources_dir.exists:
        pytest.skip("sources.list.d directory does not exist")

    # Find all .sources files (deb822 format)
    cmd = host.run("find /etc/apt/sources.list.d -name '*.sources' -type f 2>/dev/null")
    if cmd.rc != 0 or not cmd.stdout.strip():
        pytest.skip("No .sources (deb822) repository files found")

    for repo_file_path in cmd.stdout.strip().split("\n"):
        if repo_file_path:
            repo_file = host.file(repo_file_path)
            assert repo_file.exists is True, (
                f"Repository file {repo_file_path} should exist"
            )
            assert repo_file.user == "root", (
                f"Repository file {repo_file_path} should be owned by root"
            )
            assert repo_file.group == "root", (
                f"Repository file {repo_file_path} should have root group"
            )
            assert repo_file.mode == 0o644, (
                f"Repository file {repo_file_path} should have 644 permissions"
            )
            # Verify file is not empty
            assert repo_file.size > 0, (
                f"Repository file {repo_file_path} should not be empty"
            )
            # Verify deb822 format contains required fields
            content = repo_file.content_string
            assert "URIs:" in content or "Types:" in content, (
                f"Repository file {repo_file_path} should contain valid deb822 format"
            )


def test_apt_repository_keyring_files_valid(host):
    """Verify that GPG keyring files for repositories exist and are valid."""
    keyrings_dir = host.file("/etc/apt/keyrings")
    if not keyrings_dir.exists:
        pytest.skip("keyrings directory does not exist")

    # Find all keyring files (gpg, asc, key extensions)
    cmd = host.run(
        "find /etc/apt/keyrings -type f \\( -name '*.gpg' -o -name '*.asc' -o -name '*.key' \\) 2>/dev/null"
    )
    if cmd.rc != 0 or not cmd.stdout.strip():
        pytest.skip("No keyring files found")

    for keyring_path in cmd.stdout.strip().split("\n"):
        if keyring_path:
            keyring_file = host.file(keyring_path)
            assert keyring_file.exists is True, (
                f"Keyring file {keyring_path} should exist"
            )
            assert keyring_file.user == "root", (
                f"Keyring file {keyring_path} should be owned by root"
            )
            assert keyring_file.size > 0, (
                f"Keyring file {keyring_path} should not be empty"
            )
