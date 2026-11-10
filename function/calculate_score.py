# function/calculate_score.py

def calculate_turn_score(
    leader,
    animal,
    domain,
    competence,
    synergy,
):
    leader_comp = competence[leader][domain]
    animal_comp = competence[animal][domain]
    pair_synergy = synergy[leader][animal]

    return pair_synergy * (leader_comp + animal_comp)