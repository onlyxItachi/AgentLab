# Mini demo: Tool function and structured output

[Back to demos](../README.en.md) | [Türkçe](README.md)

**Status:** Working local starter example. This demo does not call an LLM, a real agent, or an external API. It calls a fixed concept table like a tool function and checks the result against a small schema. The real AI agent the instructor will use has not been selected.

First complete the [setup guide](../../../../setup/README.en.md). Open a terminal at the repository root, enter the demo folder, and use the commands for your system:

```text
cd sessions/01-llm-fundamentals/demos/structured-output
```

macOS / Linux:

```sh
../../../../.agentlab/venv/bin/python demo.py --term token --language en
../../../../.agentlab/venv/bin/python demo.py --term unknown --language en
../../../../.agentlab/venv/bin/python demo.py --term schema --language en
```

Windows PowerShell:

```powershell
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term token --language en
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term unknown --language en
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term schema --language en
```

Observe the `term`, `found`, and `explanation` fields. The [schema file](schema.json) describes fields and types. The [source code](demo.py) locally checks only the small feature subset used in this schema; it is not a general JSON Schema validator. Schema compliance alone does not prove an explanation is correct.

The demo makes no network connections and creates no persistent resources. See the [setup guide](../../../../setup/README.en.md) for the project environment.

## Experiment D: Separate structure from truth

This small companion runs two examples through the same actual validator:

```text
# macOS / Linux
../../../../.agentlab/venv/bin/python schema_lab.py --language en
# Windows PowerShell
..\..\..\..\.agentlab\venv\Scripts\python.exe schema_lab.py --language en
```

Object A is valid JSON and passes the schema, but its explanation is **intentionally false**. B is valid JSON too, but fails the schema because `found` is a string rather than a boolean. The validator does not check whether the explanation is true. The example runs offline and makes no model call.
