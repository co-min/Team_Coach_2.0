
# core/block.py

from core.trial import run_trial

# 최초 버전의 block.py
# 기본 block 이후 추가해야하는 기능
    # retention 기존 동물 유지 및 새로운 동물 교체
    # selective reversal에서 특정 attribute 변경
    # condition counterbalancing
    # block 종료 후 attribute rating

def run_block(context, block_design):
    """Run all trials in one block."""

    # 1. Initialize block scores
    context.cumulative_scores = {
        "self": 0.0,
        "agent": 0.0,
    }

    # 2. Run trials
    trial_states = []

    for trial_design in block_design["trials"]:

        state = run_trial(
            context=context,
            trial_design=trial_design,
        )

        trial_states.append(state)

    # 3. Return block results
    return trial_states
