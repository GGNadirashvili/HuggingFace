document.addEventListener("DOMContentLoaded", () => {
  const modelSelect = document.getElementById("model");

  const models = [
    { id: "facebook/detr-resnet-50", label: "Object Detection (DETR)" },
    { id: "google/vit-base-patch16-224", label: "Image Classification (ViT)" },
    { id: "hustvl/yolos-tiny", label: "Object Detection (YOLOS Tiny)" },
    { id: "openai/clip-vit-base-patch32", label: "Zero-shot Classification (CLIP)" }
  ];

  // Check availability of each model
  async function checkModelAvailability(modelId) {
    try {
      const response = await fetch(`https://huggingface.co/api/models/${modelId}`);
      if (!response.ok) return false;

      const data = await response.json();

      if (data.disabled || (data.pipeline_tag && data.lastModified === null)) {
        return false;
      }

      return true;
    } catch (err) {
      console.error(`Error checking model ${modelId}:`, err);
      return false;
    }
  }

  // Populate dropdown with valid models
  async function populateModelDropdown() {
    modelSelect.innerHTML = "";

    for (const model of models) {
      const isValid = await checkModelAvailability(model.id);
      if (isValid) {
        const option = document.createElement("option");
        option.value = model.id;
        option.textContent = model.label;
        modelSelect.appendChild(option);
      } else {
        console.warn(`Model not available: ${model.id}`);
      }
    }

    if (modelSelect.options.length === 0) {
      const option = document.createElement("option");
      option.textContent = "No valid models available";
      option.disabled = true;
      modelSelect.appendChild(option);
    }
  }

  populateModelDropdown();

  // Form submission
  document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const imageInput = document.getElementById("image");
    const selectedModel = modelSelect.value;

    if (!imageInput.files.length) {
      alert("Please select an image file.");
      return;
    }

    // Validate model before upload
    const isModelValid = await checkModelAvailability(selectedModel);
    if (!isModelValid) {
      alert("The selected model is unavailable or invalid on Hugging Face.");
      return;
    }

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);
    formData.append("model", selectedModel);

    try {
      const response = await fetch("https://2gohabukv8.execute-api.us-east-1.amazonaws.com/prod/upload", {
        method: "POST",
        body: formData
      });

      const contentType = response.headers.get("content-type") || "";
      let result;

      if (contentType.includes("application/json")) {
        result = await response.json();
      } else {
        result = await response.text();
      }

      if (!response.ok) {
        alert("Upload failed: " + result);
      } else {
        alert("Upload successful: " + JSON.stringify(result, null, 2));
      }
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed: " + (err.message || JSON.stringify(err)));
    }
  });
});
