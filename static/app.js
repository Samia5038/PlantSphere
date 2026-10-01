document.addEventListener("DOMContentLoaded", () => {
  const cropForm = document.querySelector("#crop-form");
  const soilForm = document.querySelector("#soil-form");

  async function submitForm(form, result, render) {
    const button = form.querySelector("button[type='submit']");
    const label = button.querySelector(".button-label");
    const originalLabel = label.textContent;
    button.disabled = true;
    label.textContent = "Working...";
    result.classList.add("is-loading");

    try {
      const response = await fetch(form.action, { method: "POST", body: new FormData(form) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "The request could not be completed.");
      render(result, data);
    } catch (error) {
      result.innerHTML = `<span class="result-kicker">PLEASE CHECK</span><h2>We couldn't finish<br>that request.</h2><p>${escapeHtml(error.message)}</p>`;
    } finally {
      result.classList.remove("is-loading");
      button.disabled = false;
      label.textContent = originalLabel;
    }
  }

  if (cropForm) {
    cropForm.addEventListener("submit", (event) => {
      event.preventDefault();
      submitForm(cropForm, document.querySelector("#crop-result"), (result, data) => {
        result.innerHTML = `<span class="result-kicker">YOUR CROP MATCH</span>
        <div class="result-illustration result-illustration-done">
       
        <span></span><span></span><span></span>
        <i></i></div><p class="match-label">CONDITIONS POINT TOWARD</p>
        
        <h2 class="crop-name">${escapeHtml(data.prediction)}</h2>
        <p>Based on the nutrient and climate values you entered.</p>
        <div class="confidence-row"><span>Model confidence</span>
        
        <strong>${Number(data.confidence)}%</strong>
        </div>
        
        <div class="confidence-track"><i style="width:${Math.min(100, Math.max(0, Number(data.confidence)))}%"></i></div>
        <span class="result-footnote">GUIDANCE, NOT A GUARANTEE OF YIELD</span>`;
      });
    });
  }

  if (soilForm) {
    const input = soilForm.querySelector("input[type='file']");
    input.addEventListener("change", () => {
      document.querySelector("#file-label").textContent = input.files[0]?.name || "Drop an image here or browse";
    });
    soilForm.addEventListener("submit", (event) => {
      event.preventDefault();
      submitForm(soilForm, document.querySelector("#soil-result"), (result, data) => {
        const crops = data.recommended_crops.map(escapeHtml).join(" · ");
        result.innerHTML = `<span class="result-kicker">TRAINED IMAGE CLASSIFIER</span>
        <div class="soil-profile-art soil-profile-done">
        <span></span><span></span><span></span>
        </div><p class="match-label">PREDICTED SOIL FAMILY</p><h2 class="crop-name">${escapeHtml(data.soil_type)}</h2>
        <p>Associated crops: ${crops || "No crop list available."}</p>
        <div class="confidence-row"><span>Prediction confidence</span>
        
        <strong>${Number(data.confidence)}%</strong>
        </div>
        
        <div class="confidence-track"><i style="width:${Math.min(100, Math.max(0, Number(data.confidence)))}%"></i></div>
        <span class="result-footnote">MODEL: EXTRA TREES / PIXEL + COLOR FEATURES</span>`;
      });
    });
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[character]);
  }
});