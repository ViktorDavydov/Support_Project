

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
    
    def make_arrays_for_plots(self, formated_tags: dict) -> list[dict]:
        arrays_for_plots = []  
        for service, issues in formated_tags.items():
            service_name = self.service_names.get(service)
            code_issues_list = issues.get("code")
            inner_issues_list = issues.get("inner")
            outer_issues_list = issues.get("outer")
            
            if code_issues_list:
                code_week_array = list(set([item.get("week") for item in code_issues_list]))
                code_issues_array = []
                for week in code_week_array:
                    temp_issues_count_list = []
                    for item in code_issues_list:
                        if week == item.get("week"):
                            temp_issues_count_list.append(item.get("issues_count"))
                    total_week_issues = sum(temp_issues_count_list)
                    code_issues_array.append(total_week_issues)
            else:
                code_week_array = []
                code_issues_array = []
                
            if inner_issues_list:
                inner_week_array = list(set([item.get("week") for item in inner_issues_list]))
                inner_issues_array = []
                for week in inner_week_array:
                    temp_issues_count_list = []
                    for item in inner_issues_list:
                        if week == item.get("week"):
                            temp_issues_count_list.append(item.get("issues_count"))
                    total_week_issues = sum(temp_issues_count_list)
                    inner_issues_array.append(total_week_issues)
            else:
                inner_week_array = []
                inner_issues_array = []
                
            if outer_issues_list:
                outer_week_array = list(set([item.get("week") for item in outer_issues_list]))
                outer_issues_array = []
                for week in outer_week_array:
                    temp_issues_count_list = []
                    for item in outer_issues_list:
                        if week == item.get("week"):
                            temp_issues_count_list.append(item.get("issues_count"))
                    total_week_issues = sum(temp_issues_count_list)
                    outer_issues_array.append(total_week_issues)
            else:
                outer_week_array = []
                outer_issues_array = []
            
             
            result = {
                service_name: {
                    "code_week_array": code_week_array,
                    "code_issues_array": code_issues_array,
                    "inner_week_array": inner_week_array,
                    "inner_issues_array": inner_issues_array,
                    "outer_week_array": outer_week_array,
                    "outer_issues_array": outer_issues_array
                }
            }
            arrays_for_plots.append(result)
            
        return arrays_for_plots
            
