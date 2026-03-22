import requests
import json
from config import API_HOST, SITE_API_KEY, API_TIMEOUT

headers = {"X-API-KEY": SITE_API_KEY}


def get_movie_by_id(movie_id: int):
    """Получение фильма по ID"""
    try:
        url = f"{API_HOST}/movie/{movie_id}"
        response = requests.get(
            url,
            headers=headers,
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
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


def find_move_by_name(move_name: str, page=1, limit=10):
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


def find_movies_by_rating(min_rating=0.0, max_rating=10.0, page=1, limit=10):
    """Поиск фильмов по рейтингу Кинопоиск"""
    try:
        url = f"{API_HOST}/movie"
        params = {
            "page": page,
            "limit": limit,
            "rating.kp": f"{min_rating}-{max_rating}",
            "sortField": "rating.kp",
            "sortType": "-1"  # Сортировка по убыванию рейтинга
        }
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
    print(json.dumps(find_movies_by_rating(min_rating=7), ensure_ascii=False, indent=2))
    result = find_move_by_name("Титаник")
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