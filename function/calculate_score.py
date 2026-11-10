# function/calculate_score.py

def calculate_turn_score(
    leader: str,
    animal: str,
    domain: str,
    competence: dict,
    synergy: dict,
) -> float:
    """Calculate the score for one teammate selection."""

    leader_comp = competence[leader][domain]
    animal_comp = competence[animal][domain]
    pair_synergy = synergy[leader][animal]

    turn_score = pair_synergy * (leader_comp + animal_comp)

    return turn_score


## 아래와 같은 데이터 구조 필요.
# synergy = {
#     "self": {
#         "A": 1.0,
#         "B": 1.5,
#     },
#     "agent": {
#         "A": 1.2,
#         "B": 0.8,
#     },
# }