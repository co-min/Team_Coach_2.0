
# main.py

from core.context import ExperimentContext
from core.block import run_block
from function.agent import Agent


def main():

    # 1. 실제 Attribute 값 (테스트용)
    competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 5},
        "A": {"cooking": 8},
        "B": {"cooking": 4},
        "C": {"cooking": 6},
        "D": {"cooking": 3},
    }

    synergy = {
        "self": {
            "A": 3, "B": 2, "C": 1, "D": 2
        },
        "agent": {
            "A": 2, "B": 1, "C": 3, "D": 2
        },
    }

    # 2. Create shared objects
    agent = Agent(seed=42)

    # 실제 Display / Logger 구현과 연결해야 함
    display = create_display()
    logger = create_logger()

    # 3. Create ExperimentContext
    context = ExperimentContext(
        display=display,
        agent=agent,
        logger=logger,
        competence=competence,
        synergy=synergy,
    )

    # 4. Example block design
    block_design = {
        "block_type": "initial_learning",
        "condition": "competence_hint",
        "trials": [
            {
                "domain": "cooking",
                "animals": ["A", "B", "C", "D"],
                "actor_order": ["self", "agent"],
                "hint_colors": {
                    "A": "#2BB830",
                    "B": "#FF1515",
                    "C": "#F3E221",
                    "D": "#FF1515",
                },
            },
        ],
    }

    # 5. Run block
    run_block(context, block_design)


if __name__ == "__main__":
    main()
