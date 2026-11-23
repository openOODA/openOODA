# privacy.md — Privacy, Redaction & Zero-Telemetry Quick Card (`ooda privacy`)

1. **Kernel/Runtime Privacy Attenuation (`ooda-standard/sec/capreg.oo:oo_cap_privacy_attenuate`)**:
   - Forces Rights8 masks `64` (`RIGHT_PRIVACY_REDACT`) and `128` (`RIGHT_ZERO_TELEMETRY`) immutable/sealed on child capability registers.
   - Strips exfiltration & capture capabilities from untrusted children: clears `NetCap(0)`, `MetricsCap(11)`, `TcpCap(17)`, `UdpCap(18)`, `AudioCap(20)`, `CameraCap(21)`, `HidCap(23)`, and `FrameCap(25)`.

2. **Stream, Taint & Metadata Redaction (`@openOODA-system/ooda-vault` & `@openOODA-apps/ooda-camera`)**:
   - **Static & Dynamic IFC Taint (`SECRET:`)**: Values tagged `SECRET:` cannot flow to unencrypted network, log, or `process_exec` sinks.
   - **`ooda-vault`** (`redact`, `taint`, `guard`, `prompt-filter`, `pii`, `exif`): Scrubs PEM private keys, bearer/API tokens, PII, and prompt-injection payloads from streams and agent logs.
   - **Default EXIF/GPS Stripping (`ooda-camera` & `ooda-media`)**: Strips GPS coordinates, serial numbers, and device timestamps on capture/export by default.

3. **Hardware Privacy LED & Desktop Portal Gates (`@openOODA-system/ooda-compositor` & `ooda-portal`)**:
   - **Camera & Mic LED Gate (`ooda_compositor_seat_privacy_gate`)**: Refuses capture unless `CameraCap`/`AudioCap` is held AND the hardware privacy indicator LED is armed (`return 2`).
   - **Screen Share Blackout (`ooda_compositor_net_stream_gated`)**: Automatically blacks out windows tagged `PRIVACY_BLACKOUT` during screen recording/casting.
   - **Clipboard Auto-Burn (`ooda-portal/core/clip/ttl_burn.oo`)**: `PRIVACY_BLACKOUT` copies expire after **1 paste or 30 seconds** (default: 64 pastes / 3600s) and zeroize RAM.

4. **Canonical Local-First Feedback & Opt-In Interaction Journal (`ooda-standard v2.14.0`)**:
   - **Default-OFF Interaction Journal**: Controlled fail-closed by `~/.openooda/config/feedback.oot` (`journal_enabled=0` by default; toggled in `ooda-settings` Privacy & Caps or `<app> feedback journal on|off|clear`).
   - **Strictly Anonymous `OOFEEDBACK 1` Bundles**: Maximum 16 KB, SHA-256 sealed (`~/.openooda/feedback/*.oot`); zero contact fields, zero raw keystrokes, zero unguarded background network calls.
   - **Mandatory Scrubbing & Capabilities**: `fb_scrub_text` redacts home paths, emails, IPv4, PEM/API/bearer tokens, ANSI controls, and `SECRET:` lines before saving or opening GitHub Issue/Discussion URLs under `RIGHT_PRIVACY_REDACT | RIGHT_ZERO_TELEMETRY`.
