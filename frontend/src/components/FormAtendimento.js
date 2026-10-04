/**
 * Formulário de registro de um novo atendimento.
 *
 * Pensado para atendentes com pouca familiaridade com tecnologia:
 * apenas dois campos (nome do paciente e tipo de atendimento), o tipo é
 * escolhido por botões grandes (não por texto livre) e o feedback de
 * sucesso/erro é grande e visível.
 */

import React, { useState } from "react";
import { criarAtendimento } from "../services/api";

const TIPOS_ATENDIMENTO = ["Consulta Geral", "Vacinação", "Curativo", "Encaminhamento"];

function FormAtendimento({ onAtendimentoCriado }) {
  const [nomePaciente, setNomePaciente] = useState("");
  const [tipoSelecionado, setTipoSelecionado] = useState(null);
  const [mensagem, setMensagem] = useState(null);
  const [enviando, setEnviando] = useState(false);

  async function handleRegistrar() {
    setMensagem(null);

    if (!nomePaciente.trim()) {
      setMensagem({ tipo: "erro", texto: "Digite o nome do paciente." });
      return;
    }
    if (!tipoSelecionado) {
      setMensagem({ tipo: "erro", texto: "Escolha o tipo de atendimento." });
      return;
    }

    setEnviando(true);
    try {
      const atendimentoCriado = await criarAtendimento({
        nome_paciente: nomePaciente.trim(),
        tipo_atendimento: tipoSelecionado,
        status: "aguardando",
      });
      onAtendimentoCriado(atendimentoCriado);
      setMensagem({ tipo: "sucesso", texto: "Atendimento registrado com sucesso!" });
      setNomePaciente("");
      setTipoSelecionado(null);
    } catch (erro) {
      const texto = erro.response?.data?.erro || "Não foi possível registrar o atendimento.";
      setMensagem({ tipo: "erro", texto });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="form-atendimento">
      <h2>Novo Registro de Atendimento</h2>

      <label className="campo-grande">
        Nome do paciente
        <input
          type="text"
          value={nomePaciente}
          onChange={(evento) => setNomePaciente(evento.target.value)}
          placeholder="Digite o nome completo"
        />
      </label>

      <p className="rotulo-grande">Tipo de atendimento</p>
      <div className="grade-botoes">
        {TIPOS_ATENDIMENTO.map((tipo) => (
          <button
            key={tipo}
            type="button"
            className={`botao-opcao ${tipoSelecionado === tipo ? "selecionado" : ""}`}
            onClick={() => setTipoSelecionado(tipo)}
          >
            {tipo}
          </button>
        ))}
      </div>

      {mensagem && (
        <div className={`feedback feedback-${mensagem.tipo}`}>
          {mensagem.tipo === "sucesso" ? "✔ " : "⚠ "}
          {mensagem.texto}
        </div>
      )}

      <button type="button" className="botao-primario" onClick={handleRegistrar} disabled={enviando}>
        {enviando ? "Registrando..." : "Registrar Atendimento"}
      </button>
    </div>
  );
}

export default FormAtendimento;
