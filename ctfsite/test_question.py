
from question.models import Tag, Question, Solve

T1 = Tag(tag_name=Tag.PWN)
T2 = Tag(tag_name=Tag.MISC)
T3 = Tag(tag_name=Tag.WEB)
T4 = Tag(tag_name=Tag.Crypto)
T5 = Tag(tag_name=Tag.Reverse)
T1.save()
T2.save()
T3.save()
T4.save()
T5.save()

Q1 = Question(question_tag=T4, question_name="小强的自述", description="小强说了一段话")
Q1.set_flag("NKCTF{HELLO}")
Q1.save()
