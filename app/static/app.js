const form = document.getElementById("download-form");
const urlInput = document.getElementById("url");
const submitBtn = document.getElementById("submit-btn");
const status = document.getElementById("status");
const statusText = document.getElementById("status-text");
const statusSpinner = document.getElementById("status-spinner");
const statusSuccess = document.getElementById("status-success");
const statusError = document.getElementById("status-error");

const STATUS_STYLES = {
  progress: "border-slate-700 bg-slate-800 text-slate-200",
  success: "border-emerald-800 bg-emerald-950 text-emerald-300",
  error: "border-red-800 bg-red-950 text-red-300",
};

function setStatus(kind, message) {
  status.classList.remove("hidden");
  status.className = `mt-4 rounded-lg border px-4 py-3 text-sm flex items-center gap-3 ${STATUS_STYLES[kind]}`;

  statusSpinner.classList.toggle("hidden", kind !== "progress");
  statusSuccess.classList.toggle("hidden", kind !== "success");
  statusError.classList.toggle("hidden", kind !== "error");

  statusText.textContent = message;
}

function endpointFor(url) {
  const host = new URL(url).hostname;
  if (host.includes("facebook.com") || host.includes("fb.watch")) {
    return "/download/facebook";
  }
  if (host.includes("youtube.com") || host.includes("youtu.be")) {
    return "/download/youtube";
  }
  return null;
}

function filenameFrom(response, fallback) {
  const header = response.headers.get("content-disposition") || "";
  const match = header.match(/filename="?([^"]+)"?/);
  return match ? match[1] : fallback;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const url = urlInput.value.trim();
  const endpoint = endpointFor(url);

  if (!endpoint) {
    setStatus("error", "Only Facebook and YouTube links are supported.");
    return;
  }

  submitBtn.disabled = true;
  setStatus("progress", "Downloading… this can take a moment.");

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Download failed");
    }

    const blob = await response.blob();
    const filename = filenameFrom(response, "video.mp4");
    const objectUrl = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(objectUrl);

    setStatus("success", `Saved: ${filename}`);
  } catch (err) {
    setStatus("error", `Error: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
  }
});
