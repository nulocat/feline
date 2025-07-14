# Documento

este documento se trata de uma revisão gerada aproximadamente 03/25, sua utilidade é ser um panorama de issues do projeto

## Tree

```python
./
├── __about__.py    # version, pip meta
│
├── __init__.py     # shortcuts imports (i think it drecraptate)
│
├── __main__.py     # call cli (shortcut)
│
├── application.py  # core of framework
├── config.py       # config class
├── exceptions.py   # project custom exceptions
│
├── structures.py   # has only one structure maybe AttributeDict
│
├── cli/
│   └── __init__.py # ALL FUCK CODE OF CLI """VERY UGLY""" """TOP 1 UGLY"""
│
├── context/
│   ├── __init__.py
│   └── manager.py
│
├── extensions/     # Feline Extensions
│   ├── security/   # Security """WE NEED ORGANIZE A BIT"""
│   │   ├── cryptography.py # bunch of functions to make encrypt with fennet
│   │   └── __init__.py     # bunch of functions to secure hash and passwords
│   │
│   └── utils/      # Utils """NOT HAVE A PROPOSE"""
│       ├── __init__.py # Useless file 
│       └── render.py   # ALL jinja render here """WARNING it is imported by core i think"""
│
├── http/           # http
│   ├── cookies.py      # missing delete cookie Yeah
│   ├── request.py      # GOOD
│   └── response.py     # """UGLY"""
│
├── middleware/
│   └── __init__.py # Yeah it is very basic, but good
│
├── routing/
│   ├── parameters.py # ok very basic
│   ├── resolver.py # """LINGUIÇÃO DE IFs""" """UGLY"""
│   └── router.py # ok can survive next day
│
└── shortcuts/ 
    ├── __init__.py     # links -> from many parts of project """CORE HAS REQUIRING A OPTIONAL, IT IMPORT RENDER, BUT RENDER IS OPTIONAL"""
    └── parameters.py   # links -> routing/parameters

```

## ISSUES

- ERROR CONTROL (atualmente erros quebram o app sem @app.onerror)
- CLI CODE IS CHAOTIC (one file foda, hard de manter)
- RESPONSE IS UGLY (bagunçado, code smells e talvés código duplicado)
- ROUTER.RESOLVER = LINGUIÇÃO DE IFs (refactor pra algo mais legível)
- SHORTCUTS IMPORTA RENDER (core dependente de opcional é veneno)
- EXTENSIONS/UTILS SEM PROPÓSITO (antes ela cuidava do security mas security virou core e UTILS ficou sozinho com RENDER)

## TODO

### Críticos

- [ ] Criar sistema de tratamento de erro centralizado (@app.onerror)
- [ ] Tornar request headers case-insensitive
- [ ] Refatorar response.py para separar serialização de lógica de resposta
- [ ] Separar render do core — transformar em extension real

### Refatorações úteis

- [ ] Refatorar cli/__init__.py em múltiplos comandos/modularizar
- [ ] Reescrever resolver.py com dicionário de handlers ou FSM-like
- [ ] Documentar lifecycle de uma requisição (entrada -> saída)

### Qualidade de vida

- [ ] Adicionar logs com cor e nível (info, warn, error)
- [ ] Implementar teste simples (ex: assert status 200 numa rota)
- [ ] Esboçar uma extensão de autenticação (JWT ou session)
