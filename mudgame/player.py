from mudgame.item import Item

class Player:
    def __init__(self, name="용사"):
        self.name = name
        self.level = 1
        self.exp = 0
        self.hp = 100
        self.max_hp = 100
        self.mp = 30
        self.max_mp = 30
        self.atk = 10
        self.defense = 5
        self.gold = 100
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.titles = []       # 칭호 보유
        self.active_title = None
        self.codex = {"items": set(), "sets": set(), "skills": set()}  # 도감
        self.skills = {"Heal": {"level": 1, "cooldown": 3}}
        self.available_skills = ["Heal", "Fireball", "Shield Bash"]  # 해금 후보

    def add_exp(self, amount, log=None):
        self.exp += amount
        if log:
            log(f"📊 EXP +{amount} (현재 {self.exp})")
        # 레벨업 체크
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.max_mp += 5
            self.mp = self.max_mp
            if log:
                log(f"⬆️ 레벨업! Lv.{self.level} 도달!")
            # 레벨업 시 스킬 선택 플래그
            import streamlit as st
            st.session_state.skill_choice_open = True
            
    def add_item(self, item, log=None):
        self.inventory.append(item)
        self.codex["items"].add(item.name)
        if log:
            log(f"🎁 아이템 획득: {item.display_name()}")

    def add_gold(self, amount, log=None):
        self.gold += amount
        if log:
            log(f"💰 Gold +{amount} (현재 {self.gold})")

    def equip(self, item):
        if item.type == "weapon":
            self.weapon = item
        elif item.type == "armor":
            self.armor = item

    def use_item(self, item_name, count=1, log=None):
        used = 0
        for _ in range(count):
            found = None
            for i in self.inventory:
                if i.name == item_name:
                    found = i
                    break
            if not found:
                if used == 0 and log:
                    log(f"❌ {item_name} 없음")
                break

            # 소비 아이템 효과
            if found.name == "체력 포션":
                heal = min(50, self.max_hp - self.hp)
                self.hp += heal
                if log: log(f"💊 체력 포션 사용! HP +{heal} → {self.hp}/{self.max_hp}")
            elif found.name == "마나 포션":
                restore = min(20, self.max_mp - self.mp)
                self.mp += restore
                if log: log(f"🔮 마나 포션 사용! MP +{restore} → {self.mp}/{self.max_mp}")
            elif found.name == "만능 포션":
                self.hp = self.max_hp
                self.mp = self.max_mp
                if log: log(f"🌈 만능 포션 사용! HP/MP 전부 회복!")

            # 사용 후 인벤토리에서 제거
            self.inventory.remove(found)
            used += 1

        return used > 0

    def stats(self):
        atk = self.atk + (self.weapon.attack if self.weapon else 0)
        defense = self.defense + (self.armor.defense if self.armor else 0)
        return atk, defense
 