import datetime
import time

from django.shortcuts import redirect, render

from core.web import bm_user, bm_voting
from core.web.forms import BallotCreationForm
from core.web.models.ballot import Ballot


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    ballots = []
    for ballot in reversed(Ballot.objects.all()):
        title, _, end_date, count_of_votes = bm_voting.get_ballot(ballot.id)
        ballots.append({
            "id": ballot.id,
            "tx_hash": ballot.tx_hash,
            "transaction": bm_voting.get_transaction(ballot.tx_hash),
            "title": title,
            "count_of_votes": sum(count_of_votes),
            "end_date": datetime.date.fromtimestamp(end_date)
        })

    user = bm_user.get_user(request.user.passport)

    if request.method == "POST":
        form = BallotCreationForm(data=request.POST)

        if not form.is_valid():
            return render(request, "home.html", context={"form": form, "ballots": ballots})

        if user is None:
            return render(request, "home.html", context={
                "form": form,
                "ballots": ballots,
                "error": "Permission denied."
            })

        title = form.cleaned_data["title"].strip()
        options = [option.strip() for option in form.cleaned_data["options"].split(",")]
        end_date = int(time.mktime(form.cleaned_data["end_date"].timetuple()))

        tx_hash, ballot_id = bm_voting.create_ballot(title, options, end_date)

        if tx_hash is None:
            return render(request, "home.html", context={
                "form": form,
                "ballots": ballots,
                "error": "Transaction failed."
            })

        Ballot.objects.create(ballot_id, tx_hash)

        return redirect(request.path)

    return render(request, "home.html", context={"form": BallotCreationForm(), "ballots": ballots})
