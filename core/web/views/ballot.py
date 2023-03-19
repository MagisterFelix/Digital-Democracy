import datetime
import json
import random

from django.shortcuts import get_object_or_404, redirect, render

from core.web import bm_user, bm_voting
from core.web.forms import VoteForm
from core.web.models.ballot import Ballot


def ballot_view(request, ballot_id):
    if not request.user.is_authenticated:
        return redirect("login")

    ballot = get_object_or_404(Ballot, id=ballot_id)
    title, options, end_date, votes = bm_voting.get_ballot(ballot.id)
    ballot = {
        "id": ballot.id,
        "tx_hash": ballot.tx_hash,
        "title": title,
        "options": [(index + 1, option) for index, option in enumerate(options)],
        "end_date": datetime.datetime.fromtimestamp(end_date),
        "count_of_votes": sum(votes)
    }
    vote = bm_voting.get_vote(ballot["id"], request.user.passport)

    if datetime.date.today() >= datetime.date.fromtimestamp(end_date):
        ballot["end_date"] = None
        disabled = True

    colors = []

    for seed in range(len(options)):
        random.seed((seed + 2) * 31415)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color = f"rgb({r}, {g}, {b})"

        colors.append(color)

    user = bm_user.get_user(request.user.passport)
    disabled = not user

    if request.method == "POST":
        form = VoteForm(options=ballot["options"], data=request.POST)

        if form.is_valid():
            if user is None:
                return render(request, "ballot.html", context={
                    "form": form,
                    "ballot": ballot,
                    "error": "Permission denied.",
                    "options": options,
                    "votes": votes if sum(votes) else None,
                    "colors": colors
                })

            tx_hash = bm_voting.vote(ballot["id"], request.user.passport, int(form.cleaned_data["option"]))

            if tx_hash is None:
                return render(request, "ballot.html", context={
                    "form": form,
                    "ballot": ballot,
                    "error": "Transaction failed.",
                    "options": options,
                    "votes": votes if sum(votes) else None,
                    "colors": colors
                })

            transaction = bm_voting.get_transaction(tx_hash)
            request.session[ballot_id] = json.dumps(transaction, default=str)

            return redirect(request.path)

    transaction = request.session.get(ballot_id)
    if transaction is not None:
        transaction = json.loads(transaction)
        transaction["block_timestamp"] = datetime.datetime.fromisoformat(transaction["block_timestamp"])

    return render(request, "ballot.html", context={
        "form": VoteForm(options=ballot["options"], selected=vote, disabled=disabled),
        "ballot": ballot,
        "vote": vote,
        "transaction": transaction,
        "options": options,
        "votes": votes if sum(votes) else None,
        "colors": colors
    })
