import math
from users.models import User
from progress.models import StepProgress
from progress.progress_cache import get_progress
from tags.models import TagLesson

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

for user in User.objects.filter(knowledge_rank__isnull=False).order_by('knowledge_rank'):
  knowledge = 0.0
  user = User.objects.get(id=2)
  seen = set()
  total = user.step_progresses.count()
  count = 0
  
  for step_progress in user.step_progresses.filter(step__deleted_at__isnull=True):
    if count % 100 == 0:
      print(count, '/', total)
    count += 1
    lesson = step_progress.step.lesson
    if lesson in seen:
      continue
    seen.add(lesson)
    if get_progress(user, lesson).is_passed:
      for tag_lesson in lesson.lesson_tags.all():
        difficulty = tag_lesson.difficulty
        knowledge += sigmoid(difficulty) * 10
        print(knowledge)
  
  print(knowledge)
                      

###

yet = set()

for step_progress in user.step_progresses.filter(step__deleted_at__isnull=True):
	lesson = step_progress.step.lesson
	if lesson in yet:
		continue
	get_progress(user, lesson).is_passed
	StepProgress.objects.filter(step__deleted_at__isnull=True, first_success=0).first().best_score
	get_progress(user, target)