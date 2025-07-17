#!/usr/bin/env python3
"""
Тест извлечения ревью на уже загруженных данных
"""

import dill
from extract import Extractor
import pandas as pd

def test_review_extraction():
    print("=== ТЕСТ ИЗВЛЕЧЕНИЯ РЕВЬЮ ===")
    
    # Загружаем существующие данные
    try:
        with open('papers_with_reviews.pkl', 'rb') as f:
            papers_data = dill.load(f)
        print("✅ Данные загружены успешно")
    except FileNotFoundError:
        print("❌ Файл papers_with_reviews.pkl не найден")
        return
    
    # Создаем экстрактор с включенным извлечением ревью (убираем 'match' поле)
    extractor = Extractor(
        fields=['forum'], 
        subfields={'content':['title', 'keywords', 'abstract']}, 
        extract_reviews=True
    )
    
    # Найдем первую статью с ревью для тестирования
    test_paper = None
    test_venue = None
    
    print("\n🔍 Ищем статью с ревью...")
    for group_name, group_data in papers_data.items():
        for venue_name, venue_papers in group_data.items():
            for i, paper in enumerate(venue_papers):
                if (hasattr(paper, 'details') and 
                    paper.details and 
                    paper.details.get('directReplies')):
                    # Проверяем, есть ли официальные ревью (обновленная логика)
                    direct_replies = paper.details['directReplies']
                    official_reviews = [
                        reply for reply in direct_replies 
                        if (isinstance(reply, dict) and 
                            'invitations' in reply and 
                            any('Official_Review' in inv for inv in reply['invitations']))
                    ]
                    if official_reviews:
                        test_paper = paper
                        test_venue = venue_name
                        print(f"✅ Найдена статья с {len(official_reviews)} ревью")
                        print(f"   Venue: {venue_name}")
                        title_content = paper.content.get('title', {})
                        title = title_content.get('value', 'No title') if isinstance(title_content, dict) else str(title_content)
                        print(f"   Title: {title[:100]}...")
                        
                        # Показываем пример ревью
                        first_review = official_reviews[0]
                        review_content = first_review.get('content', {})
                        summary_content = review_content.get('summary', {})
                        summary = summary_content.get('value', 'No summary') if isinstance(summary_content, dict) else str(summary_content)
                        print(f"   First review summary: {summary[:100]}...")
                        break
            if test_paper:
                break
        if test_paper:
            break
    
    if not test_paper:
        print("❌ Не найдено статей с официальными ревью")
        return
    
    # Применяем экстрактор к тестовой статье
    print("\n🔧 Применяем экстрактор...")
    try:
        extracted_data = extractor.extract(test_paper)
        print("✅ Извлечение прошло успешно")
        
        # Проверяем наличие полей ревью
        review_fields = [key for key in extracted_data.keys() if 'review' in key.lower()]
        print(f"\n📋 Найдены поля ревью: {review_fields}")
        
        # Показываем содержимое каждого поля ревью
        for field in review_fields:
            value = extracted_data[field]
            print(f"\n🔹 {field}:")
            if isinstance(value, str):
                if len(value) > 200:
                    print(f"   {value[:200]}...")
                    print(f"   [Всего символов: {len(value)}]")
                else:
                    print(f"   {value}")
            else:
                print(f"   {value}")
        
        # Создаем мини CSV для демонстрации
        print(f"\n💾 Создаем демонстрационный CSV...")
        df_data = [extracted_data]
        df = pd.DataFrame(df_data)
        df.to_csv('review_extraction_demo.csv', index=False)
        print(f"✅ Файл review_extraction_demo.csv создан")
        print(f"   Колонок: {len(df.columns)}")
        print(f"   Размер: {df.shape}")
        
        # Показываем список всех колонок
        print(f"\n📊 Все колонки:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при извлечении: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_review_extraction() 