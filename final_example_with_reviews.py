#!/usr/bin/env python3
"""
Финальный рабочий пример веб-скрапера OpenReview с извлечением ревью

Этот скрипт демонстрирует полную функциональность:
- Скрапинг статей с OpenReview
- Извлечение полного текста ревью
- Экспорт в CSV со всеми данными
"""

from scraper import Scraper
from extract import Extractor
from filters import title_filter, keywords_filter, abstract_filter, reviews_filter
from selector import Selector
from utils import save_papers, load_papers

def main():
    print("🚀 OPENREVIEW SCRAPER С ИЗВЛЕЧЕНИЕМ РЕВЬЮ")
    print("=" * 50)
    
    # Настройки скрапинга
    years = ['2024']
    conferences = ['ICLR']
    keywords = [
        'language',     # общие ключевые слова, которые найдут больше статей
        'learning',
        'model',
        'neural'
    ]
    
    def modify_paper(paper):
        """Модифицирует URL'ы для статьи"""
        paper.forum = f"https://openreview.net/forum?id={paper.forum}"
        if 'pdf' in paper.content:
            paper.content['pdf'] = f"https://openreview.net{paper.content['pdf']}"
        return paper
    
    # Создаем экстрактор с включенным извлечением ревью
    print("🔧 Настраиваем экстрактор с извлечением ревью...")
    extractor = Extractor(
        fields=['forum'], 
        subfields={'content': ['title', 'keywords', 'abstract', 'pdf', 'match']}, 
        extract_reviews=True  # ✨ КЛЮЧЕВАЯ ОПЦИЯ!
    )
    
    # Создаем скрапер
    selector = Selector()
    scraper = Scraper(
        conferences=conferences, 
        years=years, 
        keywords=keywords,
        extractor=extractor, 
        fpath='papers_with_reviews_final.csv', 
        fns=[modify_paper], 
        selector=selector
    )
    
    # Добавляем фильтры
    print("🔍 Добавляем фильтры...")
    scraper.add_filter(title_filter)
    scraper.add_filter(keywords_filter) 
    scraper.add_filter(abstract_filter)
    scraper.add_filter(reviews_filter)  # ✨ Фильтр по ревью!
    
    print(f"📋 Конфигурация:")
    print(f"   Конференции: {conferences}")
    print(f"   Годы: {years}")
    print(f"   Ключевые слова: {keywords}")
    print(f"   Извлечение ревью: ✅ Включено")
    print(f"   Выходной файл: papers_with_reviews_final.csv")
    
    # Запускаем скрапинг
    print("\n🕷️ Запускаем скрапинг...")
    scraper()
    
    # Сохраняем данные
    print("\n💾 Сохраняем данные...")
    save_papers(scraper.papers, fpath='papers_with_reviews_final.pkl')
    
    # Проверяем результат
    print("\n📊 Анализируем результат...")
    import os
    import pandas as pd
    
    if os.path.exists('papers_with_reviews_final.csv'):
        df = pd.read_csv('papers_with_reviews_final.csv')
        print(f"✅ CSV файл создан успешно!")
        print(f"   📄 Статей: {len(df)}")
        print(f"   📝 Колонок: {len(df.columns)}")
        
        # Проверяем наличие колонок с ревью
        review_columns = [col for col in df.columns if 'review' in col.lower()]
        if review_columns:
            print(f"   🔍 Колонки с ревью: {len(review_columns)}")
            for col in review_columns:
                print(f"      - {col}")
            
            # Показываем статистику по ревью
            if 'reviews_count' in df.columns:
                total_reviews = df['reviews_count'].sum()
                avg_reviews = df['reviews_count'].mean()
                print(f"   📈 Всего ревью: {total_reviews}")
                print(f"   📈 Среднее ревью на статью: {avg_reviews:.1f}")
            
            if 'reviews_average_rating' in df.columns:
                ratings = df['reviews_average_rating'].dropna()
                if len(ratings) > 0:
                    overall_avg = ratings.mean()
                    print(f"   ⭐ Средний рейтинг: {overall_avg:.2f}")
        else:
            print("   ⚠️  Колонки с ревью не найдены")
        
        print(f"\n📋 Первые 5 колонок:")
        for i, col in enumerate(df.columns[:5], 1):
            print(f"   {i}. {col}")
        
        if len(df.columns) > 5:
            print(f"   ... и ещё {len(df.columns) - 5} колонок")
            
    else:
        print("❌ CSV файл не создан - возможно, не найдено статей, прошедших фильтры")
        print("💡 Попробуйте расширить ключевые слова или убрать некоторые фильтры")

    print("\n🎉 Готово!")
    print("📁 Результаты сохранены в:")
    print("   - papers_with_reviews_final.csv (таблица)")
    print("   - papers_with_reviews_final.pkl (бинарные данные)")

if __name__ == "__main__":
    main() 