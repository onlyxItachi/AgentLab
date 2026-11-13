# Session glossary: Agent Architecture, Context and Memory

[Back to session](README.en.md) | [Türkçe](kavram-sozlugu.md) | [General glossary](../../docs/en/glossary.md)

| Term | Meaning in this session |
| --- | --- |
| Harness | Application coordinating model calls, context, tool permissions and task flow. |
| Agent loop | Control loop repeating model proposals, validation, tool observations and continuation or stopping. |
| ReAct | An approach interleaving task assessment, actions and observations. |
| Plan-and-Solve | An approach preparing a brief task plan before executing its steps. |
| Action | A proposed or validated and executed operation; these are separate stages. |
| Observation | Actual result or error returned by an executed tool. |
| Trace | Record of observable requests, tools, results and stop reasons. |
| Context engineering | Designing what enters a model request and within which budget. |
| State | Current messages, results and task progress. |
| Session | Conversation and task scope maintained by the application. |
| Memory | Selected records available for later reuse. |
| Persistence | Retaining information after a process or session ends. |
| Retrieval | Selecting relevant pieces from a collection. |
| Corpus | Document or record collection available to search. |
| Vector search | Search ranking numerical vectors with a similarity measure. |
| Cosine similarity | Dot product normalized by vector lengths, measuring direction similarity. |
| Embedding | Numerical vector representation of an item; its method determines its behavior. |
| RAG | Generation that receives retrieved evidence in its context. |
| Grounding | Supporting an answer with inspectable sources. |
| Allowlist | The application's permitted tools and argument boundaries. |
| Step limit | Upper bound preventing an unbounded execution loop. |
| KV cache | Runtime memory retaining some prior-token computations, separate from model weights. |
