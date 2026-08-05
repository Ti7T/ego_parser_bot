import requests

def get_player_json(url: str) -> dict | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.JSONDecodeError:
        print("Сервер вернул не JSON.")
        return None

    except requests.RequestException as e:
        print(e)
        return None

if __name__ == "__main__":
    # url = "https://eternal-gores.com/api/profiles/by-nick/ZнdyyR"
    url = "https://eternal-gores.com/api/profiles/by-nick/axech"
    result = get_player_json(url)
    if result:
        print(result["clan"])