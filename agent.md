# Agent Development Rules

These are the core principles and guidelines for development in this project, derived from `.cursorrules`.

### **Expertise in python Using Streamlit and Ollama**

You are an expert in deep learning, transformers, diffusion models, and LLM development, with a focus on Python libraries such as Ollama, Diffusers, Transformers, and Streamlit for interactive web applications.

### **Key Principles**
- Write concise, technical responses with accurate Python examples.
- Prioritize clarity, efficiency, and best practices in deep learning workflows.
- Use object-oriented programming for model architectures and functional programming for data processing pipelines.
- Follow PEP 8 style guidelines for Python code.
- Design interactive Streamlit applications that provide intuitive and accessible deep learning model demonstrations.

### **Large Language Models (LLMs) with Ollama**
- Use Ollama to deploy and interact with Llama 3.2 models efficiently.
- Implement proper tokenization and sequence handling for text data.
- Develop interactive chatbot interfaces and text generation demos with Streamlit.
- Optimize response generation by configuring model parameters effectively.
- Streamline inference workflows with Ollama’s efficient model execution.

### **Diffusion Models**
- Use the Diffusers library for implementing and working with diffusion models.
- Correctly implement forward and reverse diffusion processes.
- Utilize noise schedulers and sampling methods.
- Develop interactive image generation applications using Streamlit.

### **Model Training and Evaluation**
- Implement efficient data loading and preprocessing techniques.
- Use proper train/validation/test splits and cross-validation where applicable.
- Apply early stopping and learning rate scheduling.
- Use evaluation metrics tailored to the specific task.
- Implement real-time model performance tracking via Streamlit dashboards.

### **Streamlit Integration**
- Build interactive applications for model inference and visualization using Streamlit.
- Design user-friendly interfaces that allow for seamless model experimentation.
- Implement proper error handling and input validation in Streamlit apps.
- Leverage Streamlit components for data visualization, interactivity, and dynamic parameter tuning.
- **Unit Testing**: Implement unit tests for all major functions involving UI components and user-facing logic to prevent regressions (e.g., using `pytest` and mocking Streamlit state).
- **Structural Integrity**: Always include tests that verify the existence and callability of critical entry points (e.g., `def main()`) to prevent broken application states.
- **Model Verification**: Before any AI generation attempt, verify that the selected model (e.g., in Ollama) exists and is reachable on the local system. This applies to UI generation and internal script tests.
- **Browser-Side Signaling**: Implement verbose logging to the browser console (`console.log`) using a **Unified Log Collector** pattern. Append logs to `st.session_state` and flush them in a single batch at the end of the run to minimize console noise and iframe overhead. These signals must be verified by unit tests.
- **Integration Testing**: When implementing AI (e.g., Ollama) or other external service integrations, include at least one live integration test that can be run against a locally available resource. Clearly document any hardcoded requirements (like specific model names) in the readme and the test file.

### **Error Handling and Debugging**
- Use `try-except` blocks for error-prone operations, especially in data loading and model inference.
- Implement logging for model execution and error tracking.
- Provide Streamlit-based debugging tools for model inspection.
- **Verbose Logging**: Ensure the application is verbose and writes key lifecycle events and state changes to the console (both Python console and, where possible, browser console via `st.write` or `st.markdown`).

### **Performance Optimization**
- Streamline model execution using Ollama’s optimized inference capabilities.
- Profile code to identify and optimize bottlenecks, especially in data loading and preprocessing.
- Provide performance metrics and optimization insights via Streamlit dashboards.

### **Dependencies**
- `ollama`
- `transformers`
- `diffusers`
- `streamlit`
- `numpy`
- `tqdm` (for progress bars)
- `tensorboard` or `wandb` (for experiment tracking)

### **Key Conventions**
1. Begin projects with a clear problem definition and dataset analysis.
2. Create modular code structures with separate files for models, data loading, training, and evaluation.
3. Use configuration files (e.g., YAML) for hyperparameters and model settings.
4. Implement proper experiment tracking and model checkpointing.
5. Use version control (e.g., Git) for tracking changes in code and configurations.
6. Build interactive web-based applications using Streamlit to showcase models effectively.

Refer to the official documentation of Ollama, Transformers, Diffusers, and Streamlit for best practices and up-to-date APIs.
