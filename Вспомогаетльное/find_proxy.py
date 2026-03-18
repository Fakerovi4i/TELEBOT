import requests
import socks
import socket
from urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждения о SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def test_proxy_detailed(proxy_string):
    print(f"🔍 Детальная проверка прокси: {proxy_string}")

    # Пробуем разные протоколы
    protocols = ['socks5', 'socks5h', 'http', 'https']

    for protocol in protocols:
        # Заменяем протокол в строке
        modified_proxy = proxy_string.replace('socks5', protocol)
        print(f"\n📡 Тестируем протокол: {protocol}")
        print(f"   Строка: {modified_proxy}")

        proxies = {'https': modified_proxy}

        try:
            # Сначала пробуем обычный запрос
            r = requests.get('https://api.telegram.org',
                             proxies=proxies,
                             timeout=10,
                             verify=False)  # отключаем проверку SSL
            print(f"   ✅ Успех! Статус: {r.status_code}")
            return modified_proxy, protocol
        except Exception as e:
            print(f"   ❌ Ошибка: {type(e).__name__}: {e}")

    # Пробуем без прокси (для сравнения)
    print("\n📡 Тестируем без прокси:")
    try:
        r = requests.get('https://api.telegram.org', timeout=5, verify=False)
        print(f"   ✅ Без прокси работает! Статус: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Без прокси тоже не работает: {e}")

    return None, None


if __name__ == "__main__":
    PROXY = 'socks5://user378530:ybn81k@185.121.227.116:7255'
    working_proxy, protocol = test_proxy_detailed(PROXY)

    if working_proxy:
        print(f"\n🎯 Найден рабочий вариант: {working_proxy}")
        print(f"   Используйте протокол: {protocol}")
    else:
        print("\n❌ Ни один протокол не сработал")