
from user.models import User, Career, Team


C1 = Career(Career.PWN)
C2 = Career(Career.MISC)
C3 = Career(Career.WEB)
C4 = Career(Career.Crypto)
C5 = Career(Career.Almighty)
C1.save()
C2.save()
C3.save()
C4.save()
C5.save()


DragonTeam = Team(team_name="Dragon", description="Welcome to Dragon team")
DragonTeam.save()
WolfTeam = Team(team_name="Tiny Wolf", description="Welcome to tiny wolf team")
WolfTeam.save()

User_A = User(username="A", score=10, belong=DragonTeam, user_career=C1, is_leader=True)
User_A.save()
User_B = User(username="B", score=20, belong=DragonTeam, user_career=C4)
User_B.save()
User_C = User(username="C", score=5, belong=DragonTeam, user_career=C2)
User_C.save()

User_D = User(username="D", score=100, belong=WolfTeam, user_career=C1, is_leader=True)
User_D.save()
User_E = User(username="E", score=200, belong=WolfTeam, user_career=C3)
User_E.save()