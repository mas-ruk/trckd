document.addEventListener('DOMContentLoaded', () => {
const shareModalEl = document.getElementById('shareOptionsModal');
const shareModal   = new bootstrap.Modal(shareModalEl);

document.getElementById('shareBtn').addEventListener('click', async (event) => {
  event.preventDefault();  

  const selected = Array.from(
    document.querySelectorAll('.card-item input:checked')
  ).map(input =>
    input.closest('.card-item').getAttribute('data-card')
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

document.getElementById('toggleBtn').onclick = () => {
  document.getElementById('sidebar').classList.toggle('collapsed');
};
});