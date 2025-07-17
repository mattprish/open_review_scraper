from scraper import Scraper
from extract import Extractor
from filters import title_filter, keywords_filter, abstract_filter, reviews_filter
from selector import Selector
from utils import save_papers, load_papers


years = [
    '2024'
]
conferences = [
    'ICLR'
]
keywords = [
    'NLP'
]

# Дополнительные ключевые слова для поиска в ревью
review_keywords = [
    'strong reject',
    'accept',
    'novelty',
    'contribution'
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
    keywords=keywords + review_keywords,  # Объединяем ключевые слова 
    extractor=extractor, 
    fpath='example_with_review_filter.csv', 
    fns=[modify_paper], 
    selector=selector
)

# Добавляем стандартные фильтры
scraper.add_filter(title_filter)
scraper.add_filter(keywords_filter)
scraper.add_filter(abstract_filter)

# Добавляем новый фильтр по ревью
scraper.add_filter(reviews_filter)

print("Запускаем скрапинг с извлечением и фильтрацией ревью...")
scraper()

save_papers(scraper.papers, fpath='papers_with_review_filter.pkl')
print("Готово! Результаты сохранены в example_with_review_filter.csv") 