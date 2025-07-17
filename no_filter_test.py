from scraper import Scraper
from extract import Extractor
from selector import Selector
from utils import save_papers, load_papers


years = [
    '2024'
]
conferences = [
    'ICLR'
]
# Используем очень общие ключевые слова, которые точно найдутся
keywords = [
    'model'  # почти во всех статьях есть слово "model"
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
    fpath='no_filter_test.csv', 
    fns=[modify_paper], 
    selector=selector
)

# НЕ добавляем никаких фильтров!
print("Запускаем тест без фильтров для извлечения ревью...")
print("Это займет некоторое время, так как мы обрабатываем все статьи...")

scraper()

print("Готово! Проверим результаты...")

# Проверим, создался ли CSV файл
import os
if os.path.exists('no_filter_test.csv'):
    print("✅ CSV файл создан успешно!")
    with open('no_filter_test.csv', 'r', encoding='utf-8') as f:
        header = f.readline().strip()
        print(f"Заголовки: {header}")
        columns = header.split(',')
        print(f"Количество колонок: {len(columns)}")
        
        # Посмотрим на колонки с ревью
        review_columns = [col for col in columns if 'review' in col.lower()]
        if review_columns:
            print(f"✅ Найдены колонки с ревью: {review_columns}")
        else:
            print("❌ Колонки с ревью НЕ найдены")
        
        # Прочитаем первую строку данных
        first_line = f.readline().strip()
        if first_line:
            print("✅ Первая строка данных найдена!")
            # Показываем первые несколько колонок
            values = first_line.split(',')
            for i, (col, val) in enumerate(zip(columns[:5], values[:5])):
                print(f"  {col}: {val[:50]}..." if len(val) > 50 else f"  {col}: {val}")
        else:
            print("❌ Нет данных в файле")
else:
    print("❌ CSV файл НЕ создан") 