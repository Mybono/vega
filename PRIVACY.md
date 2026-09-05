# Privacy Policy

**Last updated:** 2026-08-29 · Applies to the VEGA desktop app for macOS and Windows.

This describes what VEGA does with your data. It is written against the code, not around it — every
claim below corresponds to something you can find in this repository, and the technical detail
behind it is in [SECURITY.md](SECURITY.md).

## The short version

**Your speech never leaves your computer.** Dictation is transcribed on-device by a local Whisper
model. No audio, and no transcript of dictated text, is ever uploaded — there is no server to upload
it to.

Things do leave your computer in three cases, all of which you control:

1. **You sign in.** Your Google account's basic profile goes to our database so we know which plan
   you're on.
2. **You use a voice command that needs the internet** — weather, a web search, currency rates. The
   words of *that command* go to the service that answers it.
3. **You configure a cloud AI provider.** Commands are then processed by OpenAI or Anthropic, under
   your own account and your own API key.

Ordinary dictation involves none of these.

## What stays on your computer, always

| Data | Where | Kept until |
| :--- | :---- | :--------- |
| Audio you dictate | In memory during recording | Discarded as soon as it is transcribed — never written to disk |
| The transcribed text | Pasted at your cursor | Not stored by VEGA |
| Your settings (languages, hotkeys, microphone) | `vega-config.json` | You change them, or uninstall |
| Your OpenAI/Anthropic API keys | The macOS Keychain or Windows DPAPI — **never** in a plain file | You remove them, or uninstall |
| Your sign-in session | `session.json`, readable only by your user account | You sign out, or uninstall |
| Daily dictation time (a number, for plan limits) | `usage.json` | Reset daily; removed on uninstall |
| The app log | `vega.log` | **Cleared once a day**, and removed on uninstall |

The log records what VEGA did — which mode was active, how long transcription took, which command
route was taken — but **not what you said**. Text is written as a length (`<34 chars>`), never
verbatim. If you are diagnosing a problem and want the actual text in the log, you can opt in for
that session by setting `VEGA_LOG_TRANSCRIPTS=1`; it is off unless you set it.

The Whisper speech model is downloaded once from Hugging Face and then runs entirely offline. The
download tells Hugging Face your IP address, like any file download.

## What leaves your computer, and when

### If you sign in with Google

VEGA uses Google's standard sign-in. We receive, and store in Google Firestore:

- your Google account id, email address, display name and profile photo URL;
- your plan, trial length, and the timestamps of account creation and last sign-in;
- which platform you're on (macOS or Windows).

That is the whole record. We use it only to know who you are and what you've paid for. **You can use
dictation without signing in.**

### If you use a voice command that needs the internet

Only the command you spoke is sent, only to the service that answers it, and only when you use that
command:

| Command | Goes to |
| :------ | :------ |
| Weather | `open-meteo.com` (place name, then coordinates) |
| Web search | `duckduckgo.com`; opening results uses `google.com` / `youtube.com` |
| Currency rates | `frankfurter.dev` |
| Crypto prices | `coingecko.com` |

These are third-party services with their own privacy policies. VEGA sends no account identifier
with these requests.

### If you configure a cloud AI provider

By default, voice commands are interpreted by **Ollama running on your own machine** — nothing
leaves the computer. If you enter an OpenAI or Anthropic API key, command text is sent to
`api.openai.com` or `api.anthropic.com` instead, billed to your own account and governed by that
provider's terms. Remove the key and it stops.

### Always

VEGA checks GitHub for a new release, and (if you're signed in) reads your plan from Firestore.
Neither request carries your speech or your files.

### If VEGA crashes

VEGA sends us a crash report. It contains the error, where in the code it happened (file, line and
function — never the values your program was working with), the app version, your OS version, and
the last few lines the speech engine printed while failing. That is the whole report.

It cannot contain what you said: the reporter never reads the log or any transcript, and the
paths in it are rewritten so your home folder — which usually contains your name — does not travel
with it. Every report is also written to a file on your computer, so you can see exactly what would
be sent.

Crash reports are what let us fix a build that fails only on real machines. If you would rather not
send them, turn off **Privacy & Terms → Send Crash Reports** in the menu; everything else keeps
working. Reports are write-only on our side — nobody can read back, change or delete a filed report.

If you want to help diagnose a crash, you can email a saved report to **<mavoxlabs@gmail.com>** and
attach `vega.log` from the same machine. That is entirely your choice and it is a separate act from the
automatic report above: VEGA never attaches the log itself. Read both files before you send them —
the log holds no dictated text unless you ran that session with `VEGA_LOG_TRANSCRIPTS=1`, in which
case it holds exactly what you said.

## What VEGA never does

- Never uploads audio.
- Never uploads transcripts of dictated text.
- Never reads your screen, files, or clipboard except when a command you spoke asks it to, and only
  in that moment.
- No usage analytics, no behavioural tracking, no advertising identifiers, no third-party trackers.
  The crash report described above is the only thing VEGA sends on its own, and you can turn it off.
- Never sells or shares personal data with anyone beyond the services listed above.

## Permissions VEGA asks for, and why

| Permission | Why |
| :--------- | :-- |
| Microphone | To hear what you dictate |
| Input Monitoring | To notice the hotkey you hold, while other apps are focused |
| Accessibility | To paste the transcribed text at your cursor |
| Screen Recording (optional) | Only for the screenshot and on-screen-text commands |

Uninstalling resets all of these.

## Deleting your data

**On your computer:** the app's own **Uninstall…** removes every local trace — settings, session and
refresh token, API keys from the OS keystore, entitlement cache, usage counters, the log, saved crash
reports, the downloaded speech model (if you choose to), and the app itself, and resets its system permissions.

**Our database:** signing out removes your session locally but leaves the account record. To have
the record deleted, open a request at
[github.com/Mybono/vega/issues](https://github.com/Mybono/vega/issues) or email
**<mavoxlabs@gmail.com>** from the address you signed up with; it is deleted within 30 days. The app
itself cannot delete it — the security rules deliberately forbid clients from deleting account records, so
the request goes through us.

Under GDPR (EEA/UK) and CCPA (California) you may also request a copy of what we hold, ask for it to
be corrected, or object to processing. Same route, same 30 days.

## Children

VEGA is not directed at children under 13 and we do not knowingly collect their data.

## Changes

Material changes will be announced in the release notes and reflected in the "Last updated" date
above. The published history of this file lives in the repository, so you can see exactly what
changed and when.

## Contact

**<mavoxlabs@gmail.com>** is the official mailbox. Privacy questions, data-deletion and data-access
requests, support and crash reports all reach us there.
