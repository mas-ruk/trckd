console.log('🔍 share.js loaded');

document.addEventListener('DOMContentLoaded', () => {
  console.log('📄 DOMContentLoaded');

  // Modal
  const shareModalEl  = document.getElementById('shareOptionsModal');
  const shareModal    = new bootstrap.Modal(shareModalEl);
  const closeModalBtn = shareModalEl.querySelector('.btn-close');

  // Carousel / buttons
  let selected       = [];
  const carousel     = document.getElementById('selectedCarousel');
  const shareBtn     = document.getElementById('shareBtn');
  const clearAllBtn  = document.getElementById('clearAllBtn');

  console.log('shareBtn=', shareBtn, 'clearAllBtn=', clearAllBtn);

  function renderSelected() {
    carousel.innerHTML = '';
    selected.forEach(c => {
      const cardEl = document.createElement('div');
      cardEl.className = 'selected-card';
      cardEl.innerHTML = `
        <button class="remove-btn">&times;</button>
        <img src="${c.image_url}" alt="${c.name}">
        <div class="card-name">${c.name}</div>
      `;
      cardEl.querySelector('.remove-btn').onclick = () => {
        const gridCb = document.querySelector(
          `.cards-grid .card-item[data-card-id="${c.id}"] input[type="checkbox"]`
        );
        if (gridCb) gridCb.checked = false;
        selected = selected.filter(x => x.id !== c.id);
        renderSelected();
      };
      carousel.append(cardEl);
    });
    document.getElementById('shareCount').textContent = selected.length;
  }

  clearAllBtn.addEventListener('click', () => {
    console.log('🗑️ Clear All clicked');
    document
      .querySelectorAll('.cards-grid .card-item input[type="checkbox"]')
      .forEach(cb => cb.checked = false);
    selected = [];
    renderSelected();
  });

  document.querySelectorAll('.cards-grid .card-item input[type="checkbox"]')
    .forEach(cb => {
      cb.addEventListener('change', e => {
        const item = e.target.closest('.card-item');
        const cardData = {
          id:         item.dataset.cardId,
          name:       item.querySelector('label').innerText.trim(),
          image_url:  item.querySelector('img').src
        };
        if (e.target.checked) selected.push(cardData);
        else selected = selected.filter(x => x.id !== cardData.id);
        renderSelected();
      });
    });

  renderSelected();

  shareBtn.addEventListener('click', async ev => {
    console.log('🖱️ shareBtn clicked; selected:', selected);
    ev.preventDefault();
    if (selected.length === 0) {
      alert('Please select at least one card.');
      return;
    }
    try {
      const res = await fetch('/generate_share_link', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ card_ids: selected.map(c => c.id) })
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.message || 'Error');

      const shareUrl    = data.share_url;
      const downloadUrl = `${window.location.origin}/download_shared/${data.link_id}`;

      shareModalEl.querySelector('#facebookShare').href =
        `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
      shareModalEl.querySelector('#whatsappShare').href =
        `https://api.whatsapp.com/send?text=${encodeURIComponent(shareUrl)}`;
      shareModalEl.querySelector('#copyLinkBtn').onclick = () => {
        navigator.clipboard.writeText(shareUrl);
        alert('Link copied!');
      };
      shareModalEl.querySelector('#downloadBtn').onclick = () => {
        window.location.href = downloadUrl;
      };

      shareModal.show();
    } catch (err) {
      console.error(err);
      alert('Failed to generate share link: ' + err.message);
    }
  });

  closeModalBtn.addEventListener('click', () => shareModal.hide());

  // existing sidebar & search code follows...
  const toggleBtn      = document.getElementById('toggleBtn');
  const uploadedSearch = document.getElementById('uploadedSearch');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.getElementById('sidebar').classList.toggle('collapsed');
    });
  }
  if (uploadedSearch) {
    uploadedSearch.addEventListener('input', () => {
      const term = uploadedSearch.value.trim().toLowerCase();
      document.querySelectorAll('.cards-grid .card-item').forEach(item => {
        const name = item.querySelector('label').textContent.toLowerCase();
        item.style.display = name.includes(term) ? '' : 'none';
      });
    });
  }
});
