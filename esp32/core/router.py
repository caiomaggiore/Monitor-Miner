# ============================================================================
# ROUTER - Monitor Miner v4.0
# ============================================================================
# Sistema de roteamento HTTP
# - Mapeamento de rotas
# - Middleware support
# - Controllers integration
# ============================================================================

import re

# MicroPython não tem urllib.parse, implementar unquote manualmente
def unquote(string):
    """Decodifica URL encoding (implementação básica para MicroPython)"""
    if not string:
        return string
    
    # Substituições básicas
    string = string.replace('%20', ' ')
    string = string.replace('%21', '!')
    string = string.replace('%22', '"')
    string = string.replace('%23', '#')
    string = string.replace('%24', '$')
    string = string.replace('%25', '%')
    string = string.replace('%26', '&')
    string = string.replace('%27', "'")
    string = string.replace('%28', '(')
    string = string.replace('%29', ')')
    string = string.replace('%2B', '+')
    string = string.replace('%2C', ',')
    string = string.replace('%2F', '/')
    string = string.replace('%3A', ':')
    string = string.replace('%3B', ';')
    string = string.replace('%3C', '<')
    string = string.replace('%3D', '=')
    string = string.replace('%3E', '>')
    string = string.replace('%3F', '?')
    string = string.replace('%40', '@')
    string = string.replace('%5B', '[')
    string = string.replace('%5C', '\\')
    string = string.replace('%5D', ']')
    string = string.replace('%5E', '^')
    string = string.replace('%5F', '_')
    string = string.replace('%60', '`')
    string = string.replace('%7B', '{')
    string = string.replace('%7C', '|')
    string = string.replace('%7D', '}')
    string = string.replace('%7E', '~')
    
    return string

class Router:
    """
    Sistema de roteamento HTTP
    - Mapeamento de rotas para controllers
    - Suporte a parâmetros dinâmicos
    - Middleware pipeline
    """
    
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'PUT': {},
            'DELETE': {}
        }
        self.middleware = []
        print("[ROUTER] ✅ Router inicializado")
    
    def add_route(self, method, path, handler, name=None):
        """
        Adiciona uma rota
        - method: GET, POST, PUT, DELETE
        - path: /api/sensors, /dashboard, etc.
        - handler: função que processa a requisição
        - name: nome opcional da rota
        """
        if method not in self.routes:
            self.routes[method] = {}
        
        # Converter path com parâmetros para regex
        regex_path = self._path_to_regex(path)
        
        self.routes[method][regex_path] = {
            'original_path': path,
            'handler': handler,
            'name': name,
            'params': self._extract_params(path)
        }
        
        print(f"[ROUTER] ✅ Rota adicionada: {method} {path} -> {handler.__name__ if hasattr(handler, '__name__') else 'handler'}")
    
    def _path_to_regex(self, path):
        """
        Converte path com parâmetros para regex
        /api/sensors/{id} -> /api/sensors/([^/]+)
        """
        # Escapar caracteres especiais manualmente (MicroPython não tem re.escape)
        escaped = self._escape_regex(path)
        
        # Substituir {param} por ([^/]+)
        regex = escaped.replace(r'\{([^}]+)\}', r'([^/]+)')
        
        # Adicionar âncoras de início e fim
        return f"^{regex}$"
    
    def _escape_regex(self, text):
        """Escapa caracteres especiais para regex (implementação para MicroPython)"""
        # Caracteres que precisam ser escapados em regex
        special_chars = r'\.^$*+?{}[]|()'
        escaped = text
        
        for char in special_chars:
            escaped = escaped.replace(char, '\\' + char)
        
        return escaped
    
    def _extract_params(self, path):
        """Extrai nomes dos parâmetros do path"""
        params = re.findall(r'\{([^}]+)\}', path)
        return params
    
    def match_route(self, method, path):
        """
        Encontra rota que corresponde ao path
        Retorna (handler, params) ou (None, None)
        """
        if method not in self.routes:
            return None, None
        
        # Decodificar URL
        path = unquote(path)
        
        for regex_path, route_info in self.routes[method].items():
            match = re.match(regex_path, path)
            if match:
                # Extrair parâmetros
                params = {}
                if route_info['params']:
                    groups = match.groups()
                    for i, param_name in enumerate(route_info['params']):
                        if i < len(groups):
                            params[param_name] = groups[i]
                
                print(f"[ROUTER] ✅ Rota encontrada: {method} {path} -> {route_info['handler'].__name__ if hasattr(route_info['handler'], '__name__') else 'handler'}")
                return route_info['handler'], params
        
        print(f"[ROUTER] ❌ Rota não encontrada: {method} {path}")
        return None, None
    
    def add_middleware(self, middleware_func):
        """
        Adiciona middleware ao pipeline
        - middleware_func: função que recebe (request, next)
        """
        self.middleware.append(middleware_func)
        print(f"[ROUTER] ✅ Middleware adicionado: {middleware_func.__name__ if hasattr(middleware_func, '__name__') else 'middleware'}")
    
    def process_request(self, method, path, request_data=None):
        """
        Processa requisição através do pipeline
        - Aplica middlewares
        - Encontra rota
        - Executa handler
        """
        # Criar contexto da requisição
        request = {
            'method': method,
            'path': path,
            'data': request_data,
            'params': {},
            'headers': self._parse_headers(request_data) if request_data else {}
        }
        
        # Aplicar middlewares
        for middleware in self.middleware:
            try:
                result = middleware(request)
                if result:  # Se middleware retorna algo, usar como resposta
                    return result
            except Exception as e:
                print(f"[ROUTER] ❌ Erro no middleware {middleware.__name__}: {e}")
        
        # Encontrar rota
        handler, params = self.match_route(method, path)
        if not handler:
            return self._create_404_response()
        
        # Adicionar parâmetros à requisição
        request['params'] = params
        
        # Executar handler
        try:
            response = handler(request)
            return response
        except Exception as e:
            print(f"[ROUTER] ❌ Erro no handler: {e}")
            return self._create_500_response(str(e))
    
    def _parse_headers(self, request_data):
        """Extrai headers da requisição"""
        headers = {}
        if not request_data:
            return headers
        
        lines = request_data.split('\r\n')
        for line in lines[1:]:  # Pular primeira linha (request line)
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return headers
    
    def _create_404_response(self):
        """Cria resposta 404"""
        body = "404 Not Found"
        response = f"HTTP/1.1 404 Not Found\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        return response
    
    def _create_500_response(self, error_msg):
        """Cria resposta 500"""
        body = f"500 Internal Server Error\n{error_msg}"
        response = f"HTTP/1.1 500 Internal Server Error\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        return response
    
    def get_routes_info(self):
        """Retorna informações sobre todas as rotas"""
        info = {}
        for method, routes in self.routes.items():
            info[method] = []
            for regex_path, route_info in routes.items():
                info[method].append({
                    'path': route_info['original_path'],
                    'name': route_info['name'],
                    'params': route_info['params']
                })
        return info
    
    def print_routes(self):
        """Imprime todas as rotas registradas"""
        print("\n[ROUTER] 📋 Rotas registradas:")
        for method, routes in self.routes.items():
            if routes:
                print(f"  {method}:")
                for regex_path, route_info in routes.items():
                    print(f"    {route_info['original_path']} -> {route_info['handler'].__name__ if hasattr(route_info['handler'], '__name__') else 'handler'}")
        print()
