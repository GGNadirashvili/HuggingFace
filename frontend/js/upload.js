document.addEventListener("DOMContentLoaded", () => {
  const modelSelect = document.getElementById("model");

  const models = [
    { id: "facebook/detr-resnet-50", label: "Object Detection (DETR)" },
    { id: "google/vit-base-patch16-224", label: "Image Classification (ViT)" },
    { id: "hustvl/yolos-tiny", label: "Object Detection (YOLOS Tiny)" },
    { id: "openai/clip-vit-base-patch32", label: "Zero-shot Classification (CLIP)" }
  ];

  modelSelect.innerHTML = ""; 
  models.forEach(model => {
    const option = document.createElement("option");
    option.value = model.id;
    option.textContent = model.label;
    modelSelect.appendChild(option);
  });

  document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const imageInput = document.getElementById("image");
    const selectedModel = modelSelect.value;

    if (!imageInput.files.length) {
      alert("Please select an image file.");
      return;
    }

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);
    formData.append("model", selectedModel);

    try {
      const response = await fetch("", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      alert("Upload successful: " + JSON.stringify(result));
    } catch (err) {
      alert("Upload failed: " + err.message);
    }
  });
});
