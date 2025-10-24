# ============================================================================
# RESPONSE HELPERS - Monitor Miner v4.0
# ============================================================================
# Helpers para criação de respostas HTTP
# - JSON responses
# - File responses
# - Error responses
# - CORS support
# ============================================================================

import json

class HTTPResponse:
    """
    Classe para criação de respostas HTTP
    - Suporte a diferentes content-types
    - Headers customizáveis
    - CORS automático
    """
    
    def __init__(self, status_code=200, content_type="text/html", body="", headers=None):
        self.status_code = status_code
        self.content_type = content_type
        self.body = body
        self.headers = headers or {}
    
    def to_http(self):
        """Converte para string HTTP"""
        # Status line
        status_text = self._get_status_text(self.status_code)
        response = f"HTTP/1.1 {self.status_code} {status_text}\r\n"
        
        # Headers padrão
        response += f"Content-Type: {self.content_type}\r\n"
        response += f"Content-Length: {len(self.body)}\r\n"
        response += "Connection: close\r\n"
        
        # CORS headers
        response += "Access-Control-Allow-Origin: *\r\n"
        response += "Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n"
        response += "Access-Control-Allow-Headers: Content-Type, Authorization\r\n"
        
        # Headers customizados
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"
        
        response += "\r\n"
        response += self.body
        
        return response
    
    def _get_status_text(self, status_code):
        """Retorna texto do status HTTP"""
        status_texts = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable"
        }
        return status_texts.get(status_code, "Unknown")
    
    @classmethod
    def json_response(cls, data, status_code=200):
        """Cria resposta JSON"""
        try:
            body = json.dumps(data, separators=(',', ':'))  # Compact JSON
            return cls(status_code, "application/json", body)
        except Exception as e:
            return cls(500, "text/plain", f"JSON Error: {str(e)}")
    
    @classmethod
    def html_response(cls, html_content, status_code=200):
        """Cria resposta HTML"""
        return cls(status_code, "text/html", html_content)
    
    @classmethod
    def text_response(cls, text_content, status_code=200):
        """Cria resposta de texto"""
        return cls(status_code, "text/plain", text_content)
    
    @classmethod
    def file_response(cls, file_content, content_type="application/octet-stream", status_code=200):
        """Cria resposta de arquivo"""
        return cls(status_code, content_type, file_content)
    
    @classmethod
    def error_response(cls, error_message, status_code=500):
        """Cria resposta de erro"""
        return cls(status_code, "text/plain", error_message)
    
    @classmethod
    def not_found_response(cls, message="Not Found"):
        """Cria resposta 404"""
        return cls(404, "text/plain", message)
    
    @classmethod
    def method_not_allowed_response(cls, allowed_methods=None):
        """Cria resposta 405"""
        if allowed_methods:
            body = f"Method not allowed. Allowed methods: {', '.join(allowed_methods)}"
        else:
            body = "Method not allowed"
        return cls(405, "text/plain", body)
    
    @classmethod
    def cors_preflight_response(cls):
        """Cria resposta para CORS preflight"""
        return cls(200, "text/plain", "", {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400"
        })

# Funções de conveniência
def json_response(data, status_code=200):
    """Função de conveniência para resposta JSON"""
    return HTTPResponse.json_response(data, status_code)

def html_response(html_content, status_code=200):
    """Função de conveniência para resposta HTML"""
    return HTTPResponse.html_response(html_content, status_code)

def text_response(text_content, status_code=200):
    """Função de conveniência para resposta de texto"""
    return HTTPResponse.text_response(text_content, status_code)

def error_response(error_message, status_code=500):
    """Função de conveniência para resposta de erro"""
    return HTTPResponse.error_response(error_message, status_code)

def not_found_response(message="Not Found"):
    """Função de conveniência para resposta 404"""
    return HTTPResponse.not_found_response(message)

def cors_preflight_response():
    """Função de conveniência para CORS preflight"""
    return HTTPResponse.cors_preflight_response()
