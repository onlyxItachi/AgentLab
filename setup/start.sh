#!/usr/bin/env bash
# Beginner entry point; never installs system software or runs sudo.
set -u

action=install
language=tr
interactive=1
while [ "$#" -gt 0 ]; do
    case "$1" in
        install|verify|uninstall) action=$1 ;;
        --language)
            if [ "$#" -lt 2 ]; then printf '%s\n' 'Missing language / Dil eksik.' >&2; exit 64; fi
            language=$2
            shift ;;
        --non-interactive) interactive=0 ;;
        *) printf 'Unknown option / Bilinmeyen seçenek: %s\n' "$1" >&2; exit 64 ;;
    esac
    shift
done
if [ "$language" != tr ] && [ "$language" != en ]; then
    printf '%s\n' 'Language must be tr or en / Dil tr veya en olmalı.' >&2
    exit 64
fi

say() {
    if [ "$language" = en ]; then printf '%s\n' "$2"; else printf '%s\n' "$1"; fi
}

script_path=${BASH_SOURCE[0]}
case "$OSTYPE" in
    msys*|cygwin*) script_path=${script_path//\\//} ;;
esac
script_dir=${script_path%/*}
if [ "$script_dir" = "$script_path" ]; then script_dir=.; fi
root=$(CDPATH= cd -- "$script_dir/.." && pwd -P) || exit 1
case "$OSTYPE" in
    darwin*) system_name=macOS ;;
    linux*) system_name=Linux ;;
    msys*|cygwin*) system_name='Windows (Git Bash)' ;;
    *) system_name=$OSTYPE ;;
esac
say "Algılanan ortam: $system_name (Bash)." "Detected environment: $system_name (Bash)."

if [ "$action" = uninstall ]; then
    if [ ! -e "$root/.agentlab" ] && [ ! -L "$root/.agentlab" ]; then
        say 'Kaldırılacak AgentLab ortamı bulunmuyor.' 'There is no AgentLab environment to remove.'
        exit 0
    fi
    say "Otomatik kaldırma kapalı; hiçbir dosya silinmedi. $root/.agentlab klasörünü inceleyin, güvenliyse kendiniz kaldırın." \
        "Automatic removal is disabled; no files were deleted. Inspect $root/.agentlab and remove it yourself only if safe."
    say 'Sonra kurulumu veya kaldırmayı tekrar çalıştırabilirsiniz.' \
        'You can then rerun install or uninstall.'
    exit 1
fi

python_bin=
for name in python3 python; do
    candidate=$(type -P "$name" 2>/dev/null || true)
    [ -n "$candidate" ] || continue
    # On macOS, avoid invoking the system stub if it would offer to install developer tools.
    if [[ "$OSTYPE" == darwin* ]] && [ "$candidate" = /usr/bin/python3 ] && \
       ! /usr/bin/xcode-select -p >/dev/null 2>&1; then
        continue
    fi
    if "$candidate" -B -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
        python_bin=$candidate
        break
    fi
done

if [ -z "$python_bin" ]; then
    if [[ "$OSTYPE" == darwin* ]]; then
        url=https://www.python.org/downloads/macos/
        opener=open
    else
        url=https://www.python.org/downloads/
        opener=xdg-open
    fi
    say 'Python 3.10 veya yenisi bulunamadı. Python kurulumunu kendiniz başlatmalısınız.' \
        'Python 3.10 or newer was not found. You must start Python installation yourself.'
    say "Resmî kurulum sayfası: $url" "Official installation page: $url"
    say 'Python kurulduktan sonra terminali kapatıp açın ve bu komutu yeniden çalıştırın.' \
        'After installing Python, restart the terminal and run this command again.'
    if [ "$interactive" -eq 1 ]; then
        if [ "$language" = en ]; then printf 'Open the official page? [y/N] '; else printf 'Resmî sayfa açılsın mı? [e/H] '; fi
        IFS= read -r answer || answer=
        case "$answer" in
            e|E|evet|Evet|y|Y|yes|Yes)
                if command -v "$opener" >/dev/null 2>&1; then
                    "$opener" "$url" >/dev/null 2>&1 || say 'Tarayıcı açılamadı; bağlantıyı elle açın.' 'Could not open the browser; open the link manually.'
                else
                    say 'Tarayıcı otomatik açılamıyor; bağlantıyı elle açın.' 'Cannot open a browser automatically; open the link manually.'
                fi ;;
        esac
    fi
    exit 2
fi

if [ "$action" = install ] && ! "$python_bin" -B -c 'import venv' >/dev/null 2>&1; then
    say 'Python bulundu, ancak venv bileşeni kullanılamıyor. Linux dağıtımınızın resmî yönergelerini izleyin (Debian/Ubuntu: python3-venv).' \
        'Python was found, but venv is unavailable. Follow your Linux distribution’s official instructions (Debian/Ubuntu: python3-venv).'
    say 'Sistem paketini script kurmaz; seçimi ve onayı siz verirsiniz.' \
        'The script does not install system packages; that choice and approval are yours.'
    exit 3
fi

AGENTLAB_LANGUAGE="$language" "$python_bin" -X utf8 -B "$root/setup/manage.py" "$action"
status=$?
if [ "$status" -eq 0 ] && [ "$action" = install ]; then
    AGENTLAB_LANGUAGE="$language" "$python_bin" -X utf8 -B "$root/setup/manage.py" verify
    status=$?
fi
if [ "$status" -ne 0 ]; then
    say 'İşlem durdu. Yukarıdaki ayrıntıları ve kurulum rehberini inceleyin.' \
        'The operation stopped. Review the details above and the setup guide.'
fi
exit "$status"
