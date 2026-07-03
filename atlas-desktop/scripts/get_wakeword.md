# Making the "Hey Atlas" wake word

The wake word runs **on your Mac** (Picovoice Porcupine) — no audio leaves the
machine until Atlas is awake. Generating the custom phrase is free and takes ~2 minutes.

## Steps
1. Go to **https://console.picovoice.ai** and sign in (free).
2. Copy your **AccessKey** → paste it into `atlas-desktop/.env` as `PICOVOICE_ACCESS_KEY`.
3. In the console, open **Porcupine → Wake Word**.
4. Type the phrase: **`Hey Atlas`**.
5. Set **Platform = macOS**, then **Train / Download**. You'll get a file like
   `Hey-Atlas_en_mac_v3_0_0.ppn`.
6. Put it here:
   ```
   atlas-desktop/keywords/Hey-Atlas_en_mac.ppn
   ```
   (matching `wake_word.keyword_path` in `config.yaml` — rename it or update the path).

## Don't want to wait?
Until you make the custom word, the app falls back to the built-in keyword set in
`config.yaml` (`builtin_fallback: "jarvis"`). So you can test **right now** by saying
**"Jarvis"** instead of "Hey Atlas". Swap in the custom `.ppn` whenever you're ready.

## Notes
- `.ppn` files are tied to your AccessKey — keep the key in `.env` (git-ignored).
- Retrain if you change the phrasing. You can add multiple keyword files later.
- Sensitivity is tunable in `config.yaml` (`wake_word.sensitivity`): higher catches more
  but false-triggers more.
