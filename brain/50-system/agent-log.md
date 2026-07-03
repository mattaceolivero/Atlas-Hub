# Agent Activity Log

Append-only. Every delegation and every self-improvement action gets one line here so the
collective stays accountable and self-aware. Newest at the bottom.

Format: `YYYY-MM-DD | agent | task | outcome`

---

2026-07-03 | Atlas | Hub bootstrapped: charter, 6 specialist agents, 3 skills, brain vault, docs | Foundation committed to branch claude/ai-agent-collective-design-pc1apg
2026-07-03 | Atlas | Roster v2 per Matt: Athena→Vantage (proprietary lead-gen, sole owner of growth); removed Hestia, merged inbox/customer/relations into Hermes (the Messenger = all inbound). Updated charter, agents, skills, docs | Committed
2026-07-03 | Atlas | Authored docs/ATLAS-DESKTOP-PRD.md — hands-free "Hey Atlas" desktop Jarvis app (wake word, VAD, barge-in, HUD visuals, OS/app control) | Committed
2026-07-03 | Atlas | Built atlas-desktop/ v1 per Matt's choices (Mac, Google Chirp, hands-free): Porcupine wake word, Silero VAD, Chirp2 STT + Chirp3-HD TTS, barge-in, continuous conversation, reactive orb HUD, Claude Agent SDK brain. Verified SDK API via claude-code-guide; all modules compile | Committed
2026-07-03 | Atlas | Backend update per Matt: brain uses Claude Code login (no ANTHROPIC_API_KEY); voice switched to Gemini STT+TTS (his key is a Gemini/AIza key) with pluggable provider — google-chirp remains a config flip. Added stt_gemini/tts_gemini, provider switch, updated env/config/docs. NOTE: Matt pasted his Gemini key in chat — advised rotate/restrict; key NOT committed | Committed
