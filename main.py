from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse


hostName = "127.0.0.1"
serverPort = 8080


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MyServer(BaseHTTPRequestHandler):
    """
    Обработчик HTTP запросов
    """

    def do_GET(self):
        """
        Обрабатывает GET-запросы
        """

        parsed_path = urlparse(self.path)
        path = parsed_path.path


        if path == "/favicon.ico":
            self.send_response(204)  # No Content
            self.end_headers()
            return

        if path == "/" or path == "":

            self.serve_file(os.path.join(BASE_DIR, "templates", "contacts.html"), "text/html")

        elif path == "/index.html":

            self.serve_file(os.path.join(BASE_DIR, "index.html"), "text/html")

        elif path.startswith("/static/"):

            file_path = os.path.join(BASE_DIR, path.lstrip("/"))
            self.serve_static_file(file_path)

        elif path.startswith("/templates/"):

            file_path = os.path.join(BASE_DIR, path.lstrip("/"))
            self.serve_file(file_path, "text/html")

        else:

            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")

    def serve_file(self, file_path, content_type):
        """
        Обслуживает HTML файлы
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()

            self.send_response(200)
            self.send_header("Content-type", f"{content_type}; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))

            # Логирование
            print(f"✅ {self.client_address[0]} - GET {self.path} - 200 OK")

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - File Not Found</h1>")
            print(f"❌ {self.client_address[0]} - GET {self.path} - 404 Not Found")

    def serve_static_file(self, file_path):
        """
        Обслуживает статические файлы (CSS, JS, иконки и т.д.)
        """
        try:

            if file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            elif file_path.endswith(".json"):
                content_type = "application/json"
            elif file_path.endswith(".woff2"):
                content_type = "font/woff2"
            elif file_path.endswith(".woff"):
                content_type = "font/woff"
            elif file_path.endswith(".ttf"):
                content_type = "font/ttf"
            elif file_path.endswith(".svg"):
                content_type = "image/svg+xml"
            elif file_path.endswith(".png"):
                content_type = "image/png"
            elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                content_type = "image/jpeg"
            elif file_path.endswith(".gif"):
                content_type = "image/gif"
            elif file_path.endswith(".ico"):
                content_type = "image/x-icon"
            else:
                content_type = "application/octet-stream"


            with open(file_path, "rb") as f:
                data = f.read()

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(data)

            print(f"✅ {self.client_address[0]} - GET {self.path} - 200 OK ({content_type})")

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - File Not Found</h1>")
            print(f"❌ {self.client_address[0]} - GET {self.path} - 404 Not Found")

    def log_message(self, format, *args):
        """
        Переопределяем логирование по умолчанию (отключаем, т.к. логируем вручную)
        """
        pass


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)

    print("=" * 60)
    print(" Веб-сервер запущен!")
    print("=" * 60)
    print(f" Server started: http://{hostName}:{serverPort}")
    print("")
    print(" Доступные страницы:")
    print(f"   • Контакты (GET /):     http://{hostName}:{serverPort}/")
    print(f"   • Главная:              http://{hostName}:{serverPort}/index.html")
    print(f"   • Каталог:              http://{hostName}:{serverPort}/templates/catalog.html")
    print(f"   • Категория:            http://{hostName}:{serverPort}/templates/category.html")
    print(f"   • Контакты (шаблон):    http://{hostName}:{serverPort}/templates/contacts.html")
    print("")
    print("  Для остановки нажмите Ctrl + C")
    print("=" * 60)
    print("")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("\n" + "=" * 60)
    print("🛑 Server stopped.")
    print("=" * 60)
