# First-time setup for beginners

[Home](../README.en.md) | [Türkçe](README.md)

This guide is for people who have never installed Python or development tools. Before copying a command, follow the steps below to open the **AgentLab folder**. This first example requires Python 3.10 or newer; it does not require Git, a GPU, an API key, or a paid account.

## 1. Get the files and open the folder

Download the AgentLab folder shared by your instructor and extract it if it is compressed. You can also use **Code → Download ZIP** on GitHub. Open the folder containing `README.md` and the `setup` directory.

- **Windows:** With that folder open in File Explorer, type `powershell` in the address bar and press Enter.
- **macOS:** Open Terminal, type `cd `, drag the AgentLab folder from Finder into the window, and press Enter.
- **Linux:** Open the AgentLab folder in your file manager and choose “Open in Terminal”, or type `cd ` in a terminal and drag the folder into the window.

## 2. Start setup

**Windows PowerShell:** Use this path on Windows. Running `start.sh` through Git Bash may trigger automatic installation with some Python launchers.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action install -Language en
```

This command changes the execution policy only for the PowerShell process it starts; it does not change the computer's persistent policy. If an organization policy blocks it, consult your administrator.

**macOS or Linux terminal:**

```bash
bash setup/start.sh install --language en
```

The script checks for Python and its required `venv` module. If Python is missing, it displays the official download page and asks before opening it. You choose whether to download and install Python; the script does not automatically download software, perform system installation, or run `sudo`. An installer may ask to make system-wide changes; review its request before approving it. After installation, restart the terminal and run the same AgentLab command again.

On Windows, if the downloaded application installed only the **Python Install Manager**, you must also install a Python runtime. For example, in a new PowerShell window you can choose to run `py install 3.11` yourself for the Python version exercised in CI, and review the installer's steps. Then rerun the AgentLab setup command.

On Debian/Ubuntu, if Python is present but `venv` is missing, consult your distribution's official package instructions and install `python3-venv` yourself if appropriate. This can change system packages and requires your approval.

When suitable Python is found, the script creates and verifies a project-owned virtual environment in `.agentlab/venv`. It downloads no packages or models. Running the install command again preserves and re-verifies the existing environment if it is unchanged.

## 3. Verify and try the demo

**Windows PowerShell:**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action verify -Language en
.\.agentlab\venv\Scripts\python.exe sessions/01-llm-fundamentals/demos/structured-output/demo.py --term token --language en
```

**macOS or Linux:**

```bash
bash setup/start.sh verify --language en
.agentlab/venv/bin/python sessions/01-llm-fundamentals/demos/structured-output/demo.py --term token --language en
```

See the [tool and structured output example](../sessions/01-llm-fundamentals/demos/structured-output/README.en.md) for an explanation. The demo does not call a real AI model.

## 4. Remove the environment safely

Automatic removal is disabled because it cannot reliably distinguish concurrent file replacements. If `.agentlab` exists, the uninstall command deletes nothing, explains the situation, and stops with exit code 1; Python is not required. If the folder is absent, it succeeds.

1. Close AgentLab demos and programs using the environment.
2. Find **`.agentlab`** in the AgentLab project folder. If it is hidden, show hidden items: use **View → Hidden items** in Windows File Explorer, or **Command + Shift + .** in macOS Finder.
3. Inspect its contents. Preserve or copy your own files and anything you are unsure about before deciding. If you do not want to remove the whole folder, do not run an automatic cleanup.
4. Only if you are certain its contents can be removed, move `.agentlab` to the Trash or Recycle Bin yourself. This does not remove a separately installed system Python.
5. After removing the folder, `bash setup/start.sh uninstall --language en` or, on Windows, `powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action uninstall -Language en` reports that the environment is absent. You may then install again.

If an older uninstall was interrupted, its `removing` marker and remaining files are preserved. Follow the same inspection and manual removal steps. Until the folder is removed, install and verify stop with recovery guidance; after removal, installation works again.
