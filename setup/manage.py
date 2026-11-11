"""Manage an isolated, repository-local Python environment without pip."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".agentlab"
ENVIRONMENT = STATE / "venv"
MANIFEST = STATE / "manifest.json"
OWNER = "agentlab-local-venv-v1"
TURKISH = {
    "The setup directory is missing or is a symbolic link.": "Kurulum klasörü eksik veya sembolik bağlantı.",
    "No valid ownership marker; nothing will be changed.": "Geçerli sahiplik işaretçisi yok; hiçbir şey değiştirilmeyecek.",
    "The environment is missing or is a symbolic link.": "Ortam eksik veya sembolik bağlantı.",
    "Extra items are present in .agentlab; nothing will be changed.": ".agentlab içinde ek dosyalar var; hiçbir şey değiştirilmeyecek.",
    "The ownership marker cannot be read safely.": "Sahiplik işaretçisi güvenle okunamıyor.",
    "The ownership marker is invalid or belongs to another location.": "Sahiplik işaretçisi geçersiz veya başka bir konuma ait.",
    "The environment was changed; nothing will be deleted or replaced.": "Ortam değiştirilmiş; hiçbir şey silinmeyecek veya değiştirilmeyecek.",
    "Python's venv module is unavailable; review the setup guide.": "Python'un venv modülü kullanılamıyor; kurulum rehberine bakın.",
    "Environment already installed and unchanged.": "AgentLab ortamı zaten kurulu ve değiştirilmemiş.",
    "Setup was interrupted; review .agentlab manually.": "Kurulum yarım kaldı; .agentlab klasörünü kendiniz inceleyin.",
    "Environment installed in .agentlab/venv; no packages were downloaded.": "Ortam .agentlab/venv içine kuruldu; hiçbir paket indirilmedi.",
    "The environment interpreter did not report the expected location.": "Ortamın Python yorumlayıcısı beklenen konumu bildirmedi.",
    "Environment ownership, contents and interpreter verified.": "Ortamın sahipliği, içeriği ve Python yorumlayıcısı doğrulandı.",
    "No environment to remove.": "Kaldırılacak ortam bulunmuyor.",
    "Automatic removal is disabled to protect user files. No files were deleted. Inspect .agentlab and remove it manually only if safe; then rerun install or uninstall.": "Kullanıcı dosyalarını korumak için otomatik kaldırma kapalı. Hiçbir dosya silinmedi. .agentlab klasörünü inceleyin; güvenliyse kendiniz kaldırın ve ardından kurulumu veya kaldırmayı tekrar çalıştırın.",
    "Unchanged AgentLab environment removed.": "Değiştirilmemiş AgentLab ortamı kaldırıldı.",
    "Uninstall was interrupted; correct the problem and run uninstall again. Changed or extra files will be preserved.": "Kaldırma yarım kaldı; sorunu düzeltip kaldırmayı yeniden çalıştırın. Değiştirilmiş veya ek dosyalar korunur.",
    "Uninstall is incomplete; run uninstall again before installing or verifying.": "Kaldırma tamamlanmadı; kurulum veya doğrulama öncesi kaldırmayı yeniden çalıştırın.",
    "The ownership marker contains an unsafe path.": "Sahiplik işaretçisi güvenli olmayan bir yol içeriyor.",
    "An environment directory changed during uninstall.": "Kaldırma sırasında bir ortam klasörü değişti.",
    "An environment link changed during uninstall.": "Kaldırma sırasında bir ortam bağlantısı değişti.",
    "An environment file changed during uninstall.": "Kaldırma sırasında bir ortam dosyası değişti.",
    "An environment item changed during uninstall.": "Kaldırma sırasında bir ortam içeriği değişti.",
}


def translated(message: str) -> str:
    return TURKISH.get(message, message) if os.environ.get("AGENTLAB_LANGUAGE") == "tr" else message


class SetupError(Exception):
    """A setup operation was stopped without touching unowned content."""


def is_link_or_reparse(path: Path) -> bool:
    info = path.lstat()
    return path.is_symlink() or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def snapshot(root: Path) -> dict[str, dict[str, str]]:
    """Record directories, files and links, without following any links."""
    records: dict[str, dict[str, str]] = {}

    def visit(directory: Path) -> None:
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                path = Path(entry.path)
                name = path.relative_to(root).as_posix()
                if entry.is_symlink():
                    records[name] = {"kind": "symlink", "target": os.readlink(path)}
                elif is_link_or_reparse(path):
                    raise SetupError(f"Unsupported reparse point in environment: {path}")
                elif entry.is_dir(follow_symlinks=False):
                    records[name] = {"kind": "directory"}
                    visit(path)
                elif entry.is_file(follow_symlinks=False):
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    records[name] = {"kind": "file", "sha256": digest}
                else:
                    raise SetupError(f"Unsupported item in environment: {path}")

    visit(root)
    return records


def validate_owned(allow_removing: bool = False) -> dict:
    """Refuse to modify a foreign, incomplete, moved or changed installation."""
    if not STATE.is_dir() or is_link_or_reparse(STATE):
        raise SetupError("The setup directory is missing or is a symbolic link.")
    if not MANIFEST.is_file() or is_link_or_reparse(MANIFEST):
        raise SetupError("No valid ownership marker; nothing will be changed.")
    items = {p.name for p in STATE.iterdir()}
    if not items <= {MANIFEST.name, ENVIRONMENT.name}:
        raise SetupError("Extra items are present in .agentlab; nothing will be changed.")
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SetupError("The ownership marker cannot be read safely.") from exc
    if (
        not isinstance(manifest, dict)
        or manifest.get("owner") != OWNER
        or manifest.get("project") != str(ROOT)
        or manifest.get("state") not in {"ready", "removing"}
        or not isinstance(manifest.get("files"), dict)
    ):
        raise SetupError("The ownership marker is invalid or belongs to another location.")
    if manifest["state"] == "removing" and not allow_removing:
        raise SetupError("Uninstall is incomplete; run uninstall again before installing or verifying.")
    if ENVIRONMENT.name not in items:
        if manifest["state"] == "removing" and allow_removing:
            return manifest
        raise SetupError("The environment is missing or is a symbolic link.")
    if not ENVIRONMENT.is_dir() or is_link_or_reparse(ENVIRONMENT):
        raise SetupError("The environment is missing or is a symbolic link.")
    current = snapshot(ENVIRONMENT)
    if any(manifest["files"].get(name) != value for name, value in current.items()) or (
        manifest["state"] == "ready" and current != manifest["files"]
    ):
        raise SetupError("The environment was changed; nothing will be deleted or replaced.")
    return manifest


def install() -> None:
    try:
        import venv
    except ModuleNotFoundError as exc:
        raise SetupError("Python's venv module is unavailable; review the setup guide.") from exc

    if STATE.exists() or STATE.is_symlink():
        validate_owned()
        print(translated("Environment already installed and unchanged."))
        return
    STATE.mkdir()
    # An incomplete installation is deliberately left for manual review on failure.
    MANIFEST.write_text(
        json.dumps({"owner": OWNER, "project": str(ROOT), "state": "creating"}),
        encoding="utf-8",
    )
    try:
        venv.EnvBuilder(with_pip=False, symlinks=False).create(ENVIRONMENT)
        manifest = {
            "owner": OWNER,
            "project": str(ROOT),
            "state": "ready",
            "files": snapshot(ENVIRONMENT),
        }
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SetupError("Setup was interrupted; review .agentlab manually.") from exc
    print(translated("Environment installed in .agentlab/venv; no packages were downloaded."))


def verify() -> None:
    validate_owned()
    executable = ENVIRONMENT / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    result = subprocess.run(
        [str(executable), "-X", "utf8", "-B", "-c", "import sys; print(sys.prefix)"],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    if Path(result.stdout.strip()).resolve() != ENVIRONMENT.resolve():
        raise SetupError("The environment interpreter did not report the expected location.")
    print(translated("Environment ownership, contents and interpreter verified."))


def uninstall() -> None:
    """Never delete by pathname while another process can replace the target."""
    if not STATE.exists() and not STATE.is_symlink():
        print(translated("No environment to remove."))
        return
    raise SetupError(
        "Automatic removal is disabled to protect user files. No files were deleted. "
        "Inspect .agentlab and remove it manually only if safe; then rerun install or uninstall."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "verify", "uninstall"))
    args = parser.parse_args()
    try:
        {"install": install, "verify": verify, "uninstall": uninstall}[args.action]()
    except (OSError, SetupError, subprocess.SubprocessError) as exc:
        prefix = "Kurulum durdu" if os.environ.get("AGENTLAB_LANGUAGE") == "tr" else "Setup stopped"
        print(f"{prefix}: {translated(str(exc))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
