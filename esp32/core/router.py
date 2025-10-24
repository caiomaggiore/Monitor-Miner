# ============================================================================
# ROUTER - Monitor Miner v4.0
# ============================================================================
# Sistema de roteamento HTTP compatível com MicroPython
# - Mapeamento de rotas
# - Middleware support
# - Controllers integration
# ============================================================================

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
    Sistema de roteamento HTTP compatível com MicroPython
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
        
        # Armazenar informações da rota
        self.routes[method][path] = {
            'handler': handler,
            'path': path,
            'params': self._extract_params(path),
            'name': name
        }
        
        print(f"[ROUTER] ✅ Rota adicionada: {method} {path} -> {handler.__name__ if hasattr(handler, '__name__') else 'handler'}")
    
    def _extract_params(self, path):
        """Extrai nomes dos parâmetros do path (implementação para MicroPython)"""
        params = []
        # Buscar manualmente por {param}
        i = 0
        while i < len(path):
            if path[i] == '{':
                # Encontrar o fechamento }
                j = i + 1
                while j < len(path) and path[j] != '}':
                    j += 1
                if j < len(path):  # Encontrou o fechamento
                    param = path[i+1:j]
                    params.append(param)
                    i = j + 1
                else:
                    break
            else:
                i += 1
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
        
        # Tentar match com path (implementação básica para MicroPython)
        for route_path, route_info in self.routes[method].items():
            if self._path_matches(route_path, path):
                # Extrair parâmetros
                params = self._extract_path_params(route_path, path)
                
                print(f"[ROUTER] ✅ Rota encontrada: {method} {path} -> {route_info['handler'].__name__ if hasattr(route_info['handler'], '__name__') else 'handler'}")
                return route_info['handler'], params
        
        print(f"[ROUTER] ❌ Rota não encontrada: {method} {path}")
        return None, None
    
    def _path_matches(self, route_path, request_path):
        """Verifica se o path da requisição corresponde à rota (implementação básica)"""
        # Se são iguais, match exato
        if route_path == request_path:
            return True
        
        # Se a rota tem parâmetros {param}, fazer match básico
        if '{' in route_path and '}' in route_path:
            # Implementação básica: verificar se os segmentos coincidem
            route_segments = route_path.split('/')
            request_segments = request_path.split('/')
            
            if len(route_segments) != len(request_segments):
                return False
            
            for i, route_seg in enumerate(route_segments):
                request_seg = request_segments[i]
                
                # Se é um parâmetro {param}, aceitar qualquer valor
                if route_seg.startswith('{') and route_seg.endswith('}'):
                    continue
                
                # Se não é parâmetro, deve ser igual
                if route_seg != request_seg:
                    return False
            
            return True
        
        return False
    
    def _extract_path_params(self, route_path, request_path):
        """Extrai parâmetros do path (implementação básica)"""
        params = {}
        
        if '{' not in route_path:
            return params
        
        route_segments = route_path.split('/')
        request_segments = request_path.split('/')
        
        for i, route_seg in enumerate(route_segments):
            if route_seg.startswith('{') and route_seg.endswith('}'):
                param_name = route_seg[1:-1]  # Remove { e }
                if i < len(request_segments):
                    params[param_name] = unquote(request_segments[i])
        
        return params
    
    def add_middleware(self, middleware_func):
        """
        Adiciona middleware ao pipeline
        - middleware_func: função que processa requisição
        """
        self.middleware.append(middleware_func)
        print(f"[ROUTER] ✅ Middleware adicionado: {middleware_func.__name__ if hasattr(middleware_func, '__name__') else 'middleware'}")
    
    def process_middleware(self, request):
        """
        Processa middleware pipeline
        - request: objeto de requisição
        """
        for middleware in self.middleware:
            try:
                result = middleware(request)
                if result:  # Se middleware retorna algo, parar pipeline
                    return result
            except Exception as e:
                print(f"[ROUTER] ❌ Erro no middleware {middleware.__name__ if hasattr(middleware, '__name__') else 'middleware'}: {e}")
                continue
        
        return None
    
    def get_routes_info(self):
        """
        Retorna informações sobre todas as rotas
        """
        info = {
            'total_routes': 0,
            'routes_by_method': {},
            'middleware_count': len(self.middleware)
        }
        
        for method, routes in self.routes.items():
            count = len(routes)
            info['total_routes'] += count
            info['routes_by_method'][method] = count
        
        return info