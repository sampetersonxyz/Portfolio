// Resolve published release assets on each visit so downloads stay current.
(async () => {
  const status = document.getElementById('vision-release-status');
  const downloads = document.getElementById('vision-downloads');
  try {
    const response = await fetch('https://api.github.com/repos/petesamerson/V-s-on/releases/latest', {
      headers: { Accept: 'application/vnd.github+json' },
      signal: AbortSignal.timeout(10000)
    });
    if (response.status === 404) {
      status.textContent = 'Windows and Android downloads will appear here when a release is published.';
      return;
    }
    if (!response.ok) throw new Error('Release unavailable');
    const release = await response.json();
    const assets = Array.isArray(release.assets) ? release.assets : [];
    let count = 0;
    for (const [platform, pattern] of [
      ['Windows', /\.(exe|msi|msix)$/i],
      ['Android', /\.apk$/i]
    ]) {
      const matches = assets.filter(asset => pattern.test(asset.name) ||
        (platform === 'Windows' && /(?:windows|win64|win32|win-x64).*\.zip$/i.test(asset.name)));
      for (const asset of matches) {
        const url = new URL(asset.browser_download_url);
        if (url.protocol !== 'https:' || url.hostname !== 'github.com') continue;
        const link = document.createElement('a');
        link.href = url.href;
        link.textContent = `Download for ${platform} — ${asset.name}`;
        link.style.cssText = 'display:inline-block;margin:0.75rem 0;padding:0.75rem;background:#3b82f6;color:white;border-radius:6px;overflow-wrap:anywhere';
        downloads.append(link, document.createElement('br'));
        count++;
      }
    }
    status.textContent = count
      ? `Latest release: ${release.name || release.tag_name}. Download again here for future updates.`
      : 'The latest release has no Windows or Android downloads yet.';
  } catch {
    status.textContent = 'Unable to check builds right now. Browse all releases below for downloads.';
  }
})();
