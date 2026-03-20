import requests
import json
from config import API_HOST, SITE_API_KEY, API_TIMEOUT

headers = {"X-API-KEY": SITE_API_KEY}

def get_move_by_name(move_name: str, page=1, limit=5):
    """Поиск по названию"""
    try:
        url = f"{API_HOST}/movie/search"
        params = {"query": move_name, "page": page, "limit": limit}
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT

        )
        if response.status_code == 200:
            return response.json().get("docs", [])

        print(f"⚠️ API вернул код {response.status_code}")
        return None

    except requests.Timeout:
        print("⏰ Превышено время ожидания от API")
        return None

    except requests.ConnectionError:
        print("🔌 Ошибка подключения к API")
        return None

    except Exception as e:
        print(f"❌ Неожиданная ошибка от API: {e}")
        return None



if __name__ == "__main__":
    print('Тестирование API')
    result = get_move_by_name("Титаник")
    if result is None:
        print("❌ Произошла ошибка при обращении к API")
    elif len(result) == 0:
        print("😔 Фильм не найден")
    else:
        print(f"✅ Найдено фильмов: {len(result)}")
        print(f"Первый результат: {result[0].get('name', 'Без названия')}")
        print(result)





# with open('структура.txt', 'w', encoding='utf-8') as file:
#     file.write(json.dumps(result, ensure_ascii=False, indent=2))