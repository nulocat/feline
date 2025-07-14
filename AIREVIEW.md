# AIREVIEW

Este documento é um  review de uma versão de aproximadamente 03/25, seu objetivo é fazer dump das criticas de uma GPT sobre o projeto, indicando ao dev coisas que ele pode dar uma olhada

---

### `./__about__.py`

Este arquivo está **OK** para a versão 1.0.0. Ele define a versão do pacote e as informações de licença, o que é fundamental. No entanto, lembre-se de **atualizar a versão para `1.0.0`** quando estiver pronto para o lançamento.

---

### `./application.py`

Este é um dos corações do Feline.

* **Tratamento de Exceções (`exception_handles` e `__call__` `except` block):**
    * **Prioridade Alta:** Atualmente, o bloco `except` no `__call__` simplesmente itera sobre `exception_handles` e, se não encontra um handler customizado, **re-lança a exceção**. Para a v1.0.0, é **crucial** ter um fallback robusto. Mesmo que seja um `server_error()` padrão para exceções não tratadas, ele deve evitar que o servidor caia. A linha `# TEMP, future handle erro` indica isso.
    * **Ação:** Implemente a lógica para que, se nenhuma exceção for capturada por `self.exception_handles`, um `Response` de erro (e.g., `server_error()`) seja retornado em vez de re-lançar a exceção, o que derrubaria o servidor ASGI.

* **`handle_request` - Respostas:**
    * A lógica de inferência de resposta (HTML, JSON, Text) é boa. Certifique-se de que a ordem e as condições de `isinstance` sejam à prova de falhas para evitar retornos inesperados.

* **`handle_lifespan`:**
    * A funcionalidade básica está presente. Comentários como `# app init (nothing for now)` e `# app save kill (nothing for now)` sugerem que pode haver funcionalidades futuras aqui, mas para a v1.0.0, está **OK**.

* **`run` method:**
    * Este método duplica parte da lógica de inicialização do servidor que já existe no CLI (`cli/__init__.py`).
    * **Ação:** Considere se o método `run` da classe `Feline` é estritamente necessário. Se a ideia é que o framework seja rodado principalmente via CLI (`feline run`), esta duplicação pode ser eliminada para manter uma única fonte de verdade para o bootstrapping da aplicação. Se for mantido, garanta que ambos usem a mesma lógica robusta de tratamento de erros e importação.

* **Geral:** O design com `get`, `post` e `onerror` como decoradores na própria instância da aplicação é intuitivo para um micro-framework.

---

### `./cli/__init__.py`

Este arquivo é o **CLI** do Feline.

* **Comando `run`:**
    * **Ponto de Melhoria:** Há uma duplicidade na forma como a aplicação é importada e rodada. O `application.py` tem um método `run`, e o CLI também lida com a importação e o `uvicorn.run`.
    * **Ação:** Padronize a importação e o `run`. O ideal seria que o CLI importasse a aplicação e então chamasse o método `run` da instância de `Feline` (se você decidir mantê-lo), ou que a lógica de inicialização do Uvicorn fosse primariamente no CLI.
    * O `console.print_exception()` pode ser útil para debug, mas em um CLI para usuário final, talvez um erro mais amigável seja preferível.

* **Comando `init`:**
    * **OK:** A funcionalidade de criação de projeto básico está clara e útil. A adição do `secret_key = 'CHANGE_ME!'` é uma boa prática.

* **Comando `clean`:**
    * **OK:** Funcionalidade útil para limpeza. O comentário "`Nan bro meus olhos ardem quando eu dou tree`" é divertido, mas pode ser removido ou substituído por algo mais "profissional" se quiser manter o código mais formal.

* **Comandos `info` e `version`:**
    * **OK:** Úteis para depuração e para o usuário verificar as versões. A lógica de obter a versão local e do PyPI é bem implementada.

* **Geral:** O uso de `rich-click` é excelente para um CLI amigável.

---

### `./config.py`

* **OK:** A classe `Config` com `__getattr__` e `__setattr__` para acesso a atributos é um padrão flexível e parece bem implementada para um micro-framework. A geração de uma `secret_key` padrão aleatória é ótima para segurança.

---

### `./context/__init__.py`

* **OK, mas Refinar:** O uso de `ContextVar` é a maneira correta de lidar com contexto por requisição em ASGI, o que é um ponto forte.
* **Ponto de Atenção:** A classe `GlobalObject` e o `_ctx_global.set(GlobalObject())` são bons para um escopo global. No entanto, é importante garantir que o **ciclo de vida** desse `GlobalObject` esteja bem definido para evitar vazamentos de memória ou dados incorretos entre requisições em ambientes assíncronos. Atualmente, `_ctx_global` é setado uma única vez na inicialização do módulo, o que o torna verdadeiramente global e não por requisição. Se a intenção é ter um objeto global para a aplicação inteira (e não por requisição), está correto. Se a ideia é ter um objeto "g" por requisição, então ele precisaria ser resetado ou instanciado por requisição no `request_context_window`. No momento, parece ser global, o que está OK para um `g` global.

