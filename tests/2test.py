import re
from scrapers.x1337 import Scraper1337, Params1337, Category1337

def clean_title(raw_name: str) -> str:
    # 1) Убираем всё в скобках
    s = re.sub(r"[\[\(].*?[\]\)]", "", raw_name)
    # 2) Удаляем "мусорные" слова
    garbage = [
        r"\brepack\b", r"\bfitgirl\b", r"\bdodi\b", r"\bxatab\b",
        r"\bcorepack\b", r"\bcatalyst\b", r"\bmechanic\b", r"\bgog\b",
        r"\bselective download\b", r"\bMULTI\d+\b", r"\bGold Edition\b",
        r"\bDeluxe Edition\b", r"\bCracFIX\b", r"\bPC game\b", r"\bPKG\b",
        r"\bPROPHET\b", r"\bSKIDROW\b", r"\bSilent Assassin\b",
        r"\bElite Edition\b", r"\bProfessional Edition\b",
        r"\bFCKDRM\b", r"\bOnly Crack\b", r"\bCrack Only\b",
        r"\bXBOX360\b", r"\bPS4\b", r"\bPS5\b", r"\bSwitch\b", r"\bNSP\b"
    ]
    s = re.sub("|".join(garbage), "", s, flags=re.IGNORECASE)
    # 3) Убираем версии (vX.Y.Z) и обновления (Update X)
    s = re.sub(r"\bupdate\s*\d+(?:\.\d+)*\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\bv\d+(?:\.\d+)*\b", "", s, flags=re.IGNORECASE)
    # 4) Обрезаем всё после первых разделителей дефиса или многоточия
    s = re.sub(r"[-–—·…]+.*$", "", s)
    # 5) Оставляем только буквы, цифры, двоеточие и некоторые символы
    s = re.sub(r"[^A-Za-z0-9 :'-]", " ", s)
    # 6) Убираем лишние пробелы
    s = re.sub(r"\s{2,}", " ", s).strip()
    # 7) Делаем заглавными первые буквы слов
    return s.title()

# Пример использования:
user_input = "Hitman"
target_clean = clean_title(user_input)
print(f"\nКаноническое название: {target_clean}\n")

scraper = Scraper1337()
params = Params1337(
    name=user_input,
    category=Category1337.GAMES,
    order_ascending=False
)
results = scraper.find_torrents(params, (1, 2, 3, 4, 5))

matches = [t for t in results if clean_title(t.name) == target_clean]

if matches:
    print(f"Каноническое название: {target_clean}")
    print("Найденные релизы с точно таким названием:")
    for t in matches:
        print(f" - {t.name}")
else:
    print(f"Релизов с названием '{target_clean}' не найдено.")