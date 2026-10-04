/**
 * Tela de detalhes de um atendimento: mostra os dados do registro e
 * permite avançar o status (aguardando -> em atendimento -> finalizado)
 * ou excluir o registro, com botões grandes e confirmação visual.
 */

import React, { useEffect, useState } from "react";
import { buscarAtendimento, atualizarAtendimento, removerAtendimento } from "../services/api";

const STATUS_VALIDOS = ["aguardando", "em atendimento", "finalizado"];

function DetalheAtendimento({ atendimentoId, onVoltar, onAtendimentoAtualizado, onAtendimentoRemovido }) {
  const [atendimento, setAtendimento] = useState(null);
  const [mensagem, setMensagem] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    carregarAtendimento();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [atendimentoId]);

  async function carregarAtendimento() {
    setCarregando(true);
    try {
      const dados = await buscarAtendimento(atendimentoId);
      setAtendimento(dados);
    } catch (erro) {
      setMensagem({ tipo: "erro", texto: "Não foi possível carregar este atendimento." });
    } finally {
      setCarregando(false);
    }
  }

  async function handleMudarStatus(novoStatus) {
    setMensagem(null);
    try {
      const atualizado = await atualizarAtendimento(atendimentoId, {
        ...atendimento,
        status: novoStatus,
      });
      setAtendimento(atualizado);
      onAtendimentoAtualizado(atualizado);
      setMensagem({ tipo: "sucesso", texto: "Status atualizado com sucesso!" });
    } catch (erro) {
      setMensagem({ tipo: "erro", texto: "Não foi possível atualizar o status." });
    }
  }

  async function handleExcluir() {
    const confirmou = window.confirm("Tem certeza que deseja excluir este atendimento?");
    if (!confirmou) return;

    try {
      await removerAtendimento(atendimentoId);
      onAtendimentoRemovido(atendimentoId);
    } catch (erro) {
      setMensagem({ tipo: "erro", texto: "Não foi possível excluir o atendimento." });
    }
  }

  if (carregando) {
    return <p>Carregando atendimento...</p>;
  }

  if (!atendimento) {
    return (
      <div className="detalhe-atendimento">
        <p className="feedback feedback-erro">Atendimento não encontrado.</p>
        <button type="button" className="botao-secundario" onClick={onVoltar}>
          Voltar
        </button>
      </div>
    );
  }

  return (
    <div className="detalhe-atendimento">
      <h2>Detalhes do Atendimento</h2>

      <div className="detalhe-linha">
        <span className="detalhe-rotulo">Paciente</span>
        <span className="detalhe-valor">{atendimento.nome_paciente}</span>
      </div>
      <div className="detalhe-linha">
        <span className="detalhe-rotulo">Tipo</span>
        <span className="detalhe-valor">{atendimento.tipo_atendimento}</span>
      </div>
      <div className="detalhe-linha">
        <span className="detalhe-rotulo">Registrado em</span>
        <span className="detalhe-valor">{atendimento.data_hora}</span>
      </div>

      {mensagem && (
        <div className={`feedback feedback-${mensagem.tipo}`}>
          {mensagem.tipo === "sucesso" ? "✔ " : "⚠ "}
          {mensagem.texto}
        </div>
      )}

      <p className="rotulo-grande">Alterar status</p>
      <div className="grade-botoes">
        {STATUS_VALIDOS.map((status) => (
          <button
            key={status}
            type="button"
            className={`botao-opcao ${atendimento.status === status ? "selecionado" : ""}`}
            onClick={() => handleMudarStatus(status)}
          >
            {status}
          </button>
        ))}
      </div>

      <div className="acoes-detalhe">
        <button type="button" className="botao-secundario" onClick={onVoltar}>
          Voltar para a lista
        </button>
        <button type="button" className="botao-perigo" onClick={handleExcluir}>
          Excluir Atendimento
        </button>
      </div>
    </div>
  );
}

export default DetalheAtendimento;
