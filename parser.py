import requests
from bs4 import BeautifulSoup

def parse_text_from_url(url):
    """
    Получает текст с указанного URL и возвращает очищенный текстовый контент.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        if response.encoding is None:
            response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Удаляем скрипты, стили и другие нежелательные элементы
        for tag in soup(['script', 'style', 'meta', 'noscript']):
            tag.decompose()
        
        # Получаем текст, разделяем строки и убираем лишние пробелы
        text = soup.get_text(separator='\n', strip=True)
        
        # Дополнительная очистка: удаляем пустые строки
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        return cleaned_text
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None

if __name__ == "__main__":
    url = "https://eternal-gores.com/api/profiles/by-nick/ZнdyyR"
    result = parse_text_from_url(url)
    if result:
        print(result[:1000])