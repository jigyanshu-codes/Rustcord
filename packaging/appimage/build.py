"""Package the native Linux payload as a Type 2 AppImage; never launch Serein."""

import argparse
import filecmp
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "linux"))
from package import native_elf, stage_payload


def update_metadata(version, release_tag):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version):
        raise ValueError("Expected a semantic application version")
    if release_tag and release_tag != f"v{version}":
        raise ValueError("AppImage release tag must match the application version")
    name = f"rustcord-{release_tag or version}-Linux-X64.AppImage"
    channel = "latest-pre" if "-" in version.split("+", 1)[0] else "latest"
    information = f"gh-releases-zsync|jigyanshu-codes|Rustcord|{channel}|rustcord-*-Linux-X64.AppImage.zsync"
    url = f"https://github.com/jigyanshu-codes/Rustcord/releases/download/v{version}/rustcord-v{version}-Linux-X64.AppImage"
    return name, information, url


def build(root, version):
    native_elf(root)
    if platform.machine() != "x86_64":
        raise ValueError("AppImage releases currently support Linux x86_64 only")
    name, information, url = update_metadata(version, os.environ.get("RUSTCORD_RELEASE_TAG") or os.environ.get("SEREIN_RELEASE_TAG", ""))
    bin_name = "rustcord" if (root / "rustcord").exists() else "serein"
    tools = Path("target/appimage-tools").resolve()
    appimagetool = tools / "appimagetool"
    runtime = tools / "runtime-x86_64"
    if not appimagetool.is_file() or not runtime.is_file():
        raise ValueError("Run bash packaging/appimage/install-tools.sh first")
    if not shutil.which("file"):
        raise ValueError("The 'file' command is required by appimagetool but was not found in PATH")
    if not shutil.which("zsyncmake"):
        raise ValueError("Install zsync to generate AppImage delta-update metadata")
    libraries = subprocess.check_output(["ldd", str(root / bin_name)], text=True)
    if "not found" in libraries:
        raise ValueError(f"Missing host runtime libraries:\n{libraries}")
    with tempfile.TemporaryDirectory(prefix="rustcord-appimage-") as directory:
        temporary = Path(directory)
        appdir = temporary / "RustCord.AppDir"
        stage_payload(root, appdir)
        shutil.copyfile("packaging/appimage/AppRun", appdir / "AppRun")
        (appdir / "AppRun").chmod(0o755)
        desktop_src = Path("packaging/linux/rustcord.desktop") if Path("packaging/linux/rustcord.desktop").exists() else Path("packaging/linux/serein.desktop")
        shutil.copyfile(desktop_src, appdir / f"io.github.{bin_name}.desktop")
        icon_src = Path("packaging/linux/hicolor/256x256/apps/rustcord.png") if Path("packaging/linux/hicolor/256x256/apps/rustcord.png").exists() else Path("packaging/linux/hicolor/256x256/apps/serein.png")
        shutil.copyfile(icon_src, appdir / f"{bin_name}.png")
        shutil.copyfile(icon_src, appdir / ".DirIcon")
        doc = appdir / f"usr/share/doc/{bin_name}"
        shutil.copyfile("packaging/appimage/README.md", doc / "AppImage-README.md")
        shutil.copyfile("packaging/appimage/RUNTIME-LICENSE", doc / "licenses/AppImage-runtime.txt")
        (doc / "AppImage-host-libraries.txt").write_text(libraries, encoding="utf-8")
        subprocess.run(["desktop-file-validate", str(appdir / f"io.github.{bin_name}.desktop")], check=True)
        candidate = temporary / name
        subprocess.run([str(appimagetool), "--runtime-file", str(runtime),
                        "--updateinformation", information, "--file-url", url,
                        "--no-appstream", str(appdir), str(candidate)], check=True, cwd=temporary,
                       env={**os.environ, "ARCH": "x86_64", "VERSION": version,
                            "APPIMAGE_EXTRACT_AND_RUN": "1"})
        with candidate.open("rb") as stream:
            header = stream.read(20)
        if header[:6] != b"\x7fELF\x02\x01" or header[8:11] != b"AI\x02" or header[18:20] != b"\x3e\x00":
            raise ValueError("Expected a Type 2 x86_64 AppImage")
        if candidate.stat().st_size > 512 * 1024 * 1024:
            raise ValueError("AppImage exceeds the in-app updater's 512 MiB limit")
        candidate.chmod(0o755)
        embedded = subprocess.check_output([str(candidate), "--appimage-updateinformation"], text=True)
        if embedded.strip() != information:
            raise ValueError("AppImage update information did not survive packaging")
        zsync = candidate.with_suffix(".AppImage.zsync")
        if not zsync.is_file() or not 0 < zsync.stat().st_size <= 16 * 1024 * 1024:
            raise ValueError("AppImage zsync metadata is missing, empty or oversized")
        # Execute only the pinned AppImage runtime's extraction command, not AppRun
        # or the application. Verify actual output rather than trusting staging.
        subprocess.run([str(candidate), "--appimage-extract"], cwd=temporary,
                       stdout=subprocess.DEVNULL, check=True)
        extracted = temporary / "squashfs-root"
        for source in appdir.rglob("*"):
            if source.is_file():
                target = extracted / source.relative_to(appdir)
                if not target.is_file() or not filecmp.cmp(source, target, shallow=False):
                    raise ValueError(f"AppImage changed payload: {source.relative_to(appdir)}")
        for name in ["AppRun", f"usr/bin/{bin_name}"]:
            if not os.access(extracted / name, os.X_OK):
                raise ValueError(f"AppImage lost executable permission: {name}")
        destination = root / candidate.name
        shutil.copyfile(candidate, destination)
        destination.chmod(0o755)
        shutil.copyfile(zsync, root / zsync.name)
        print(f"Unsigned AppImage: {destination}; host GTK4/WebKit6 runtime required")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staged_directory", type=Path)
    parser.add_argument("application_version")
    args = parser.parse_args()
    build(args.staged_directory.resolve(), args.application_version)
