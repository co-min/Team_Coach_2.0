# core/context.py

# context = 실행에 필요한 공통 객체를 하나로 묶은 container
# main에서 experimental context 생성
# run_block(context, block_design) 같은 context를 하위 함수에 전달
# run_trial -> choice_segment -> turn


# core/context.py

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExperimentContext:
    display: Any
    agent: Any
    logger: Any

    competence: dict
    synergy: dict

    cumulative_scores: dict[str, float] = field(
        default_factory=lambda: {
            "self": 0.0,
            "agent": 0.0,
        }
    )
