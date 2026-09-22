const form = document.getElementById("download-form");
const urlInput = document.getElementById("url");
const submitBtn = document.getElementById("submit-btn");
const status = document.getElementById("status");

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
    status.textContent = "Only Facebook and YouTube links are supported.";
    return;
  }

  submitBtn.disabled = true;
  status.textContent = "Downloading… this can take a moment.";

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

    status.textContent = `Saved: ${filename}`;
  } catch (err) {
    status.textContent = `Error: ${err.message}`;
  } finally {
    submitBtn.disabled = false;
  }
});
