class Extractor:
  def __init__(self, fields, subfields, include_subfield=False, extract_reviews=False):
    self.fields = fields
    self.subfields = subfields
    self.include_subfield = include_subfield
    self.extract_reviews = extract_reviews
  
  def __call__(self, paper):
    return self.extract(paper)

  def extract_review_data(self, paper):
    """Извлекает и объединяет данные ревью из directReplies"""
    review_data = {
      'reviews_full_text': '',
      'reviews_summary': '',
      'reviews_strengths': '',
      'reviews_weaknesses': '',
      'reviews_questions': '',
      'reviews_average_rating': None,
      'reviews_count': 0
    }
    
    if not hasattr(paper, 'details') or not paper.details:
      return review_data
      
    direct_replies = paper.details.get('directReplies', [])
    if not direct_replies:
      return review_data
    
    # Фильтруем только официальные ревью (данные теперь хранятся как словари)
    reviews = []
    for reply in direct_replies:
      if (isinstance(reply, dict) and 
          'invitations' in reply and 
          any('Official_Review' in inv for inv in reply['invitations'])):
        reviews.append(reply)
    
    if not reviews:
      return review_data
    
    review_data['reviews_count'] = len(reviews)
    
    # Собираем данные из всех ревью
    all_summaries = []
    all_strengths = []
    all_weaknesses = []
    all_questions = []
    all_full_texts = []
    ratings = []
    
    for review in reviews:
      content = review.get('content', {})
      
      # Извлекаем основные поля ревью
      summary = self._extract_value(content.get('summary', ''))
      strengths = self._extract_value(content.get('strengths', ''))
      weaknesses = self._extract_value(content.get('weaknesses', ''))
      questions = self._extract_value(content.get('questions', ''))
      rating = self._extract_value(content.get('rating', ''))
      
      if summary:
        all_summaries.append(f"Summary: {summary}")
      if strengths:
        all_strengths.append(f"Strengths: {strengths}")
      if weaknesses:
        all_weaknesses.append(f"Weaknesses: {weaknesses}")
      if questions:
        all_questions.append(f"Questions: {questions}")
      
      # Формируем полный текст ревью
      review_parts = []
      if summary:
        review_parts.append(f"SUMMARY: {summary}")
      if strengths:
        review_parts.append(f"STRENGTHS: {strengths}")
      if weaknesses:
        review_parts.append(f"WEAKNESSES: {weaknesses}")
      if questions:
        review_parts.append(f"QUESTIONS: {questions}")
      
      if review_parts:
        full_review = "\n\n".join(review_parts)
        all_full_texts.append(full_review)
      
      # Извлекаем рейтинг для подсчета среднего
      if rating:
        try:
          # Пытаемся извлечь числовое значение из рейтинга
          rating_str = str(rating).lower()
          if ':' in rating_str:
            rating_num = rating_str.split(':')[0].strip()
          else:
            rating_num = rating_str
          
          # Извлекаем число
          import re
          numbers = re.findall(r'\d+', rating_num)
          if numbers:
            ratings.append(int(numbers[0]))
        except:
          pass
    
    # Объединяем все данные
    review_data['reviews_full_text'] = "\n\n--- REVIEW SEPARATOR ---\n\n".join(all_full_texts)
    review_data['reviews_summary'] = " | ".join(all_summaries)
    review_data['reviews_strengths'] = " | ".join(all_strengths)
    review_data['reviews_weaknesses'] = " | ".join(all_weaknesses)
    review_data['reviews_questions'] = " | ".join(all_questions)
    
    # Вычисляем средний рейтинг
    if ratings:
      review_data['reviews_average_rating'] = sum(ratings) / len(ratings)
    
    return review_data
  
  def _extract_value(self, field):
    """Вспомогательная функция для извлечения значения из поля"""
    if isinstance(field, dict) and 'value' in field:
      return field['value']
    elif isinstance(field, str):
      return field
    else:
      return str(field) if field else ''

  def extract(self, paper):
    trimmed_paper = {}
    
    # Извлекаем обычные поля
    for field in self.fields:
      trimmed_paper[field] = paper.__getattribute__(field)
    
    # Извлекаем subfields
    for subfield, fields in self.subfields.items():
      if self.include_subfield:
        trimmed_paper[subfield] = {}
      for field in fields:
        field_value = paper.__getattribute__(subfield)[field]
        if self.include_subfield:
          trimmed_paper[subfield][field] = field_value
        else:
          trimmed_paper[field] = field_value
    
    # Извлекаем данные ревью, если требуется
    if self.extract_reviews:
      review_data = self.extract_review_data(paper)
      trimmed_paper.update(review_data)
    
    return trimmed_paper