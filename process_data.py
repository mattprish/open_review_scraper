#!/usr/bin/env python3

from utils import load_papers, to_csv
from extract import Extractor

def modify_paper(paper):
    """Функция для модификации данных статьи"""
    paper.forum = f"https://openreview.net/forum?id={paper.forum}"
    paper.content['pdf'] = f"https://openreview.net{paper.content['pdf']}"
    return paper

def process_papers():
    # Загружаем данные
    papers = load_papers('papers_with_reviews.pkl')
    
    # Создаем экстрактор (без поля match, так как оно может отсутствовать)
    extractor = Extractor(
        fields=['forum'], 
        subfields={'content':['title', 'keywords', 'abstract', 'pdf']}, 
        extract_reviews=True
    )
    
    processed_papers = []
    
    for group_name, group_data in papers.items():
        for venue, venue_papers in group_data.items():
            venue_split = venue.split('/')
            venue_name, venue_year, venue_type = venue_split[0], venue_split[1], venue_split[2]
            
            for paper in venue_papers:
                # Применяем модификацию
                paper = modify_paper(paper)
                
                # Извлекаем данные
                extracted_paper = extractor(paper)
                
                # Добавляем дополнительные поля
                extracted_paper['venue'] = venue_name
                extracted_paper['year'] = venue_year
                extracted_paper['type'] = venue_type
                
                processed_papers.append(extracted_paper)
    
    print(f"Обработано статей: {len(processed_papers)}")
    
    if processed_papers:
        print(f"Колонки в данных: {list(processed_papers[0].keys())}")
        
        # Сохраняем в CSV
        to_csv(processed_papers, 'processed_papers.csv')
        print("CSV файл создан: processed_papers.csv")
        
        # Показываем пример первой статьи
        print("\n=== ПРИМЕР ПЕРВОЙ СТАТЬИ ===")
        first_paper = processed_papers[0]
        for key, value in first_paper.items():
            if isinstance(value, str) and len(value) > 200:
                print(f"{key}: {value[:200]}...")
            else:
                print(f"{key}: {value}")
    
    return processed_papers

if __name__ == "__main__":
    process_papers() 