import base64
import requests

def url_to_base64(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # проверим, что загрузка прошла успешно
    
    # Определяем MIME-тип по расширению или из ответа
    content_type = response.headers.get('content-type', 'image/png')
    b64 = base64.b64encode(response.content).decode()
    return f"data:{content_type};base64,{b64}"

if __name__ == "__main__":
    # url = "https://eternal-gores.com/api/profiles/by-nick/ZнdyyR"
    url = "https://eternal-gores.com/api/profiles/by-nick/axech"
    result = url_to_base64("https://eternal-gores.com/static/avatars/a78303c910f94362b932b56db39badb6.webp")
    if result:
        print(result)