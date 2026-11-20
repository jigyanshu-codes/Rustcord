"""Check and synchronize upstream updates from ViceVerse-cz/Serein while preserving RustCord branding."""

import os
import subprocess
import sys
from pathlib import Path


def run(*args, cwd=None, check=True):
    print(f"Running: {' '.join(str(a) for a in args)}")
    return subprocess.run(args, cwd=cwd, check=check, text=True, capture_output=True)


def output(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


PRESERVED_PATHS = [
    "README.md",
    "docs/logo.png",
    "packaging/linux/rustcord.desktop",
    "packaging/linux/package.py",
    "packaging/appimage/build.py",
    "packaging/repositories/build.py",
    "packaging/repositories/test_build.py",
    ".github/workflows/ci.yml",
    ".github/workflows/linux-packages.yml",
    ".github/workflows/sync-upstream.yml",
    "packaging/windows/installer.nsi",
    "packaging/windows/rustcord.rc",
    "packaging/windows/Rustcord.ico",
    "packaging/windows/rustcord.png",
    "packaging/windows/setup.ps1",
    "packaging/windows/install-notifications.ps1",
    "crates/ui/src/icons.rs",
]


def main():
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)

    # 1. Ensure upstream remote exists
    remotes = output("git", "remote").splitlines()
    if "upstream" not in remotes:
        run("git", "remote", "add", "upstream", "https://github.com/ViceVerse-cz/Serein.git")
    else:
        run("git", "remote", "set-url", "upstream", "https://github.com/ViceVerse-cz/Serein.git")

    # 2. Fetch upstream main
    print("Fetching upstream Serein changes...")
    run("git", "fetch", "upstream", "main")

    # 3. Check if there are new commits in upstream
    new_commits = output("git", "log", "HEAD..upstream/main", "--oneline")
    if not new_commits.strip():
        print("RustCord is already completely up to date with upstream Serein. Nothing to sync.")
        # Clean up temporary upstream remote if needed, or leave it
        return 0

    print("Found new commits from upstream Serein:")
    print(new_commits)

    # 4. Backup preserved branding files in memory
    backups = {}
    for rel_path in PRESERVED_PATHS:
        file_path = root / rel_path
        if file_path.is_file():
            backups[rel_path] = file_path.read_bytes()

    # Also backup all rustcord icons in hicolor
    hicolor_dir = root / "packaging/linux/hicolor"
    if hicolor_dir.is_dir():
        for icon_path in hicolor_dir.rglob("*rustcord*"):
            if icon_path.is_file():
                backups[icon_path.relative_to(root).as_posix()] = icon_path.read_bytes()

    # 5. Attempt merge
    print("Merging upstream changes...")
    merge_res = run(
        "git", "merge", "upstream/main", "-m", "chore(sync): merge upstream updates from ViceVerse-cz/Serein",
        check=False
    )

    # 6. Restore our preserved branding files regardless of merge result
    for rel_path, data in backups.items():
        dest = root / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    # Ensure apps/desktop/Cargo.toml has package name = rustcord
    cargo_desktop = root / "apps/desktop/Cargo.toml"
    if cargo_desktop.is_file():
        content = cargo_desktop.read_text(encoding="utf-8")
        if 'name = "serein"' in content:
            content = content.replace('name = "serein"', 'name = "rustcord"')
            cargo_desktop.write_text(content, encoding="utf-8")

    # 7. Complete merge if there were conflicts or changes
    status = output("git", "status", "--porcelain")
    if status.strip():
        run("git", "add", "-A")
        if (root / ".git/MERGE_HEAD").exists():
            run("git", "commit", "-m", "chore(sync): merge upstream updates preserving RustCord branding")
        else:
            run("git", "commit", "-m", "chore(sync): preserve RustCord branding after upstream sync")

    # 8. Push to origin main if GITHUB_ACTIONS is set
    if os.environ.get("GITHUB_ACTIONS"):
        print("Pushing synchronized changes to origin/main...")
        run("git", "push", "origin", "main")
        print("Synchronization complete and pushed successfully!")
    else:
        print("Local dry-run/check finished successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
