

class TagsManager:
    
    def __init__(self):
        self.keys = {
            "skip": "СКИП",
            "inn": "ИНН",
            "ip_fssp": "ИП ФССП",
            "fssp": "БД ФССП",
            "bankruptcy": "Банкротство",
            "jf": "Подсудность",
            "gas": "Суды Онлайн",
            "esia": "ЕСИА Бот"
        }
    
    def format_tags_view(self, sorted_tags_list: list[dict]) -> list[dict]:
        stats = {}
        for k, v in self.keys.items():
            result = {
                "code": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Код (Backend/Frontend)"],
                "inner": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Внутренняя (системная)"],
                "outer": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Внешняя (сайт/источник/вендор)"]
            }
            stats[k] = result
        return stats