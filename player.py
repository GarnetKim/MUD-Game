from item import Item
from utils import format_item

class Player:
    def __init__(self, name: str):
        self.name = name

        # ---------------------
        # 기본 능력치
        # ---------------------
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.atk = 10
        self.defense = 5
        self.gold = 100

        # ---------------------
        # 장비 / 인벤토리
        # ---------------------
        self.weapon: Item = None
        self.armor: Item = None
        self.inventory = []  # type: list[Item]

        # ---------------------
        # 상태 / 전투 로그
        # ---------------------
        self.status_effects: list[str] = []   # ex: ["poison", "burn"]
        self.combat_log: list[str] = []       # combat_log_xxx.txt에도 기록됨
        self.effect_history: list[str] = []   # 스킬/버프 이펙트 기록
        self.set_bonus_history: list[str] = []# 세트 효과 발동 기록

        # ---------------------
        # 스킬 / 쿨타임 / 도감
        # ---------------------
        self.skills: dict[str,int] = {}       # {"heal":1, "fireball":2, ...}
        self.skill_codex: dict[str,int] = {}  # 도감: {스킬명:최대해금레벨}
        self.skill_cooldowns: dict[str,int] = {} # {"heal":2,...}
        self.ultimate_used: bool = False      # 궁극기 1회 제한 여부

        # ---------------------
        # 세트/아이템 도감
        # ---------------------
        self.set_codex_unlocked: dict[str,bool] = {}   # 세트 도감
        self.item_codex_unlocked: dict[str,bool] = {}  # 아이템 도감

        # ---------------------
        # 칭호 시스템
        # ---------------------
        self.titles: list[str] = []           # 보유 칭호
        self.active_title: str|None = None    # 현재 활성화 칭호

        # ---------------------
        # 옵션 / 환경 설정
        # ---------------------
        self.autoload_enabled: bool = True              # 자동 로드 여부
        self.inventory_sort_preference: str = "희귀도"  # 정렬 선호도

    # -------------------------
    # 장비 장착
    # -------------------------
    def equip(self, item: Item):
        if item.type == "weapon":
            self.weapon = item
        elif item.type == "armor":
            self.armor = item

    # -------------------------
    # 상태 요약
    # -------------------------
    def summary(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": f"{self.hp}/{self.max_hp}",
            "mp": f"{self.mp}/{self.max_mp}",
            "atk": self.atk,
            "def": self.defense,
            "gold": self.gold,
            "weapon": self.weapon.name if self.weapon else None,
            "armor": self.armor.name if self.armor else None,
            "titles": self.titles,
            "active_title": self.active_title,
        }


def show_player_summary(player: Player):
    print("\n──────── [플레이어 상태 요약] ────────")
    print(f"👤 이름: {player.name}")
    print(f"⭐ 레벨: {player.level}")
    print(f"❤️ HP: {player.hp}/{player.max_hp}")
    print(f"🔮 MP: {player.mp}/{player.max_mp}")
    print(f"💰 골드: {player.gold}")
    print(f"🗡 무기: {format_item(player.weapon) if player.weapon else '없음'}")
    print(f"🛡 방어구: {format_item(player.armor) if player.armor else '없음'}")

    # 칭호
    if player.titles:
        print("🏷 보유 칭호:", ", ".join(player.titles))
        if player.active_title:
            print(f"👉 현재 활성 칭호: {player.active_title}")
        else:
            print("👉 현재 활성 칭호: 없음")
    else:
        print("🏷 칭호: 없음")

    # 총합 내성 계산 (장비 합산)
    from battle import calculate_total_resistances
    total_res = calculate_total_resistances(player)
    if total_res:
        parts = [f"{k}:{v}%" for k, v in total_res.items()]
        print(f"🛡 총합 내성: {', '.join(parts)}")
    else:
        print("🛡 총합 내성: 없음")

    print("────────────────────────────────────\n")