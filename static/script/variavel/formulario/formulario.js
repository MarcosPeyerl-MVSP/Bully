document.addEventListener('DOMContentLoaded', function() {
    console.log("📋 Iniciando formulário...");
    
    const containerPerguntas = document.getElementById('container-perguntas');
    const btnVoltar = document.getElementById('btn-voltar');
    const btnProximo = document.getElementById('btn-proximo');
    const btnEnviar = document.getElementById('btn-enviar');
    const areaEnvio = document.getElementById('area-envio');
    const progressBar = document.getElementById('barra-progresso');
    const contadorPergunta = document.getElementById('pergunta-atual');
    const debugInfo = document.getElementById('debug-info');
    const debugText = document.getElementById('debug-text');
    
    const perguntas = document.querySelectorAll('.pergunta');
    const totalPerguntas = perguntas.length;
    let perguntaAtual = 0;
    const respostas = {};

    console.log(`📊 Total de perguntas carregadas: ${totalPerguntas}`);

    // Mostrar debug info se houver problemas
    if (totalPerguntas === 0) {
        debugInfo.classList.remove('d-none');
        debugText.textContent = 'Nenhuma pergunta foi carregada do banco de dados.';
    }

    function atualizarNavegacao() {
        // Atualizar barra de progresso
        const progresso = ((perguntaAtual + 1) / totalPerguntas) * 100;
        progressBar.style.width = `${progresso}%`;
        progressBar.setAttribute('aria-valuenow', progresso);
        
        // Atualizar contador
        contadorPergunta.textContent = perguntaAtual + 1;

        // Mostrar/ocultar botões
        btnVoltar.disabled = perguntaAtual === 0;
        
        if (perguntaAtual === totalPerguntas - 1) {
            btnProximo.classList.add('d-none');
            areaEnvio.classList.remove('d-none');
        } else {
            btnProximo.classList.remove('d-none');
            areaEnvio.classList.add('d-none');
        }

        console.log(`📍 Pergunta atual: ${perguntaAtual + 1}/${totalPerguntas}`);
    }

    function mostrarPergunta(index) {
        perguntas.forEach((pergunta, i) => {
            pergunta.classList.toggle('pergunta-ativa', i === index);
            pergunta.classList.toggle('d-none', i !== index);
        });
        perguntaAtual = index;
        atualizarNavegacao();
    }

    function validarPerguntaAtual() {
        const perguntaAtualElement = document.querySelector('.pergunta-ativa');
        if (!perguntaAtualElement) return false;
        
        const perguntaId = perguntaAtualElement.getAttribute('data-id');
        const radios = perguntaAtualElement.querySelectorAll('input[type="radio"]');
        const algumSelecionado = Array.from(radios).some(radio => radio.checked);
        
        if (algumSelecionado) {
            // Salvar a resposta
            const radioSelecionado = perguntaAtualElement.querySelector('input[type="radio"]:checked');
            respostas[perguntaId] = parseInt(radioSelecionado.value);
            console.log(`💾 Salva resposta para pergunta ${perguntaId}: ${respostas[perguntaId]}`);
        }
        
        return algumSelecionado;
    }

    btnProximo.addEventListener('click', function() {
        // Validar se uma opção foi selecionada
        if (!validarPerguntaAtual()) {
            alert('Por favor, selecione uma resposta antes de continuar.');
            return;
        }

        if (perguntaAtual < totalPerguntas - 1) {
            mostrarPergunta(perguntaAtual + 1);
        }
    });

    btnVoltar.addEventListener('click', function() {
        if (perguntaAtual > 0) {
            mostrarPergunta(perguntaAtual - 1);
        }
    });

    // Salvar resposta quando o usuário selecionar uma opção
    document.addEventListener('change', function(e) {
        if (e.target.type === 'radio') {
            const perguntaId = e.target.getAttribute('data-pergunta');
            respostas[perguntaId] = parseInt(e.target.value);
            console.log(`📝 Resposta selecionada - Pergunta ${perguntaId}: ${e.target.value}`);
        }
    });

    // Envio do formulário
    btnEnviar.addEventListener('click', function() {
        // Validar última pergunta
        if (!validarPerguntaAtual()) {
            alert('Por favor, selecione uma resposta antes de enviar.');
            return;
        }

        // Verificar se todas as perguntas foram respondidas
        const respostasArray = [];
        let todasRespondidas = true;
        let primeiraNaoRespondida = -1;

        for (let i = 0; i < perguntas.length; i++) {
            const perguntaId = perguntas[i].getAttribute('data-id');
            if (respostas[perguntaId] === undefined) {
                todasRespondidas = false;
                primeiraNaoRespondida = i;
                break;
            }
            respostasArray.push(respostas[perguntaId]);
        }

        if (!todasRespondidas) {
            alert('Por favor, responda todas as perguntas antes de enviar.');
            mostrarPergunta(primeiraNaoRespondida);
            return;
        }

        console.log('📤 Enviando respostas:', respostasArray);

        // Desabilitar o botão de envio
        btnEnviar.disabled = true;
        btnEnviar.innerHTML = '<i class="bi bi-arrow-repeat spinner me-2"></i>Enviando...';

        // Enviar para o servidor
        fetch('/salvar-resposta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({respostas: respostasArray})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede');
            }
            return response.json();
        })
        .then(data => {
            console.log('✅ Resposta do servidor:', data);
            if (data.success) {
                window.location.href = `/resultado?perfil=${data.perfil}&pontuacao=${data.pontuacao}&descricao=${encodeURIComponent(data.descricao)}`;
            } else {
                alert('Erro: ' + data.error);
                btnEnviar.disabled = false;
                btnEnviar.innerHTML = '<i class="bi bi-check-circle me-2"></i>Finalizar Questionário';
            }
        })
        .catch(error => {
            console.error('❌ Erro no envio:', error);
            alert('Erro ao enviar respostas: ' + error.message);
            btnEnviar.disabled = false;
            btnEnviar.innerHTML = '<i class="bi bi-check-circle me-2"></i>Finalizar Questionário';
        });
    });

    // Inicializar
    if (totalPerguntas > 0) {
        atualizarNavegacao();
        console.log('🎯 Formulário inicializado com sucesso!');
    }
});
