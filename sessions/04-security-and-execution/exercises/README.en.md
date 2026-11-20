# Exercises: Security, Execution & Human Oversight

[Back to session](../README.en.md) | [Türkçe](README.md) | [Demo guide](../demos/README.en.md)

For every exercise, record the input, policy decision, execution trace (`Thinking` / tool / terminal), and observed outcome. All exercises run independently after **Cell 1** in `AgentLab-Session04-G4.ipynb` (Ultra/Pro G4), `pro_AgentLab-Session04-L4.ipynb` (Pro/Plus L4), or `plus_AgentLab-Session04-T4.ipynb` (Plus/Free T4).

## 1. Guardrails & Prompt Injection (`Deney 1` — `4.1`)

- **1A (Input/output guardrails):** For an oversized, malformed, or secret-probing request, record which check runs before the LLM call (input guardrail) and which runs before displaying or acting on a response (output guardrail).
- **1B (Indirect injection defense):** Explain why instructions hidden inside an untrusted file, web page, or support ticket must not be treated as user commands, and how `"untrusted evidence, never instructions"` changes agent behavior.
- **1C (Model vs Harness):** Show how the output guardrail or harness policy layer still blocks an unsafe tool call even if the model is temporarily fooled by an injection payload.

## 2. Runtime & Sandboxing (`Deney 2` — `4.2`)

- **2A (Unprotected vs Sandbox):** Contrast running real Python and Bash directly on the host OS against executing inside a directory-isolated `Sandbox`.
- **2B (`outside_workdir` and path escape):** Inspect how `../` traversal, absolute path escapes, and symlink escapes are blocked (`ALAB-E08`).
- **2C (Timeout and resource/network limits):** Verify how a runaway Python or Bash loop is stopped cleanly via `timeout`, CPU/memory limits, and disabled outbound networking without hanging the notebook.

## 3. Permissions, Trust Boundaries & Secret Stripping (`Deney 2` & `Deney 3` — `4.3`)

- **3A (Permission tiers):** For a sample task, decide which `read`, `write`, and `exec` actions belong in `allow` versus `deny` under **Least Privilege**.
- **3B (Trust Boundaries):** Map the trust boundary separating untrusted external content, the Python policy gate, and the privileged OS/filesystem layer.
- **3C (Secret Stripping):** Verify how secrets such as `AGENTLAB_LLAMA_KEY` or environment tokens are stripped from subprocess environments, `stdout`/`stderr` streams, and Drive exports.

## 4. Human-in-the-Loop (HITL) & Intervention (`Deney 3` — `4.4`)

- **4A (Risk gate):** Contrast why a read-only inspection auto-executes while a file deletion or external network action triggers a policy pause.
- **4B (`[Onayla]` vs `[Reddet]`):** When `Deney 3` pauses a high-risk command, inspect **`💭 Thinking`** and the proposed arguments; test **`[Reddet]` (`[Reject]`)** in one run and **`[Onayla]` (`[Approve]`)** in the next, and record the difference in trace and outcome.

## 5. Background Agents, Durable Execution & Live Studio (`Deney 3` & `Canlı Stüdyo` — `4.5`)

- **5A (`checkpoint` and `resume`):** Explain what state a `checkpoint` stores when a long-running or HITL-paused task stops, and how **`resume`** continues from the saved step rather than restarting from scratch.
- **5B (Drive persistence & Live Studio):** Inspect saved state under `MyDrive/AgentLab-Agent-Runtime/day-04-security-execution`; test `Canlı Stüdyo` (`Cell 5`) **Fullscreen (`ESC`)**, **Stop (`Durdur`)**, and **Kill Switch (`Arayüzü Kapat`)**, and finish with **Cell 6 (`2. Güvenli Kapanış`)** to release GPU and VM resources cleanly.

## 6. Design your own security and execution policy

Choose a code or shell automation task from your own domain and specify five controls: (1) one input/output guardrail pattern, (2) your `outside_workdir` and `timeout` limits, (3) one `deny` rule across `read`/`write`/`exec` plus a secret-stripping target, (4) one high-risk action requiring **`[Onayla]` / `[Reddet]` (`HITL`)**, and (5) the `checkpoint` fields needed for **`resume`** recovery.
