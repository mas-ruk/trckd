document.addEventListener('DOMContentLoaded', () => {
  const shareModalEl = document.getElementById('shareOptionsModal');
  const shareModal   = new bootstrap.Modal(shareModalEl);
  const toggleBtn    = document.getElementById('toggleBtn');

  // Share button handler
  document.getElementById('shareBtn').addEventListener('click', async (event) => {
    event.preventDefault();

    // Only grab checked boxes from the uploaded-cards grid
    const selected = Array.from(
      document.querySelectorAll('.cards-grid .card-item input:checked')
    ).map(cb =>
      cb.closest('.card-item').dataset.cardId
    );

    if (selected.length === 0) {
      alert("Please select at least one card.");
      return;
    }

    try {
      const res = await fetch('/generate_share_link', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({ card_ids: selected })
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.message || 'Error');

      const shareUrl    = data.share_url;
      const downloadUrl = `${window.location.origin}/download_shared/${data.link_id}`;

      // Populate modal links/buttons
      document.getElementById('facebookShare').href =
        `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
      document.getElementById('whatsappShare').href =
        `https://api.whatsapp.com/send?text=${encodeURIComponent(shareUrl)}`;
      document.getElementById('copyLinkBtn').onclick = () => {
        navigator.clipboard.writeText(shareUrl);
        alert("Link copied!");
      };
      document.getElementById('downloadBtn').onclick = () => {
        window.location.href = downloadUrl;
      };

      shareModal.show();
    } catch (err) {
      console.error(err);
      alert("Failed to generate share link: " + err.message);
    }
  });

  // Sidebar toggle handler
  if (toggleBtn) toggleBtn.addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('collapsed');
  });

  // Filter uploaded cards
  const uploadedSearch = document.getElementById('uploadedSearch');
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
