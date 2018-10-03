from user.models import User, Team


def setup_database():
    DragonTeam = Team(Name="Dragon", Description="Welcome to Dragon team")
    DragonTeam.save()
    WolfTeam = Team(Name="Tiny Wolf", Description="Welcome to tiny wolf team")
    WolfTeam.save()

    User_A = User(username="A", Score=10, Belong=DragonTeam)
    User_A.save()
    User_B = User(username="B", Score=20, Belong=DragonTeam)
    User_B.save()
    User_C = User(username="C", Score=5, Belong=DragonTeam)
    User_C.save()

    User_D = User(username="D", Score=100, Belong=WolfTeam)
    User_D.save()
    User_E = User(username="E", Score=200, Belong=WolfTeam)
    User_E.save()


if __name__ == "__main__":
    setup_database()

