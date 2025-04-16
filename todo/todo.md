# WhatsApp Messaging Bot TODO List

This list outlines the steps to create a Python script and client application for sending WhatsApp messages.

## Phase 1: Core WhatsApp Bot Logic (Python Script)
- [ ] Research and choose a WhatsApp Web automation library (e.g., `pywhatkit`, `selenium`).
- [ ] Set up the Python development environment and install necessary libraries.
- [ ] Implement basic browser control: opening WhatsApp Web, handling QR code scan.
- [ ] Implement sending a message to a single hardcoded contact.
- [ ] Define contact file format (e.g., CSV, JSON) and implement reading contacts from it.
- [ ] Implement iterating through the contact list and sending messages.
- [ ] Implement basic logging: record sent status, recipient, timestamp.
- [ ] Research how to reliably get message IDs (Note: This might be difficult or unstable with web automation).
- [ ] Implement logging with message IDs if feasible.
- [ ] Implement basic error handling (e.g., contact not found, browser closed unexpectedly).
- [ ] Add delays between messages to avoid being flagged as spam.
- [ ] Implement browser closing after sending all messages.

## Phase 2: Client Application (GUI)
- [ ] Research and choose a cross-platform GUI library (e.g., `Tkinter`, `CustomTkinter`, `PyQt`, `Kivy`).
- [ ] Design the user interface:
    - [ ] Button to select contact file.
    - [ ] Display selected file path.
    - [ ] Start/Stop buttons for the sending process.
    - [ ] Status display area (e.g., "Sending to X...", "Finished", "Error...").
    - [ ] Log display area.
- [ ] Implement the GUI layout.
- [ ] Connect GUI elements to the core bot functions (file selection, start/stop).
- [ ] Display script progress and logs in the GUI.
- [ ] Ensure the GUI runs the bot logic in a separate thread to avoid freezing.

## Phase 3: Packaging and Distribution
- [ ] Research packaging tools (e.g., `pyinstaller`, `cx_Freeze`, `py2app`).
- [ ] Configure the packaging tool to bundle the script, GUI, and dependencies.
- [ ] Create executable for Windows.
- [ ] Create application bundle for macOS.
- [ ] Test executables on target platforms (Windows, macOS).

## Phase 4: Refinements and Documentation
- [ ] Add configuration options (e.g., message delay, path to browser driver if using Selenium).
- [ ] Improve error handling and reporting in the GUI.
- [ ] Enhance logging details.
- [ ] Write a `README.md` file with setup and usage instructions.
- [ ] Add comments to the code for maintainability.
- [ ] Consider security implications (handling WhatsApp session, storing credentials).