---

### `./context/manager.py`

* **Crítico:** Este é o ponto onde o contexto de cada requisição é estabelecido.
* **Ponto de Melhoria:** O `context.cookies` é preenchido com `decode("latin1")`. Certifique-se de que a codificação `latin1` é a mais apropriada para todos os cenários de cookies que você espera. `UTF-8` é mais comum para conteúdo geral da web e pode ser mais seguro para cookies que contenham caracteres não-ASCII, embora cookies geralmente sejam mais restritos.
* **Ação:** Verifique a padronização da codificação de cookies. Se for apenas `latin1` é um ponto de atenção, se for para mudar para `utf-8` verifique a compatibilidade.
* **Geral:** A utilização de `asynccontextmanager` é a abordagem correta.

---

### `./exceptions.py`

* **OK:** As classes de exceção são bem definidas e fornecem mensagens úteis para depuração. A exceção `InvalidParameterResolution` é particularmente boa para indicar problemas na resolução de rotas.

---

### `./extensions/security/cryptography.py`

* **Refatorar / Ponto de Atenção:**
    * A função `base64_key_transformer` gera uma chave Fernet usando SHA256 e Base64 URL-safe. Embora funcione, **Fernet requer chaves de 32 bytes de alta entropia**. Gerar a chave a partir de um `secret` de string arbitrária usando SHA256 pode não ser a melhor prática para gerar uma chave criptográfica forte. O ideal seria usar `os.urandom(32)` ou `Fernet.generate_key()` para gerar a chave e então armazená-la de forma segura. Se o `secret_key` da configuração for a única fonte, ele deve ser robusto.
    * **Ação:** Revise a geração e o uso da chave para `Fernet`. Idealmente, a `secret_key` da Config deveria ser a chave Fernet completa (gerada com `Fernet.generate_key()`) ou um valor de alta entropia para derivá-la de forma segura.
    * **Ponto de Melhoria:** Adicione tratamento para erros de decriptografia (e.g., `InvalidToken`). Atualmente, `decrypt` irá levantar a exceção se o token for inválido, o que pode não ser o comportamento desejado para cookies ou outros dados criptografados que podem estar corrompidos ou adulterados.

---

### `./extensions/security/__init__.py`

* **OK:** O módulo de segurança para hashing de senhas (`secure_hash`, `hash_check`) parece bem implementado, seguindo boas práticas como PBKDF2 com salt e iterações.
* **Ponto de Atenção:** A `AlgorithmNotSupported` é uma boa adição. A lista `SUPPORTED_ALGORITHMS` está explícita.
* **Geral:** É um bom começo para utilitários de segurança.

---

### `./extensions/utils/__init__.py`

* **OK:** Este arquivo é apenas um `__init__.py` para exportar a função `render`. Nada a mudar aqui.

---

### `./extensions/utils/render.py`

* **OK:** A integração com Jinja2 para renderização de templates é funcional.
* **Ponto de Melhoria:** A criação de um novo `Environment` a cada chamada de `render` pode ser ineficiente em cenários de alta carga, pois o `FileSystemLoader` é instanciado repetidamente.
* **Ação:** Considere instanciar o `Environment` uma vez na inicialização da aplicação (talvez na classe `Feline` ou como uma variável global) e passá-lo para a função `render`, ou armazená-lo em cache. Isso melhoraria a performance.
* A passagem do `request` para o contexto do template é útil.

---

### `./http/cookies.py`

* **Refatorar/Ponto de Atenção:**
    * O `TODO Organize` é um bom lembrete. A lógica de `_load` é ok para lazy loading.
    * **Codificação de Cookies:** Similar ao `context/manager.py`, a decodificação inicial de `_raw_cookies` e a codificação final em `get_headers_of_cookie_to_set` usam `latin1` ou `utf-8` sem uma política clara. **A RFC 6265 para cookies desencoraja caracteres não-ASCII.** No entanto, se você suporta valores arbitrários, o ideal é ter certeza de que a codificação é consistente e segura. `UTF-8` é geralmente a melhor aposta se você precisa suportar esses caracteres, mas requer que o cliente e o servidor esperem isso.
    * **Ação:** Decida uma política clara de codificação para valores de cookies. Se for apenas caracteres ASCII seguros, `latin1` pode funcionar, mas `utf-8` é mais universal. Se permitir caracteres especiais, considere codificá-los (e.g., URL-encode) antes de criptografar.
    * **Criptografia:** O `get()` e `set()` dos cookies dependem diretamente das funções `encrypt` e `decrypt` do módulo `cryptography`. Isso está bom, mas a refatoração sugerida para a geração da chave em `cryptography.py` afetará este arquivo.

