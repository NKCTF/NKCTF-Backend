
from question.models import Tag, Question, Solve
from user.models import User, Career, Team
from message.models import Mail, JoinRequest


T1 = Tag.objects.create(tag_name=Tag.PWN)
T2 = Tag.objects.create(tag_name=Tag.MISC)
T3 = Tag.objects.create(tag_name=Tag.WEB)
T4 = Tag.objects.create(tag_name=Tag.Crypto)
T5 = Tag.objects.create(tag_name=Tag.Reverse)

Q1 = Question(question_tag=T4, question_name="小强的自述", description="小强说了一段话")
Q1.set_flag("NKCTF{HELLO}")
Q1.save()

C1 = Career.objects.create(career_name=Career.PWN)
C2 = Career.objects.create(career_name=Career.MISC)
C3 = Career.objects.create(career_name=Career.WEB)
C4 = Career.objects.create(career_name=Career.Crypto)
C5 = Career.objects.create(career_name=Career.Almighty)


DragonTeam = Team.objects.create(team_name="Dragon", description="Welcome to Dragon team")
WolfTeam = Team.objects.create(team_name="Tiny Wolf", description="Welcome to tiny wolf team")

User_A = User.objects.create(username="A", score=10, belong=DragonTeam,
              user_career=C1, is_leader=True)
User_B = User.objects.create(username="B", score=20, belong=DragonTeam, user_career=C4)
User_C = User.objects.create(username="C", score=5, belong=DragonTeam, user_career=C2)
User_D = User.objects.create(username="D", score=100, belong=WolfTeam,
              user_career=C1, is_leader=True)
User_E = User.objects.create(username="E", score=200, belong=WolfTeam, user_career=C3)
User_F = User.objects.create(username="F", score=1000, user_career=C1)

test_user = User(username="shesl-meow")
test_user.set_password("shesl-meow+1S")
test_user.save()
test_user.create_team("test_name")

from user.alterdb.views import JoinTeam
JoinTeam(team_name="Dragon", crt_user=User_F).apply()
JoinTeam(team_name="test_name", crt_user=User_F).apply()

M1 = Mail.objects.create(title="Hello", content="nihaoya", send_by=User_F, send_to=User_A)
M2 = JoinRequest.objects.create(title="Join", content="I want to join your team!", send_by=User_F, send_to=WolfTeam)
