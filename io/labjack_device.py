# 공통 : connect / send / exit

# LabJack T4 TTL 트리거 디바이스
#
# 핀 구성:
#   EIO0~EIO7 : 트리거 코드값 (8비트)
#   CIO0      : latch (strobe) — 수신 장비가 rising edge에서 EIO 값을 캡처


import queue
import threading
import time
from dataclasses import dataclass

from labjack import ljm


@dataclass
class TriggerRecord:
    code: int
    t_request: float
    t_latch: float | None


class LabJackDevice:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose

        self.handle = None
        self.records = []
        self.errors = []

        self.queue = queue.Queue()
        self.worker = None
        self.closed = False

        # TTL timing (seconds)
        self.setup_s = 0.002
        self.pulse_s = 0.010
        self.hold_s = 0.001

    # 1. 장치 연결
    def open(self):
        if self.worker is not None:
            raise RuntimeError("LabJack is already open")

        if not self.dry_run:
            self.handle = ljm.openS("T4", "USB", "ANY")

            try:
                ljm.eWriteNames(
                    self.handle,
                    4,
                    ["EIO_DIRECTION", "EIO_STATE",
                     "CIO_DIRECTION", "CIO_STATE"],
                    [255, 0, 15, 0],
                )
            except Exception:
                ljm.close(self.handle)
                self.handle = None
                raise

        self.closed = False
        self.worker = threading.Thread(
            target=self._worker_loop,
            daemon=False,
        )
        self.worker.start()
        return self

    # 2. 비동기 전송 요청
    def send_async(self, code):
        if self.worker is None or self.closed:
            raise RuntimeError("LabJack is not open")

        code = int(code)
        if not 0 <= code <= 255:
            raise ValueError("TTL code must be 0–255")

        self.queue.put((code, time.perf_counter(), None))

    # 3. 동기 전송 요청
    def send(self, code):
        done = threading.Event()

        if self.worker is None or self.closed:
            raise RuntimeError("LabJack is not open")

        code = int(code)
        if not 0 <= code <= 255:
            raise ValueError("TTL code must be 0–255")

        self.queue.put((code, time.perf_counter(), done))
        done.wait()

        self._check_errors()

    # 4. 다음 화면 전환에 맞춰 요청
    def send_on_flip(self, win, code):
        win.callOnFlip(self.send_async, code)

    # 5. Queue 처리 (전용 스레드)
    def _worker_loop(self):
        while True:
            item = self.queue.get()

            if item is None:
                self.queue.task_done()
                break

            code, t_request, done = item

            try:
                t_latch = self._write_pulse(code)

                self.records.append(
                    TriggerRecord(code, t_request, t_latch)
                )

                if self.verbose:
                    print(f"TTL sent: {code}")

            except Exception as error:
                self.errors.append((code, error))

            finally:
                if done is not None:
                    done.set()

                self.queue.task_done()

    # 6. 실제 TTL 신호 생성
    def _write_pulse(self, code):
        if self.dry_run:
            return None

        try:
            # Set data pins
            ljm.eWriteName(self.handle, "EIO_STATE", code)
            self._wait(self.setup_s)

            # Latch HIGH
            ljm.eWriteName(self.handle, "CIO_STATE", 1)
            t_latch = time.perf_counter()
            self._wait(self.pulse_s)

            # Latch LOW
            ljm.eWriteName(self.handle, "CIO_STATE", 0)
            self._wait(self.hold_s)

            return t_latch

        finally:
            # 신호를 LOW로 복귀시키도록 시도
            if self.handle is not None:
                try:
                    ljm.eWriteName(self.handle, "CIO_STATE", 0)
                    ljm.eWriteName(self.handle, "EIO_STATE", 0)
                except Exception:
                    pass

    @staticmethod
    def _wait(seconds):
        end = time.perf_counter() + seconds
        while time.perf_counter() < end:
            pass

    def _check_errors(self):
        if self.errors:
            code, error = self.errors[0]
            raise RuntimeError(
                f"TTL transmission failed (code={code})"
            ) from error

    # 7. 모든 전송 완료 대기
    def flush(self):
        self.queue.join()
        self._check_errors()

    # 8. 장치 종료
    def close(self):
        if self.worker is None:
            return

        self.closed = True
        self.queue.put(None)
        self.worker.join()
        self.worker = None

        if self.handle is not None:
            ljm.close(self.handle)
            self.handle = None

        self._check_errors()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc, tb):
        self.close()
