document.getElementById('send').onclick = async () => {
  const input = document.getElementById('file');
  const resultDiv = document.getElementById('result');
  const decisionDiv = document.getElementById('decision');
  const imageContainer = document.getElementById('imageContainer');

  // Reset previous outputs
  resultDiv.innerText = '';
  decisionDiv.innerText = '';
  imageContainer.innerHTML = '';

  if (!input.files.length) {
    alert('📂 Please choose a file first!');
    return;
  }

  const file = input.files[0];
  const form = new FormData();
  form.append('file', file, file.name);

  resultDiv.innerText = '⚙️ Processing... Please wait...';
  resultDiv.style.background = '#fff8e1';

  try {
    // --- Call FastAPI backend ---
    const res = await fetch("http://127.0.0.1:8000/analyze_document/", {
      method: "POST",
      body: form
    });

    const text = await res.text();
    console.log("📥 Raw API Response:", text);

    try {
      const data = JSON.parse(text);
      console.log("✅ Parsed JSON:", data);

      // --- Display extracted text ---
      resultDiv.innerText = JSON.stringify(data.extracted_text, null, 2);
      resultDiv.style.background = '#eaffea';

      // --- Decision output ---
      if (data.decision) {
        const confidencePercent = data.confidence
          ? (data.confidence * 100).toFixed(1)
          : "N/A";
        decisionDiv.innerText = `🧠 Decision: ${data.decision} (Confidence: ${confidencePercent}%)`;
      } else {
        decisionDiv.innerText = "⚠️ No decision generated.";
      }

      // --- Show explainability image ---
      if (data.explainability_map && data.explainability_map !== "N/A") {
        const img = document.createElement('img');
        // Build full image URL
        img.src = `http://127.0.0.1:8000${data.explainability_map}`;
        img.alt = 'Explainability Visualization';
        img.style.maxWidth = '80%';
        img.style.border = '1px solid #ccc';
        img.style.borderRadius = '6px';
        img.style.marginTop = '10px';
        img.onload = () => console.log("🖼️ Image loaded successfully!");
        img.onerror = () => {
          console.error("❌ Could not load explainability image:", img.src);
          imageContainer.innerText = "⚠️ Failed to load visualization image.";
        };
        imageContainer.appendChild(img);
      } else {
        imageContainer.innerText = "⚠️ No explainability visualization available.";
      }

    } catch (jsonErr) {
      console.error("❌ JSON parse error:", jsonErr);
      resultDiv.innerText = "💬 Non-JSON response:\n" + text;
      resultDiv.style.background = '#fff7e6';
    }

  } catch (err) {
    console.error("❌ Request failed:", err);
    resultDiv.innerText = "❌ Error: " + err.message;
    resultDiv.style.background = '#ffe6e6';
  }
};
