Loja PC Gamer PRO

Este é um sistema simples de loja virtual para venda de componentes de PC Gamer, desenvolvido em Python usando Tkinter para a interface gráfica.

Funcionalidades:
- Cadastro e login de usuários (armazenados em `usuarios.json`).
- Visualização dos produtos disponíveis (dados em `produtos.json`).
- Adição e remoção de produtos no carrinho.
- Finalização da compra com registro do pedido em arquivo `.txt`.
- Interface intuitiva e responsiva com navegação por telas.
- Animação de títulos e efeitos visuais para melhor experiência do usuário.

Como usar:
1. Certifique-se de ter o Python 3 instalado.
2. Instale a biblioteca Pillow (para manipulação de imagens):


3. Baixe ou clone este repositório.
4. Coloque as imagens dos produtos na pasta `imagens` (exemplo: `rtx3070.png`, `i9.png`).
5. Execute o arquivo principal:


6. Faça login com usuário padrão:
   - Usuário: `admin`
   - Senha: `1234`

7. Ou cadastre um novo usuário.

Estrutura dos arquivos JSON:
- `usuarios.json`: armazena usuários e senhas em formato `{ "usuario": "senha" }`.
- `produtos.json`: lista de produtos com campos: `nome`, `descricao`, `preco`, `imagem`.

Personalização:
- Para adicionar produtos, edite `produtos.json` com os dados desejados e coloque a imagem correspondente na pasta `imagens`.
- Para adicionar mais funcionalidades, basta editar o código fonte.

Tecnologias usadas:
- Python 3
- Tkinter (interface gráfica)
- Pillow (manipulação de imagens)
- JSON (armazenamento simples de dados)

Autor:
Desenvolvido por Bruno Fernandes.

Licença:
Projeto livre para uso e aprendizado.

