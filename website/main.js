async function loadMarkdown(path) {
    try {
      const response = await fetch(path);
      const markdown = await response.text();
      const html = marked.parse(markdown);
      document.getElementById('content').innerHTML = html;
    } catch (err) {
      document.getElementById('content').innerHTML = `<p>Failed to load content: ${err.message}</p>`;
    }
  }
  