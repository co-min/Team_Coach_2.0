# window size, fullscreen, path 
SCREEN_SIZE = (1280, 720)
FULLSCREEN = False

BACKGROUND_COLOR = "#171C29"

# norm 단위 이미지 높이 (0.36 → 720px 화면에서 약 130px), 가로는 원본 비율로 자동 계산
ANIMAL_IMAGE_HEIGHT = 0.36

# Duration
FIXATION_DURATION = 1.0
FEEDBACK_DURATION = 2.0
SCORE_DURATION = 1.0

# Agent 선택 장면 (커서 이동 연출)
AGENT_THINK_DURATION = 1.0    # 첫 커서 표시 후 고민 시간
AGENT_MOVE_DURATION = 0.5     # 커서 한 칸 이동 간격
AGENT_CONFIRM_DURATION = 1.5  # 최종 선택 후 유지 시간