const API_URL = "/api/tasks";
 
const form = document.getElementById("form-tarefa");
const input = document.getElementById("input-tarefa");
const lista = document.getElementById("lista-tarefas");
 
 
async function carregarTarefas() {
  try {
    const res = await fetch(API_URL);
 
    if (!res.ok) {
      throw new Error("Erro ao carregar tarefas");
    }
 
    const tarefas = await res.json();
    renderizar(tarefas);
 
  } catch (erro) {
    console.error("Erro:", erro);
  }
}
 
 
function renderizar(tarefas) {
  lista.innerHTML = "";
 
  tarefas.forEach((tarefa) => {
    const li = document.createElement("li");
 
    li.className = "tarefa" + (tarefa.done ? " concluida" : "");
 
    li.innerHTML = `
      <input type="checkbox" ${tarefa.done ? "checked" : ""}>
      <span></span>
      <button class="btn-excluir" title="Excluir">✕</button>
    `;
 
    const span = li.querySelector("span");
 
    if (tarefa.done) {
      const riscado = document.createElement("s");
      riscado.textContent = tarefa.title;
      span.appendChild(riscado);
    } else {
      span.textContent = tarefa.title;
    }
 
 
    li.querySelector("input").addEventListener("change", async (e) => {
      await atualizarTarefa(tarefa.id, {
        done: e.target.checked
      });
    });
 
 
    li.querySelector(".btn-excluir").addEventListener("click", async () => {
      await excluirTarefa(tarefa.id);
    });
 
 
    lista.appendChild(li);
  });
}
 
 
async function criarTarefa(title) {
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title: title
      }),
    });
 
 
    if (!res.ok) {
      throw new Error("Erro ao criar tarefa");
    }
 
 
    await carregarTarefas();
 
  } catch (erro) {
    console.error("Erro:", erro);
  }
}
 
 
async function atualizarTarefa(id, dados) {
  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados),
    });
 
 
    if (!res.ok) {
      throw new Error("Erro ao atualizar tarefa");
    }
 
 
    await carregarTarefas();
 
  } catch (erro) {
    console.error("Erro:", erro);
  }
}
 
 
async function excluirTarefa(id) {
  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: "DELETE"
    });
 
 
    if (!res.ok && res.status !== 204) {
      throw new Error("Erro ao excluir tarefa");
    }
 
 
    await carregarTarefas();
 
  } catch (erro) {
    console.error("Erro:", erro);
  }
}
 
 
form.addEventListener("submit", async (e) => {
  e.preventDefault();
 
  const titulo = input.value.trim();
 
  if (!titulo) {
    return;
  }
 
 
  await criarTarefa(titulo);
 
  input.value = "";
});
 
 
carregarTarefas();
