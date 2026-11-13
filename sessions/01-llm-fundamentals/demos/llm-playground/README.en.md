# LLM playground

[Back to demos](../README.en.md) | [Türkçe](README.md)

Start with the [Colab notebook](AgentLab-Colab.ipynb): download it from GitHub (or use your Google Drive copy), choose **File → Upload notebook** in Colab, and run cells in order (`0A` environment/device check, `1A` library install, `2A`–`2E` pinned revision manifest and model loading, `3A`–`3B` token inspection, `4A`–`4C` probability distribution and sampling, `5A`–`5B` greedy vs. sampled text generation, `6A`–`6C` strict single tool-call validation loop, `7A` memory release). The notebook headings are bilingual; most explanations and outputs remain in Turkish. You do not need local Python. The model download is about **1.75 GB**, plus packages. Check your network and available storage before starting. A GPU is not guaranteed; CPU works but is slower. Do not enter secrets. The last cell (`7A`) releases the model from memory. It does not automatically delete cache files or folders because their ownership cannot be established; inspect the temporary folder shown by the cell, so `7A` intentionally raises a `RuntimeError` safety guard after freeing memory to refuse automatic disk deletion (this is expected behavior).

If Hugging Face was already loaded with a different cache, the notebook instructs you to restart the runtime.

## Interpretation

Incomplete Unicode pieces may appear as byte arrays. Cell `4B` (`next_token_distribution`) plots the raw next-token distribution and the temperature/top-k/top-p post-sampling distribution side-by-side from one single-step forward pass; multi-token generation runs separately in `5A`–`5B` (`generate_text`). Each shows at most eight candidates and explicitly indicates unavailable probabilities. The Colab experiment limits input to 2,048 tokens; available hardware memory may be lower. A model may decline to call a tool, or a proposal may fail harness validation; invalid calls are never executed.
