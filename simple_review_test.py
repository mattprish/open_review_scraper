from scraper import Scraper
from extract import Extractor
from filters import title_filter, keywords_filter, abstract_filter
from selector import Selector
from utils import save_papers, load_papers


years = [
    '2024'
]
conferences = [
    'ICLR'
]
keywords = [
    'language',  # более общее ключевое слово
    'model',
    'learning'
]

def modify_paper(paper):
  paper.forum = f"https://openreview.net/forum?id={paper.forum}"
  paper.content['pdf'] = f"https://openreview.net{paper.content['pdf']}"
  return paper

# Включаем извлечение ревью
extractor = Extractor(
    fields=['forum'], 
    subfields={'content':['title', 'keywords', 'abstract', 'pdf', 'match']}, 
    extract_reviews=True
)
selector = Selector()
scraper = Scraper(
    conferences=conferences, 
    years=years, 
    keywords=keywords,
    extractor=extractor, 
    fpath='simple_review_test.csv', 
    fns=[modify_paper], 
    selector=selector
)

# Добавляем только один фильтр для простоты
scraper.add_filter(title_filter)

print("Запускаем простой тест извлечения ревью...")
scraper()

print("Готово! Проверим результаты...")

# Проверим, создался ли CSV файл
import os
if os.path.exists('simple_review_test.csv'):
    print("CSV файл создан успешно!")
    with open('simple_review_test.csv', 'r', encoding='utf-8') as f:
        header = f.readline().strip()
        print(f"Заголовки: {header}")
        print(f"Количество колонок: {len(header.split(','))}")
        
        # Прочитаем первую строку данных
        first_line = f.readline().strip()
        if first_line:
            print("Первая строка данных найдена!")
        else:
            print("Нет данных в файле")
else:
    print("CSV файл НЕ создан - возможно нет статей, прошедших фильтры") 