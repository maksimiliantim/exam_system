import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
django.setup()

from tests_app.models import Question, Test
import csv
from tests_app.models import Question, Test

test = Test.objects.get(title='Математика')
with open('math_questions.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        question = Question.objects.create(
            text=row['Вопрос'],
            test=test
        )
        answers = row['Ответы'].split(';')
        correct_answer = row['Правильный ответ']
        for answer_text in answers:
            question.answers.create(
                text=answer_text,
                is_correct=(answer_text == correct_answer)
            )
