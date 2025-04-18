# Setup and Build Guide for WhatsApp Bot

This guide explains how to set up the environment, install dependencies, run the application from source, and build a standalone executable for the WhatsApp Bot.

## Prerequisites

1.  **Python:** Python 3.8 or newer is recommended. Download from [python.org](https://www.python.org/). Ensure Python and Pip are added to your system's PATH during installation.
2.  **Git (Optional):** If you need to clone the repository. Download from [git-scm.com](https://git-scm.com/).
3.  **Project Files:** You need the project source code (`gui.py`, `bot.py`, `requirements.txt`, etc.).
4.  **Icon Files:**
    *   `icon.png`: The source icon file used by the GUI.
    *   `icon.ico`: An icon file converted from `icon.png` (required for the Windows executable build). Place this in the project's root directory.
5.  **Contacts File:**
    *   `contacts.csv`: A CSV file containing the contacts. It **must** have a column named `phone_number` with numbers in international format (e.g., `+1234567890`).
    *   An optional `name` column can be included for personalization (using `[Name]` in the message).
    *   Example `contacts.csv`:
        ```csv
        phone_number,name
        +19998887777,Alice
        +5511987654321,Bob
        +442071234567,Charlie
        ```

## Setup Steps

1.  **Open Terminal:** Open a terminal or command prompt in the project's root directory (`whats-web-kit`).

2.  **Create Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    ```

3.  **Activate Virtual Environment:**
    *   **Windows (Command Prompt):**
        ```cmd
        .venv\Scripts\activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
        (If you get an execution policy error, you might need to run PowerShell as Administrator and execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, then try activating again).
    *   **macOS / Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *(You should see `(.venv)` at the beginning of your terminal prompt)*.

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application from Source

Once the setup is complete, you can run the GUI directly:

```bash
python gui.py
```

## Building the Executable (Windows)

This process uses PyInstaller to bundle the application and its dependencies into a distributable format.

1.  **Ensure Prerequisites:** Make sure `icon.ico` is present in the project root directory.
2.  **Run PyInstaller:** Execute the following command in your terminal (with the virtual environment activated):
    ```bash
    pyinstaller --windowed --name gui --icon="icon.ico" --add-data="icon.png;." --noconfirm gui.py
    ```
    *   `--windowed`: Creates a GUI application without a console window.
    *   `--name gui`: Define o nome do executável resultante (`gui.exe`).
    *   `--icon="icon.ico"`: Sets the executable's icon. **Requer um arquivo `icon.ico`**.
    *   `--add-data="icon.png;."`: Bundles the `icon.png` needed by the GUI. Note the `;` separator used on Windows.
    *   `--noconfirm`: Pula as confirmações de sobrescrever pastas `dist` e `build`.
    *   `gui.py`: Specifies the main script.

3.  **Output:** PyInstaller will create a `build` folder and a `dist` folder. Your application will be inside `dist/gui/`.

## Building the Executable (macOS)

This process uses PyInstaller to bundle the application and its dependencies into a distributable macOS application bundle (`.app`).

1.  **Ensure Prerequisites:**
    *   Make sure you have an `icon.icns` file in the project root directory. You might need to convert your `icon.png` file to the `.icns` format using online tools or macOS utilities like `iconutil`.
    *   Ensure `icon.png` is also present in the project root directory (for the window icon).
2.  **Run PyInstaller:** Execute the following command in your terminal (with the virtual environment activated):
    ```bash
    pyinstaller --windowed --name gui --icon="icon.icns" --add-data="icon.png:." --noconfirm gui.py
    ```
    *   `--windowed`: Creates a standard macOS GUI application bundle.
    *   `--name gui`: Define o nome do aplicativo resultante (`gui.app`).
    *   `--icon="icon.icns"`: Sets the application bundle's icon (shown in Finder). **Requer o arquivo `icon.icns`**.
    *   `--add-data="icon.png:."`: Bundles the `icon.png` needed by the GUI code to set the window's title bar icon. Note the `:` separator used on macOS/Linux.
    *   `--noconfirm`: Pula as confirmações de sobrescrever pastas `dist` e `build`.
    *   `gui.py`: Specifies the main script.

3.  **Output:** PyInstaller will create a `build` folder and a `dist` folder. Your application bundle (`gui.app`) will be inside the `dist/` folder.

## Running the Built Executable

1.  Navigate to the `dist/` folder (macOS) or `dist/gui/` folder (Windows).
2.  Double-click `gui.app` (macOS) or `gui.exe` (Windows) to run the application.
3.  You can drag `gui.app` to your Applications folder on macOS, or create a shortcut to `gui.exe` on Windows for easier access.

## Uninstalling the Application

If you wish to remove the application and its related components, you can use the provided uninstall scripts. These scripts aim to remove the built application, the virtual environment, and other generated files.

**Important:** Close the application and deactivate the virtual environment (if active, type `deactivate` in the terminal) before running the uninstall script.

1.  **Open Terminal:** Open a terminal or command prompt in the project's root directory (`whats-web-kit`).

2.  **Run the appropriate script:**

    *   **Windows:**
        ```cmd
        uninstall.bat
        ```

    *   **macOS / Linux:**
        *   First, make the script executable (you only need to do this once):
          ```bash
          chmod +x uninstall.sh
          ```
        *   Then, run the script:
          ```bash
          ./uninstall.sh
          ```

3.  **Manual Cleanup (Optional):** The scripts attempt to remove most components. You might want to manually delete the entire project folder (`whats-web-kit`) if you no longer need the source code or any remaining configuration files. 