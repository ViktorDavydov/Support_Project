import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class Tables:
    
    def __init__(self, tags_list: list) -> None:
        self.tags_list = tags_list
        self.service_list = [item.get('service') for item in self.tags_list]
        self.issue_type_list = [item.get('issue_type') for item in self.tags_list]
        self.issues_count = [item.get('issues_count') for item in self.tags_list]
        self.after_release_list = [item.get('after_release') for item in self.tags_list]
        self.week_list = [item.get('week') for item in self.tags_list]
        
    def to_dataframe(self):
        stats = pd.DataFrame({
            'Сервис': self.service_list,
            'Тип ошибки': self.issue_type_list,
            'Кол-во возникновений, шт.': self.issues_count,
            'Послерелизная': self.after_release_list,
            'Неделя': self.week_list
        })
        
        return stats
        
    def to_excel(self, dataframe) -> None:
        dir_name = 'Reports'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        else:
            pass
        writer = pd.ExcelWriter(f'{dir_name}/1.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Детализация', index=False)
        writer._save()
        
class Plot:        
    
    def make_plot(self, arrays_dict: dict):
        
        for service_name, arrays in arrays_dict.items():
            plt.figure(figsize=(16,5))
            plt.title(service_name)
            
            # График ошибок Код (Backend/Frontend)
            plt.subplot(1, 3, 1)
            x = np.array(arrays["code_week_array"])
            y = np.array(arrays["code_issues_array"])
            plt.xlabel("Недели\nКод (Backend/Frontend)")
            plt.ylabel("Кол-во ошибок, шт.")
            plt.xticks(arrays["code_week_array"])
            plt.yticks(arrays["code_issues_array"])
            plt.plot(x, y, marker = "o")
            
            # График ошибок "Внутренняя (системная)"
            plt.subplot(1, 3, 2)
            x = np.array(arrays["inner_week_array"])
            y = np.array(arrays["inner_issues_array"])
            plt.xlabel("Недели\nВнутренняя (системная)")
            plt.ylabel("Кол-во ошибок, шт.")
            plt.xticks(arrays["inner_week_array"])
            plt.yticks(arrays["inner_issues_array"])
            plt.plot(x, y, marker = "o")
            
            # График ошибок "Внешняя (сайт/источник/вендор)"
            plt.subplot(1, 3, 3)
            x = np.array(arrays["outer_week_array"])
            y = np.array(arrays["outer_issues_array"])
            plt.xlabel("Недели\nВнешняя (сайт/источник/вендор)")
            plt.ylabel("Кол-во ошибок, шт.")
            plt.xticks(arrays["outer_week_array"])
            plt.yticks(arrays["outer_issues_array"])
            plt.plot(x, y, marker = "o")
            
            plt.show()
        
        # dir_name = 'Plots'
        # if not os.path.exists(dir_name):
        #     os.mkdir(dir_name)
        # else:
        #     pass
        # plt.savefig(f"{dir_name}/fig_1")
        
        