---

### `./http/request.py`

* **OK:** A classe `Request` é um bom wrapper para o escopo ASGI. O lazy loading de `body`, `json`, `form` e `text` é uma boa prática para evitar processamento desnecessário.
* **Ponto de Atenção:**
    * A decodificação dos headers (`k.decode(encoding="latin1").lower()`) usando `latin1` para chaves e valores pode ser um problema se os headers contiverem caracteres não-ASCII, embora isso seja raro para nomes de headers. Para valores de headers, pode ser um problema.
    * `_parse_query_params` assume `utf-8` para a query string, o que é a prática padrão e está correto.
    * A extração de `host` e `port` do `scope["client"]` com fallback para `("Unknow",0)` é robusta.
* **Geral:** Parece um arquivo sólido e bem pensado.

---

### `./http/response.py`

* **OK:** A classe `Response` é funcional e flexível, permitindo construir diferentes tipos de respostas (JSON, HTML, Texto).
* **Ponto de Melhoria:**
    * A função `get_headers()` codifica os headers de string para bytes usando `latin1` para chaves e valores, exceto para `content-length` e `set-cookie`.
    * **Ação:** Similar ao `Request` e `Cookies`, revise a consistência e correção da codificação de headers. `UTF-8` é geralmente preferível para valores de headers que podem conter caracteres especiais.
    * As funções auxiliares (`redirect`, `html`, `json_response`, `text`, `bad_request`, `not_found`, etc.) são muito úteis e mantêm o código limpo.
* **Geral:** Uma base sólida para manipulação de respostas.

---

### `./__init__.py`

* **OK:** Este arquivo é o principal `__init__.py` do pacote e define o que será importável diretamente de `feline`. A exportação de `Feline`, `context`, `Request`, `Cookies` e `Response` está adequada para o uso do framework.

---

### `./__main__.py`

* **OK:** Essencial para permitir que o Feline seja executado como um módulo (`python -m feline`).

---

### `./middleware/__init__.py`

* **OK, mas em Desenvolvimento:** A estrutura de middleware `MidwareBase` é promissora e mostra um bom entendimento do padrão ASGI.
* **Ponto de Melhoria:** Atualmente, não há um mecanismo para **registrar** e **aplicar** esses middlewares globalmente na aplicação (ex: na classe `Feline`). O código mostra como um middleware funcionaria se fosse um decorador diretamente em uma rota, mas não como ele seria aplicado a todas as rotas ou a um grupo delas.
* **Ação:** Para a v1.0.0, você precisa decidir se o sistema de middleware é um MVP funcional. Se for, implemente a integração na classe `Feline` para que os middlewares possam ser adicionados e processados durante o ciclo de requisição/resposta (antes de `handle_request` e depois do retorno). Se não, considere adiar a funcionalidade de middleware para uma versão futura e removê-la temporariamente do código para não ter "coisas incompletas" na V1.0.0.

---

### `./routing/parameters.py`

* **OK:** As classes `Query`, `Form`, `Body` são excelentes para tipagem e documentação de parâmetros de rota, similar a frameworks como FastAPI.
* **Ponto de Melhoria:** Para a V1.0.0, é crucial que o `resolver.py` consiga interpretar e usar essas classes corretamente para extrair os dados da requisição.

---

### `./routing/resolver.py`

* **Crítico e Incompleto:** Este arquivo é fundamental para o funcionamento do roteamento e da injeção de dependência/resolução de parâmetros. Atualmente, ele só possui a função `get_params`.
* **Prioridade Altíssima:** Você precisa implementar a lógica para:
    1.  **Resolver parâmetros de rota:** Extrair valores da URL (`/users/{id}`).
    2.  **Resolver parâmetros de consulta (Query):** Usar `request.args` e lidar com os defaults.
    3.  **Resolver parâmetros de formulário (Form):** Usar `request.form` e lidar com os defaults.
    4.  **Resolver parâmetros de corpo (Body):** Usar `request.json` ou `request.text` e lidar com os defaults e o tipo (`JSON`, `TEXT`).
    5.  **Injetar `Request`, `Response`, `Cookies`, `Config`, `GlobalObject`:** A injeção automática de `context.request`, `context.cookies`, etc., baseada na anotação de tipo do handler.
    6.  **Tratamento de tipos:** Garantir que o tipo inferido ou especificado para os parâmetros (`int`, `str`, `bool`, etc.) seja respeitado e que `InvalidParameterResolution` seja levantada quando houver um mismatch.
* **Ação:** Este arquivo é o principal foco para ter um MVP funcional. Sem ele, a injeção de parâmetros e a extração de dados da requisição não funcionarão como esperado.



