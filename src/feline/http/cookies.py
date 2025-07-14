# TODO Organize

from feline.extensions.security.cryptography import decrypt, encrypt


class Cookies:
    def __init__(self, raw_cookies: str) -> None:
        self._raw_cookies: str = raw_cookies
        self._cookies: dict[str,str] = {}
        self._setcookies: dict[str,str] = {}
        self._is_loaded:bool = False

    def _load(self) -> None:
        """Carrega cookies do cabeçalho raw_cookies.
        Essa função se trata de um lazy load para evitar processamento extra em rotas que não necesita de cookies
        """
        if self._is_loaded:
            return # ignore load if loaded

        if self._raw_cookies:
            cookie_pairs: list[str] = self._raw_cookies.split(sep=";")
            for pair in cookie_pairs:
                if "=" in pair:
                    key, value = pair.strip().split(sep="=", maxsplit=1)
                    self._cookies[key] = value  # ainda não decripta
            self._is_loaded = True

    def get(self, key: str) -> str | None:
        """Recupera o valor do cookie e decripta, se existir."""
        self._load()
        if key in self._cookies:
            return decrypt(data=self._cookies[key])
        return None

    def set(
        self,
        key: str,
        value: str,
        expires: str|None = None,
        max_age: int|None = None,
        domain: str|None = None,
        path: str = "/",
        secure: bool = True,
        httponly: bool = True,
        samesite: str = "Strict",
        priority: str = "Medium",
    ) -> None:
        """Configura um cookie, criptografa e armazena."""
        self._load()
        value_encrypted: str = encrypt(data=value)
        self._cookies[key] = value_encrypted

        options = {
            "expires": expires,
            "max_age": max_age,
            "domain": domain,
            "path": path,
            "secure": secure,
            "httponly": httponly,
            "samesite": samesite,
            "priority": priority,
        }

        cookie_str: str = self.create_set_cookie_string(key=key, value=value_encrypted, options=options)
        self._setcookies[key] = cookie_str

    def create_set_cookie_string(self, key: str, value: str, options: dict) -> str:
        """
        Configura um cookie com valores de segurança padrão.

        :param key: Nome do cookie.
        :param value: Valor do cookie (já criptografado).
        :param options: Dicionário com opções de configuração do cookie.
        """
        cookie_str: str = f"{key}={value}"

        # Expiração ou tempo máximo de vida
        if options.get("expires"):
            cookie_str += f"; Expires={options['expires']}"
        if options.get("max_age") is not None:
            cookie_str += f"; Max-Age={options['max_age']}"

        # Domínio e caminho (segurança)
        if options.get("domain"):
            cookie_str += f"; Domain={options['domain']}"
        if options.get("path"):
            cookie_str += f"; Path={options['path']}"

        # Segurança adicional
        if options.get("secure"):
            cookie_str += "; Secure"  # Só será transmitido via HTTPS
        if options.get("httponly"):
            cookie_str += "; HttpOnly"  # Impede acesso via JavaScript
        if options.get("samesite"):
            samesite_val = options["samesite"].capitalize()
            if samesite_val in ["Lax", "Strict", "None"]:
                cookie_str += f"; SameSite={samesite_val}"

        # Prioridade (evita que o cookie seja sobrescrito)
        if options.get("priority"):
            priority_val = options["priority"].capitalize()
            if priority_val in ["Low", "Medium", "High"]:
                cookie_str += f"; Priority={priority_val}"

        return cookie_str

    def get_headers_of_cookie_to_set(self) -> list[tuple[bytes, bytes]]:
        headers: list[tuple[bytes, bytes]] = []
        for value in self._setcookies.values():
            headers.append((b"set-cookie", value.encode(encoding="utf-8")))
        return headers
