import os
import datetime
import csv

# ------------------------
# 로그 저장
# ------------------------
def log_event(player, message: str):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"

    # 메모리에도 저장
    player.combat_log.append(log_line)

    # 날짜별 로그 파일
    fname = f"combat_log_{now.strftime('%Y-%m-%d')}.txt"
    with open(fname, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


# ------------------------
# 검색/필터 (색상 강조)
# ------------------------
def search_logs(keyword_list, date=None, append=False):
    """키워드 여러 개 동시 검색"""
    if not isinstance(keyword_list, list):
        keyword_list = [keyword_list]

    fname = f"combat_log_{date}.txt" if date else latest_logfile()
    if not fname or not os.path.exists(fname):
        print("⚠️ 로그 파일이 없습니다.")
        return []

    results = []
    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            if any(k.lower() in line.lower() for k in keyword_list):
                results.append(colorize(line.strip()))

    # 저장 옵션
    if results:
        out_name = make_filtered_filename(keyword_list, date)
        mode = "a" if append else "w"
        with open(out_name, mode, encoding="utf-8") as f:
            for r in results:
                f.write(strip_ansi(r) + "\n")
        print(f"💾 검색 결과 저장: {out_name}")

    for r in results:
        print(r)
    return results


def latest_logfile():
    files = [f for f in os.listdir() if f.startswith("combat_log_") and f.endswith(".txt")]
    return max(files, default=None, key=os.path.getmtime)


def make_filtered_filename(keywords, date=None):
    base = "_".join(keywords)
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    if date:
        return f"combat_log_{date}_{base}.txt"
    else:
        return f"combat_log_{now}_{base}.txt"


# ------------------------
# 색상 강조
# ------------------------
def colorize(line: str) -> str:
    if "치명타" in line or "crit" in line.lower():
        return f"\033[91m{line}\033[0m"  # 빨강
    if "흡혈" in line or "drain" in line.lower():
        return f"\033[92m{line}\033[0m"  # 초록
    if "방패" in line or "shield" in line.lower():
        return f"\033[94m{line}\033[0m"  # 파랑
    return line

def strip_ansi(s: str) -> str:
    """색상 코드 제거 (파일 저장용)"""
    import re
    return re.sub(r"\033\[[0-9;]*m", "", s)


# ------------------------
# CSV/Excel 내보내기
# ------------------------
def export_logs_to_csv(date=None):
    fname = f"combat_log_{date}.txt" if date else latest_logfile()
    if not fname or not os.path.exists(fname):
        print("⚠️ 로그 파일이 없습니다.")
        return

    out_csv = fname.replace(".txt", ".csv")
    with open(fname, "r", encoding="utf-8") as f, open(out_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["시간", "메시지"])
        for line in f:
            if line.strip():
                if line.startswith("["):
                    time_part, msg = line.split("]", 1)
                    time_str = time_part.strip("[]")
                    writer.writerow([time_str, msg.strip()])
                else:
                    writer.writerow(["", line.strip()])
    print(f"💾 로그 CSV 저장 완료: {out_csv}")


# ------------------------
# 페이지네이션 (20줄씩)
# ------------------------
def paginate_logs(date=None, page_size=20):
    fname = f"combat_log_{date}.txt" if date else latest_logfile()
    if not fname or not os.path.exists(fname):
        print("⚠️ 로그 파일이 없습니다.")
        return
    with open(fname, "r", encoding="utf-8") as f:
        lines = f.readlines()
    page = 0
    while page * page_size < len(lines):
        chunk = lines[page*page_size:(page+1)*page_size]
        print(f"\n📖 로그 페이지 {page+1}")
        for line in chunk:
            print(colorize(line.strip()))
        if (page+1)*page_size >= len(lines):
            break
        cmd = input("계속 보려면 Enter (중단 q): ")
        if cmd.strip().lower() == "q":
            break
        page += 1


# ------------------------
# 실시간 모니터링
# ------------------------
def monitor_logs(date=None):
    fname = f"combat_log_{date}.txt" if date else latest_logfile()
    if not fname or not os.path.exists(fname):
        print("⚠️ 로그 파일이 없습니다.")
        return

    print(f"👀 실시간 로그 모니터링 시작: {fname}")
    with open(fname, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)  # 파일 끝으로
        while True:
            line = f.readline()
            if not line:
                import time; time.sleep(0.5)
                continue
            print(colorize(line.strip()))