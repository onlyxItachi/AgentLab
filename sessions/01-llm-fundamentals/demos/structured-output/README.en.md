# Conceptual walkthrough: Tool function and structured output

[Back to demos](../README.en.md) | [Türkçe](README.md)

This walkthrough illustrates how a JSON payload from a glossary lookup relates to the rules in the [schema file](schema.json). It does not call an LLM or an external API.

## Expected schema fields

The [schema file](schema.json) requires exactly three fields (`term`, `found`, `explanation`) and forbids extras (`additionalProperties: false`):

- `term`: concept name (`string`)
- `found`: whether the concept exists in the glossary (`boolean`)
- `explanation`: explanation text (`string`)

Example payload for a known term:

```json
{"term": "token", "found": true, "explanation": "A unit produced by a tokenizer and processed by a model."}
```

Example payload for an unknown term:

```json
{"term": "unknown", "found": false, "explanation": "Term was not found in the glossary."}
```

Schema compliance alone does not establish that an explanation is factually true.

## Experiment D: Separate structure from truth

Compare these two payloads against the [schema file](schema.json):

1. **Object A** (valid JSON and schema-compliant, yet its explanation is **intentionally false**):

```json
{"term": "token", "found": true, "explanation": "A token is always a word."}
```

2. **Object B** (valid JSON, yet rejected by the schema because `found` is a string instead of a boolean):

```json
{"term": "token", "found": "true", "explanation": "A unit produced by a tokenizer and processed by a model."}
```

Being valid JSON, conforming to a schema, and containing accurate content are three separate checks.
