# LLM playground

[Back to demos](../README.en.md) | [Türkçe](README.md)

Start with the [Colab notebook](AgentLab-Colab.ipynb): choose **File → Upload notebook** in Colab and run cells in order. The notebook headings are bilingual; most explanations and outputs remain in Turkish. You do not need local Python. The model download is about **1.75 GB**, plus packages. Check your network and available storage before starting. A GPU is not guaranteed; CPU works but is slower. Do not enter secrets. The last cell releases the model from memory. It does not automatically delete cache files or folders because their ownership cannot be established; inspect the temporary folder shown by the cell.

If Hugging Face was already loaded with a different cache, the notebook instructs you to restart the runtime.

## On your own computer

1. Complete [AgentLab setup](../../../../setup/README.en.md); your Python installation needs Tkinter.
2. Download and extract a matching [official llama.cpp release](https://github.com/ggml-org/llama.cpp/releases). You will select `llama-server` from it. See the [build instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) if no matching build is available.
3. Download `Qwen3.5-0.8B-Q4_0.gguf` from [Qwen3.5-0.8B GGUF](https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF), approximately **563 MB**. The model is Apache-2.0 licensed. Weights are not committed to the repository.
4. Open `start.cmd` on Windows or `start.command` on macOS; on Linux run `start.command`. Select `llama-server` and then the GGUF file. Your browser opens after loading. CPU is supported; speed depends on hardware.
5. Press **Ctrl+C** in the launcher to stop its own server. To uninstall, delete the model and llama.cpp files you downloaded and follow the [AgentLab uninstall guide](../../../../setup/README.en.md) if desired.

The local interface listens on `127.0.0.1`, and its model server uses a random temporary key. No paid API key is required. The raw table is the first step of a separate request; the post-sampling table is the first step of the displayed generation. Each shows at most eight candidates and explicitly indicates unavailable probabilities. Incomplete Unicode pieces may appear as byte arrays. The shown context size is the running server's limit. The Colab experiment limits input to 2,048 tokens; available hardware memory may be lower. A model may decline to call a tool, or another model's template may not support tools; invalid calls are never executed.
