(() => {
  'use strict';

  const form = document.getElementById('recommend-form');
  const button = document.getElementById('submit-button');
  const empty = document.getElementById('empty-state');
  const loading = document.getElementById('loading-state');
  const error = document.getElementById('error-state');
  const recommendations = document.getElementById('recommendation-state');
  const list = document.getElementById('recommendation-list');
  const resultCount = document.getElementById('result-count');
  const notice = document.getElementById('result-notice');
  const reset = document.getElementById('reset-button');

  function showOnly(target) {
    [empty, loading, error, recommendations].forEach((element) => {
      element.hidden = element !== target;
    });
  }

  function addTextElement(parent, tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = String(text ?? '');
    parent.appendChild(element);
    return element;
  }

  function safeScore(value) {
    const score = Number(value);
    return Number.isFinite(score) ? Math.min(100, Math.max(0, Math.round(score))) : 0;
  }

  function safeRainfallBand(value) {
    if (!Array.isArray(value) || value.length !== 2) return null;
    const numbers = value.map(Number);
    return numbers.every(Number.isFinite) ? numbers : null;
  }

  function renderResults(payload) {
    if (!payload || !Array.isArray(payload.recommendations)) {
      throw new Error('The server response did not contain a valid recommendation list.');
    }

    list.replaceChildren();
    const matches = payload.recommendations.length;
    resultCount.textContent = `${matches} match${matches === 1 ? '' : 'es'}`;
    notice.textContent = payload.notice || 'Educational screening only. Confirm choices with a local agricultural expert.';

    if (matches === 0) {
      addTextElement(
        list,
        'div',
        'error-state',
        'No crop profile matched the selected soil and season together. Try another valid combination or ask your local agriculture office.'
      );
      return;
    }

    payload.recommendations.forEach((crop) => {
      const card = document.createElement('article');
      card.className = 'crop-card';

      const top = document.createElement('div');
      top.className = 'crop-card-top';
      addTextElement(top, 'h3', '', crop.name || 'Crop');
      addTextElement(top, 'span', 'score', `Rule score: ${safeScore(crop.match_score)}/100`);
      card.appendChild(top);

      const score = safeScore(crop.match_score);
      const track = document.createElement('div');
      track.className = 'score-track';
      track.setAttribute('role', 'progressbar');
      track.setAttribute('aria-label', `${crop.name || 'Crop'} rule-based score`);
      track.setAttribute('aria-valuemin', '0');
      track.setAttribute('aria-valuemax', '100');
      track.setAttribute('aria-valuenow', String(score));
      const fill = document.createElement('div');
      fill.className = 'score-fill';
      fill.style.width = `${score}%`;
      track.appendChild(fill);
      card.appendChild(track);

      addTextElement(card, 'p', 'crop-description', crop.description || '');
      addTextElement(card, 'span', 'why-title', 'Why it matched');
      const reasonsList = document.createElement('ul');
      reasonsList.className = 'crop-reasons';
      (Array.isArray(crop.reasons) ? crop.reasons : []).forEach((reason) => {
        addTextElement(reasonsList, 'li', '', reason);
      });
      card.appendChild(reasonsList);

      const evidence = document.createElement('div');
      evidence.className = 'evidence';
      addTextElement(evidence, 'strong', '', 'Reference note:');
      evidence.appendChild(document.createTextNode(` ${crop.evidence || 'See the agricultural reference for context.'}`));
      evidence.appendChild(document.createElement('br'));

      try {
        const sourceUrl = new URL(crop.source);
        if (sourceUrl.protocol === 'https:' || sourceUrl.protocol === 'http:') {
          const link = addTextElement(evidence, 'a', '', 'View agricultural reference');
          link.href = sourceUrl.href;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
        }
      } catch (_error) {
        // Ignore a malformed source URL rather than rendering an unsafe link.
      }

      evidence.appendChild(document.createElement('br'));
      const band = safeRainfallBand(crop.prototype_rainfall_band_mm);
      const bandText = band
        ? `Prototype rainfall band: ${band[0]}\u2013${band[1]} mm (not an official threshold)`
        : 'Prototype rainfall band unavailable (not an official threshold)';
      addTextElement(evidence, 'span', '', bandText);
      card.appendChild(evidence);
      list.appendChild(card);
    });
  }

  async function readJsonResponse(response) {
    try {
      return await response.json();
    } catch (_parseError) {
      throw new Error('The server returned an unreadable response. Check that the backend is running.');
    }
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload.rainfall_mm = Number(payload.rainfall_mm);

    button.disabled = true;
    showOnly(loading);
    error.textContent = '';

    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      const data = await readJsonResponse(response);
      if (!response.ok) throw new Error(data.error || 'Unable to generate recommendations.');

      renderResults(data);
      showOnly(recommendations);
    } catch (err) {
      if (err.name === 'AbortError') {
        error.textContent = 'The request timed out. Please check your connection and try again.';
      } else if (err instanceof TypeError) {
        error.textContent = 'Could not reach the recommendation service. Please try again.';
      } else {
        error.textContent = err.message || 'A network error occurred. Please try again.';
      }
      showOnly(error);
    } finally {
      window.clearTimeout(timeout);
      button.disabled = false;
    }
  });

  reset.addEventListener('click', () => {
    form.reset();
    showOnly(empty);
    document.getElementById('soil_type').focus();
  });
})();
