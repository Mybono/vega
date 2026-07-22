# Third-party notices

VEGA is proprietary software, but the app bundles a number of third-party
open-source components. Each of those components is distributed under its own
license, and those licenses continue to apply to the components inside VEGA. This
file acknowledges them.

The table below lists the components known to be bundled, along with the license
each is commonly distributed under. Treat this list as a starting point, not the
final word.

> The entire table is TO BE VERIFIED before public release. License assignments here
> are based on the commonly known license for each project and have not yet been
> confirmed against the exact versions shipped in the build.

## Bundled components

| Component | License |
|:---|:---|
| Python | PSF |
| OpenSSL | Apache-2.0 |
| NumPy | BSD-3-Clause |
| SciPy | BSD-3-Clause |
| MLX | MIT |
| mlx-whisper | MIT |
| OpenAI Whisper model | MIT |
| Numba | BSD-2-Clause |
| llvmlite | BSD-2-Clause |
| huggingface_hub | Apache-2.0 |
| httpx / httpcore | BSD-3-Clause |
| certifi | MPL-2.0 |
| charset-normalizer | MIT |
| regex | Apache-2.0 |
| tiktoken | MIT |
| PyYAML | MIT |
| MarkupSafe | BSD-3-Clause |
| rumps | BSD-3-Clause |
| pynput | LGPL-3.0 |
| sounddevice | MIT |
| pyobjc | MIT |
| pywhispercpp (Windows) | MIT |

## Before public distribution

The authoritative list of components and licenses must be generated from the actual
build environment, not maintained by hand. Run a tool such as `pip-licenses` inside
the build virtual environment to produce it:

```bash
pip-licenses --format=markdown --with-license-file
```

The full license text for every bundled component must be collected and included
with the distribution before VEGA is published. Do not treat this file as complete
until that step is done.
