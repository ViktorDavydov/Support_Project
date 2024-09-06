import datetime

class TagsManager:
    
    service_names = {
            "skip": "СКИП",
            "inn": "ИНН",
            "ip_fssp": "ИП ФССП",
            "fssp": "БД ФССП",
            "bankruptcy": "Банкротство",
            "jf": "Подсудность",
            "gas": "Суды Онлайн",
            "esia": "ЕСИА Бот"
        }

    def tags_sort_by_week(self, tags_list: list[dict]) -> list[dict]:
        sorted_tags_list = sorted(tags_list, key=lambda x: x['week'])
        return sorted_tags_list
    
    def format_tags_view(self, sorted_tags_list: list[dict]) -> dict:
        stats_dict = {}
        for k, v in self.service_names.items():
            result = {
                "code": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Код (Backend/Frontend)"],
                "inner": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Внутренняя (системная)"],
                "outer": [item for item in sorted_tags_list if item.get('service') == v and item.get("issue_type") == "Внешняя (сайт/источник/вендор)"]
            }
            stats_dict[k] = result
        return stats_dict
    
    def make_arrays_for_plots(self, formated_tags: dict, start_date: str, end_date: str) -> dict:
        '''
        Создание arrays для графиков
        '''
        arrays_for_plots = {}
        longest_week_list = []
        
        # Генерация списка недель
        
        start_week = datetime.datetime.strptime(start_date, '%d.%m.%Y')
        end_week = datetime.datetime.strptime(end_date, '%d.%m.%Y')
        weeks_list = [start_week.isocalendar()[1], end_week.isocalendar()[1]]
        
        week_delta = weeks_list[-1] - weeks_list[0]
        
        for week in range(1, week_delta):
            weeks_list.append(weeks_list[0] + week)
        
        longest_week_list = sorted((weeks_list))
        
        # Сбор списков ошибок длиной равному наиболее длинному списку недель
                
        for service, issues in formated_tags.items():
            
            code_issues_list = issues.get("code")
            inner_issues_list = issues.get("inner")
            outer_issues_list = issues.get("outer")
            service_name = self.service_names.get(service)
            
            code_issues_array = []
            inner_issues_array = []
            outer_issues_array = []
            for week in longest_week_list:
                total_code_week_issues = sum([item.get("issues_count") for item in code_issues_list if week == item.get("week")])
                total_inner_week_issues = sum([item.get("issues_count") for item in inner_issues_list if week == item.get("week")])
                total_outer_week_issues = sum([item.get("issues_count") for item in outer_issues_list if week == item.get("week")])
                
                if total_code_week_issues > 0:
                    code_issues_array.append(total_code_week_issues)
                else:
                    code_issues_array.append(0)
                    
                if total_inner_week_issues > 0:
                    inner_issues_array.append(total_inner_week_issues)
                else:
                    inner_issues_array.append(0)
                
                if total_outer_week_issues > 0:
                    outer_issues_array.append(total_outer_week_issues)
                else:
                    outer_issues_array.append(0)

            result = {
                    "code_issues_array": code_issues_array,
                    "inner_issues_array": inner_issues_array,
                    "outer_issues_array": outer_issues_array,
                    "week_array": longest_week_list
                    }
            
            arrays_for_plots[service_name] = result
            
        return arrays_for_plots
            
