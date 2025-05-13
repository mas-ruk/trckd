document.getElementById('shareBtn').addEventListener('click', async () => {
  const selected = Array.from(document.querySelectorAll('.card-item input:checked')).map(input => 
    input.closest('.card-item').getAttribute('data-card')
  );
  
  if (selected.length === 0) {
    alert("Please select at least one card.");
    return;
  }

  const res = await fetch('/generate_share_link', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ cards: selected })
  });

  const data = await res.json();
  const sharedLink = `${window.location.origin}/shared/${data.link_id}`;
  const downloadLink = `${window.location.origin}/download_shared/${data.link_id}`;

  document.getElementById('facebookShare').href =
    `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(sharedLink)}`;
  document.getElementById('whatsappShare').href =
    `https://api.whatsapp.com/send?text=${encodeURIComponent(sharedLink)}`;
  
  document.getElementById('copyLinkBtn').onclick = () => {
    navigator.clipboard.writeText(sharedLink);
    alert("Link copied!");
  };

  document.getElementById('downloadBtn').onclick = () => {
    window.location.href = downloadLink;
  };
});

// Sidebar Toggle
document.getElementById('toggleBtn').onclick = () => {
  document.getElementById('sidebar').classList.toggle('collapsed');
};
