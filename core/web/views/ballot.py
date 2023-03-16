from django.shortcuts import get_object_or_404, redirect, render

from core.web.forms import VoteForm
from core.web.models.ballot import Ballot


def ballot_view(request, address):
    if not request.user.is_authenticated:
        return redirect("login")

    ballot = get_object_or_404(Ballot, address=address)

    options = []
    options.append(("1", "Option 1"))
    options.append(("2", "Option 2"))

    if request.method == "POST":
        form = VoteForm(options=options, data=request.POST)

        if form.is_valid():
            return redirect(request.path)

    return render(request, "ballot.html", context={"form": VoteForm(options=options), "ballot": ballot})
