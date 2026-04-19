let notaArrastada = null;

async function carregarNotas() {
    const res = await fetch('/get_notes');
    const notas = await res.json();
    notas.forEach(n => criarElementoNota(n[1], n[2], n[0]));
}

function criarElementoNota(conteudo = '', colunaId = 'todo-column', id = null) {
    const nota = document.createElement('textarea');
    nota.className = 'post-it';
    nota.value = conteudo;
    nota.draggable = true;
    if (id) nota.dataset.id = id;

    const salvarOuAtualizar = async () => {
        const dados = {
            conteudo: nota.value,
            coluna: nota.parentElement ? nota.parentElement.id : colunaId,
            id: nota.dataset.id
        };

        if (nota.dataset.id) {
            await fetch('/update_note', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(dados)
            });
        } else {
            const res = await fetch('/save_note', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(dados)
            });
            const info = await res.json();
            nota.dataset.id = info.id;
        }
    };

    nota.addEventListener('blur', salvarOuAtualizar);
    nota.addEventListener('dragstart', () => { notaArrastada = nota; });
    nota.addEventListener('dragend', () => { notaArrastada = null; });

    document.getElementById(colunaId).appendChild(nota);
}

document.querySelectorAll('.column-content').forEach(coluna => {
    coluna.addEventListener('dragover', e => {
        e.preventDefault();
        coluna.classList.add('drag-over');
    });

    coluna.addEventListener('dragleave', () => coluna.classList.remove('drag-over'));

    coluna.addEventListener('drop', async () => {
        coluna.classList.remove('drag-over');
        if (notaArrastada) {
            coluna.appendChild(notaArrastada);
            const dados = {
                conteudo: notaArrastada.value,
                coluna: coluna.id,
                id: notaArrastada.dataset.id
            };
            await fetch('/update_note', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(dados)
            });
        }
    });
});

document.getElementById('btn-criar').addEventListener('click', () => criarElementoNota());

carregarNotas();
