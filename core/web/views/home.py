from django.shortcuts import redirect, render

from core.web.forms import BallotCreationForm
from core.web.models.ballot import Ballot


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    ballots = Ballot.objects.all()

    if request.method == "POST":
        form = BallotCreationForm(data=request.POST)

        if not form.is_valid():
            return render(request, "home.html", context={"form": form, "ballots": ballots})

    return render(request, "home.html", context={"form": BallotCreationForm(), "ballots": ballots})
