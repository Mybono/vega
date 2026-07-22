# Privacy

**Your audio never leaves your device.**

VEGA transcribes speech locally. On macOS it runs mlx-whisper on the Apple Neural
Engine; on Windows it runs whisper.cpp on the CPU. Either way, the recorded audio
stays on your machine and is turned into text there.

There is one exception to being fully offline, and it happens only once. On first
launch VEGA downloads a Whisper speech model. After that download completes,
dictation works with no network connection at all. Turn off Wi-Fi and it keeps
working.

VEGA is not a fully airgapped app, and pretending otherwise would be dishonest.
It makes a handful of network requests for things like update checks and voice
commands. Here is the complete list of where data goes and when.

## Network egress

| What | Destination | When |
|:---|:---|:---|
| Microphone audio | NOWHERE — transcription is fully on-device | always |
| Whisper model download | huggingface.co | once, first launch |
| Update check | api.github.com/repos/Mybono/vega | periodically |
| Voice-command text (transcribed TEXT, not audio) → LLM | http://localhost:11434 (local Ollama) BY DEFAULT | when a voice command is issued |
| Voice-command text → cloud LLM | api.openai.com or api.anthropic.com | ONLY if the user has entered their own API key (llm_provider set to openai/anthropic; default is "local") |
| Command execution queries | duckduckgo.com (search), open-meteo.com (weather), frankfurter.dev (currency), coingecko.com (crypto) | only when that specific command is used |

## Voice commands

Voice commands are the one place where text you spoke can be sent off the device,
so it is worth being precise about what does and does not happen.

When you issue a voice command, VEGA transcribes your speech to text on-device,
then sends that text to a language model to interpret it. The audio itself is never
sent. Only the transcribed text is.

By default that language model is a local Ollama instance at
`http://localhost:11434`, which runs on your own machine. Nothing leaves the device
in that case.

If you choose to use a cloud provider instead, you have to enter your own API key
and set `llm_provider` to `openai` or `anthropic`. Only then does the transcribed
text go to `api.openai.com` or `api.anthropic.com`. The default is `local`, so this
is opt-in and never happens unless you set it up yourself.

Individual commands may also reach specific services to do their work: a web search
hits duckduckgo.com, a weather lookup hits open-meteo.com, a currency conversion
hits frankfurter.dev, and a crypto price check hits coingecko.com. These only fire
when you run that particular command.

## Verify it yourself

You do not have to take any of this on faith. Here are three checks you can run.

1. Pull the network. Turn off Wi-Fi (after the first-launch model download) and
   dictate something. It still works, because transcription is local.
2. Watch the connections. See exactly which hosts the process talks to:

   ```bash
   sudo nettop -p "$(pgrep -x Vega)"
   ```

   Or list open network files for the process:

   ```bash
   sudo lsof -nP -i -a -p "$(pgrep -x Vega)"
   ```

3. Inspect the request bodies. Route VEGA through mitmproxy by setting proxy
   environment variables, then read the traffic:

   ```bash
   export HTTPS_PROXY=http://127.0.0.1:8080
   export HTTP_PROXY=http://127.0.0.1:8080
   ```

   You will see that outgoing request bodies contain text, never audio.
