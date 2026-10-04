/**
 * Cliente HTTP centralizado para falar com a API de atendimentos.
 *
 * Todo o resto do frontend chama estas funções em vez de usar axios
 * diretamente — assim nenhuma URL de endpoint fica "solta" espalhada
 * pelos componentes, e se a URL base da API mudar, o ajuste é feito
 * em um único lugar.
 */

import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

/** Lista os atendimentos, opcionalmente filtrando por status. */
export async function listarAtendimentos(status) {
  const params = status ? { status } : {};
  const resposta = await api.get("/atendimentos", { params });
  return resposta.data;
}

/** Busca os detalhes de um atendimento pelo id. */
export async function buscarAtendimento(id) {
  const resposta = await api.get(`/atendimentos/${id}`);
  return resposta.data;
}

/** Registra um novo atendimento. */
export async function criarAtendimento(atendimento) {
  const resposta = await api.post("/atendimentos", atendimento);
  return resposta.data;
}

/** Atualiza um atendimento existente (ex.: mudança de status). */
export async function atualizarAtendimento(id, atendimento) {
  const resposta = await api.put(`/atendimentos/${id}`, atendimento);
  return resposta.data;
}

/** Remove um registro de atendimento. */
export async function removerAtendimento(id) {
  const resposta = await api.delete(`/atendimentos/${id}`);
  return resposta.data;
}

export default api;
