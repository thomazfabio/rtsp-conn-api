Em JavaScript, a melhor abordagem depende do que exatamente você quer fazer. Aqui estão as equivalências das funções `filter()`, `map()` e uma alternativa com `reduce()` para selecionar dados específicos de um objeto ou array de objetos.

---

### 🎯 **Se você tem um objeto e quer extrair apenas algumas chaves específicas**
Use **Object.entries() + filter() + Object.fromEntries()**:

```javascript
const dados = {
    id: 123,
    nome: "João",
    idade: 25,
    email: "joao@email.com",
    ativo: true
};

const chavesDesejadas = ["id", "nome"];
const dadosFiltrados = Object.fromEntries(
    Object.entries(dados).filter(([key]) => chavesDesejadas.includes(key))
);

console.log(dadosFiltrados);
// Saída: { id: 123, nome: 'João' }
```

---

### 🎯 **Se você tem um array de objetos e quer filtrar com base em uma condição**
Use **`filter()`**:

```javascript
const usuarios = [
    { id: 1, nome: "Ana", idade: 17 },
    { id: 2, nome: "Carlos", idade: 22 },
    { id: 3, nome: "Bruna", idade: 30 }
];

const maioresDeIdade = usuarios.filter(u => u.idade >= 18);

console.log(maioresDeIdade);
// Saída: [{ id: 2, nome: 'Carlos', idade: 22 }, { id: 3, nome: 'Bruna', idade: 30 }]
```

---

### 🎯 **Se você quer transformar os dados (exemplo: pegar só os nomes)**
Use **`map()`**:

```javascript
const nomes = usuarios.map(u => u.nome);

console.log(nomes);
// Saída: ['Ana', 'Carlos', 'Bruna']
```

---

### 🎯 **Se você quer extrair algumas chaves de cada objeto no array**
Use **`map()`** com desestruturação:

```javascript
const usuariosResumidos = usuarios.map(({ id, nome }) => ({ id, nome }));

console.log(usuariosResumidos);
// Saída: [{ id: 1, nome: 'Ana' }, { id: 2, nome: 'Carlos' }, { id: 3, nome: 'Bruna' }]
```

---