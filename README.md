# VEGA

VEGA is a push-to-talk voice dictation tool for macOS and Windows. Hold a hotkey,
speak, release, and your words get typed into whatever app you are using. Speech
recognition runs entirely on your own machine, so your audio never leaves the device.

This repository hosts the installer releases only. It does not contain source code.
VEGA is proprietary software, not open source, and it is free for personal,
non-commercial use. See the [LICENSE](LICENSE) for the full terms.

## Requirements

| Platform | Hardware | OS | Disk |
|:---|:---|:---|:---|
| macOS | Apple Silicon (M1–M4) | macOS 12 or later | ~2 GB free |
| Windows | x86_64 CPU | Windows 10 or later | ~2 GB free |

The macOS build runs speech recognition on the Apple Neural Engine through
mlx-whisper. The Windows build uses whisper.cpp on the CPU. On both platforms the
transcription happens locally.

## Install on macOS

1. Download `VEGA-x.y.z.pkg` from the [Releases page](https://github.com/Mybono/vega/releases).
2. The installer is not yet code-signed, so macOS Gatekeeper will block a normal
   double-click. Right-click the `.pkg` file, choose Open, then click Open again in
   the warning dialog.
3. Follow the installer steps.

After installation VEGA starts on its own and adds a microphone icon to the menu
bar. A setup wizard walks you through the permissions it needs. On first launch it
downloads a Whisper speech model, somewhere between a few hundred megabytes and
about 1.5 GB depending on the model. You need an internet connection for that one
download. After it finishes, dictation works offline.

## Install on Windows

1. Download `vega-windows-x.y.z.zip` from the [Releases page](https://github.com/Mybono/vega/releases).
2. Extract the archive.
3. Double-click `install.bat`.

A tray icon appears once VEGA is running. Grant microphone access when Windows
prompts you.

## Permissions

On macOS, VEGA asks for three permissions during the setup wizard. Each one maps to
a specific job:

- Microphone: records the audio you dictate while the push-to-talk key is held.
- Input Monitoring: detects the global push-to-talk hotkey, even when another app
  is in focus.
- Accessibility: simulates the Cmd+V keystroke to paste the transcribed text into
  the active field.

If you skip a permission, the matching part of VEGA will not work. You can grant
them later in System Settings under Privacy & Security.

On Windows, VEGA only needs microphone access, which it requests on first use.

## Privacy

Your microphone audio never leaves your device. Transcription runs locally, so the
raw audio is never uploaded anywhere. VEGA does make a few other network requests,
such as the one-time model download and update checks, and all of them are listed
in [PRIVACY.md](PRIVACY.md) with the exact destination and timing.

## License

VEGA is proprietary and free for personal, non-commercial use. The full terms are
in [LICENSE](LICENSE). The app bundles third-party open-source components, each
under its own license; those are listed in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
