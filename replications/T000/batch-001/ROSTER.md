# Batch 001 Locked Receiver Roster

**Status:** Locked before `T000-RUN-002`; no Batch 001 result observed

The machine-readable authority is [`roster.json`](roster.json).
This roster prevents choosing receivers after seeing early outcomes.

| Slots | Declared family | Interface | Isolation | Media path |
| --- | --- | --- | --- | --- |
| 001–002 | OpenAI-GPT | Personal ChatGPT | Procedural | Native package |
| 003–004 | Gemini | Google API free tier | Technical | Native package |
| 005–006 | Qwen2.5-VL | Local Ollama | Technical | RMA-000 |
| 007–008 | Llama-3.2-Vision | Local Ollama | Technical | RMA-000 |

Cloud aliases must be resolved and recorded during transport-only preflight,
before a receiver sees T000.
The declared fallback rule may be used only at that time.
If neither declared choice is available, the slot stops and the roster must be
versioned before any further run; a result may never influence selection.

The two ChatGPT slots are procedurally isolated because the service boundary
cannot be independently audited.
Gemini calls expose no tools or grounding.
Local runs operate without network access and use only the supplied package and
the deterministic receiver media adapter.

Different variants within one declared family count as two runs from that
family, not as two families.
No claim of statistical independence follows from this allocation.
