/**
 * Lista os atendimentos do dia em formato de cartões grandes, com filtro
 * por status através de botões (em vez de um select pequeno). Pensado
 * para leitura rápida por atendentes com pouca familiaridade com
 * tecnologia: texto grande, cores de status bem contrastadas.
 */

import React, { useState } from "react";

const FILTROS_STATUS = [
  { valor: null, rotulo: "Todos" },
  { valor: "aguardando", rotulo: "Aguardando" },
  { valor: "em atendimento", rotulo: "Em atendimento" },
  { valor: "finalizado", rotulo: "Finalizado" },
];

const CLASSE_STATUS = {
  aguardando: "status-aguardando",
  "em atendimento": "status-em-atendimento",
  finalizado: "status-finalizado",
};

function ListaAtendimentos({ atendimentos, onFiltrarStatus, statusAtivo, onSelecionarAtendimento }) {
  const [carregando] = useState(false);

  return (
    <div className="lista-atendimentos">
      <h2>Atendimentos do Dia</h2>

      <div className="grade-botoes filtros">
        {FILTROS_STATUS.map((filtro) => (
          <button
            key={filtro.rotulo}
            type="button"
            className={`botao-filtro ${statusAtivo === filtro.valor ? "selecionado" : ""}`}
            onClick={() => onFiltrarStatus(filtro.valor)}
          >
            {filtro.rotulo}
          </button>
        ))}
      </div>

      {carregando && <p>Carregando...</p>}

      {!carregando && atendimentos.length === 0 && (
        <p className="texto-vazio">Nenhum atendimento registrado ainda.</p>
      )}

      <div className="lista-cartoes">
        {atendimentos.map((atendimento) => (
          <button
            key={atendimento.id}
            type="button"
            className="cartao-atendimento"
            onClick={() => onSelecionarAtendimento(atendimento.id)}
          >
            <span className="cartao-nome">{atendimento.nome_paciente}</span>
            <span className="cartao-tipo">{atendimento.tipo_atendimento}</span>
            <span className={`cartao-status ${CLASSE_STATUS[atendimento.status]}`}>
              {atendimento.status}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default ListaAtendimentos;
