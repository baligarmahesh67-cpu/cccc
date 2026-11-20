(() => {
  const form = document.getElementById('recommend-form');
  const button = document.getElementById('submit-button');
  const status = document.getElementById('status');
  const list = document.getElementById('recommendation-list');
  const notice = document.getElementById('result-notice');

  function addText(parent, tag, text, className) {
    const node = document.createElement(tag);
    node.textContent = String(text ?? '');
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form).entries());
    data.rainfall_mm = Number(data.rainfall_mm);
    button.disabled = true;
    status.textContent = 'Checking your farm conditions…';
    list.replaceChildren();
    notice.textContent = '';

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify(data)
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'Unable to generate recommendations.');
      status.textContent = payload.count + ' crop match(es) found.';
      payload.recommendations.forEach((crop) => {
        const card = document.createElement('article');
        card.className = 'crop-card';
        const top = document.createElement('div');
        top.className = 'crop-top';
        addText(top, 'strong', crop.name || 'Crop');
        addText(top, 'span', 'Rule score: ' + Number(crop.match_score || 0) + '/100', 'score');
        card.appendChild(top);
        const bar = document.createElement('div');
        bar.className = 'bar';
        const fill = document.createElement('span');
        fill.style.width = Math.max(0, Math.min(100, Number(crop.match_score) || 0)) + '%';
        bar.appendChild(fill);
        card.appendChild(bar);
        addText(card, 'p', crop.description || '');
        addText(card, 'strong', 'Why it matched');
        const reasons = document.createElement('ul');
        (Array.isArray(crop.reasons) ? crop.reasons : []).forEach((reason) => addText(reasons, 'li', reason));
        card.appendChild(reasons);
        addText(card, 'p', 'Reference: ' + (crop.evidence || 'See agricultural references.'));
        const link = document.createElement('a');
        try {
          const url = new URL(crop.source);
          if (url.protocol === 'https:' || url.protocol === 'http:') {
            link.href = url.href;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = 'Open agricultural source';
            card.appendChild(link);
          }
        } catch (_) { /* Do not render an invalid source URL. */ }
        list.appendChild(card);
      });
      notice.textContent = payload.notice || 'Educational screening only. Confirm choices with a local agriculture expert.';
      if (!payload.count) status.textContent = 'No crop profile matched. Try another valid combination.';
    } catch (error) {
      status.textContent = error.message || 'A network error occurred. Please try again.';
    } finally {
      button.disabled = false;
    }
  });
})();