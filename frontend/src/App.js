/**
 * Componente raiz da aplicação.
 *
 * Fluxo linear e simples, pensado para atendentes com pouca
 * familiaridade com tecnologia: uma navbar com apenas duas opções
 * ("Início" e "Novo Registro") e uma tela de detalhes acessada a partir
 * da lista. Não há menus escondidos nem múltiplos cliques necessários.
 */

import React, { useEffect, useState } from "react";
import "./App.css";
import FormAtendimento from "./components/FormAtendimento";
import ListaAtendimentos from "./components/ListaAtendimentos";
import DetalheAtendimento from "./components/DetalheAtendimento";
import { listarAtendimentos } from "./services/api";

const TELAS = {
  INICIO: "inicio",
  NOVO_REGISTRO: "novo_registro",
  DETALHE: "detalhe",
};

function App() {
  const [tela, setTela] = useState(TELAS.INICIO);
  const [atendimentos, setAtendimentos] = useState([]);
  const [statusAtivo, setStatusAtivo] = useState(null);
  const [atendimentoSelecionadoId, setAtendimentoSelecionadoId] = useState(null);
  const [erroCarregamento, setErroCarregamento] = useState(null);

  useEffect(() => {
    carregarAtendimentos(statusAtivo);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusAtivo]);

  async function carregarAtendimentos(status) {
    try {
      const dados = await listarAtendimentos(status);
      setAtendimentos(dados);
      setErroCarregamento(null);
    } catch (erro) {
      setErroCarregamento("Não foi possível carregar os atendimentos. Verifique se a API está rodando.");
    }
  }

  function handleAtendimentoCriado(atendimentoCriado) {
    setAtendimentos((atual) => [atendimentoCriado, ...atual]);
    setTela(TELAS.INICIO);
  }

  function handleAtendimentoAtualizado(atendimentoAtualizado) {
    setAtendimentos((atual) =>
      atual.map((item) => (item.id === atendimentoAtualizado.id ? atendimentoAtualizado : item))
    );
  }

  function handleAtendimentoRemovido(idRemovido) {
    setAtendimentos((atual) => atual.filter((item) => item.id !== idRemovido));
    setTela(TELAS.INICIO);
  }

  function handleSelecionarAtendimento(id) {
    setAtendimentoSelecionadoId(id);
    setTela(TELAS.DETALHE);
  }

  return (
    <div className="App">
      <nav className="navbar">
        <span className="navbar-titulo">Posto de Saúde — Atendimentos</span>
        <div className="navbar-botoes">
          <button
            type="button"
            className={`botao-nav ${tela === TELAS.INICIO ? "ativo" : ""}`}
            onClick={() => setTela(TELAS.INICIO)}
          >
            Início
          </button>
          <button
            type="button"
            className={`botao-nav ${tela === TELAS.NOVO_REGISTRO ? "ativo" : ""}`}
            onClick={() => setTela(TELAS.NOVO_REGISTRO)}
          >
            Novo Registro
          </button>
        </div>
      </nav>

      <main>
        {erroCarregamento && <p className="feedback feedback-erro">{erroCarregamento}</p>}

        {tela === TELAS.INICIO && (
          <ListaAtendimentos
            atendimentos={atendimentos}
            statusAtivo={statusAtivo}
            onFiltrarStatus={setStatusAtivo}
            onSelecionarAtendimento={handleSelecionarAtendimento}
          />
        )}

        {tela === TELAS.NOVO_REGISTRO && <FormAtendimento onAtendimentoCriado={handleAtendimentoCriado} />}

        {tela === TELAS.DETALHE && (
          <DetalheAtendimento
            atendimentoId={atendimentoSelecionadoId}
            onVoltar={() => setTela(TELAS.INICIO)}
            onAtendimentoAtualizado={handleAtendimentoAtualizado}
            onAtendimentoRemovido={handleAtendimentoRemovido}
          />
        )}
      </main>
    </div>
  );
}

export default App;
