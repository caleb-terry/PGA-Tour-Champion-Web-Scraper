"""_summary_
"""


def present_tour_schedule(data: str):
    """
    Present the data in a user-friendly format.
    """
    for month in data["props"]["pageProps"]["schedule"]["completed"]:
        print(month["month"])
        for tournament in month["tournaments"]:
            print(
                f'{tournament["champion"]} - {tournament["tournamentName"]} - {tournament["championEarnings"]}'
            )
