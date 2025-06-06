document.getElementById('perguntaForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const pergunta = document.getElementById('pergunta').value;

  fetch('/api/perguntar', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({pergunta: pergunta})
  })
  .then(res => res.json())
  .then(data => {
    const popup = document.getElementById('popup');
    popup.innerText = data.resposta;
    popup.style.display = 'block';
  })
  .catch(err => {
    alert('Erro: ' + err);
  });
});
