import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import datetime

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
    
    def make_and_save_plots(self, arrays_dict: dict):
        
        for service_name, arrays in arrays_dict.items():
            plt.figure(figsize=(20,4))
            
            x = np.array(arrays["week_array"])

            # Оставляем только целые значения для оси X
            xticks = np.arange(np.floor(x.min()), np.ceil(x.max()) + 1, 1)  # Целые значения
            
            
            # График ошибок Код (Backend/Frontend)
            plt.subplot(1, 3, 1)
            y = np.array(arrays["code_issues_array"])
            if sum(arrays["code_issues_array"]) == 0:
                empty_line_array = [1 for _ in range(len(arrays["code_issues_array"]))] # Для спуска нулевой линии вниз
            yticks = np.arange(np.floor(y.min()), np.ceil(y.max()) + 1, 1)  # Целые значения
            plt.xlabel("Недели\nКод (Backend/Frontend)")
            plt.ylabel("Кол-во возникновений ошибок, шт.")
            plt.plot(x, y, marker = "o", color="blue")
            plt.plot(x, empty_line_array, linewidth=0)
            
            plt.xticks(xticks)  # Устанавливаем только целые значения для X
            plt.yticks(yticks)  # Устанавливаем только целые значения для Y
            plt.title(service_name)
            
            # График ошибок "Внутренняя (системная)"
            plt.subplot(1, 3, 2)
            y = np.array(arrays["inner_issues_array"])
            yticks = np.arange(np.floor(y.min()), np.ceil(y.max()) + 1, 1)  # Целые значения
            
            if sum(arrays["inner_issues_array"]) == 0:
                empty_line_array = [1 for _ in range(len(arrays["inner_issues_array"]))] # Для спуска нулевой линии вниз
                
            plt.xlabel("Недели\nВнутренняя (системная)")
            plt.plot(x, y, marker = "o", color="orange")
            plt.plot(x, empty_line_array, linewidth=0)
            
            plt.xticks(xticks)  # Устанавливаем только целые значения для X
            plt.yticks(yticks)  # Устанавливаем только целые значения для Y
            plt.title(service_name)
            
            # График ошибок "Внешняя (сайт/источник/вендор)"
            plt.subplot(1, 3, 3)
            y = np.array(arrays["outer_issues_array"])
            yticks = np.arange(np.floor(y.min()), np.ceil(y.max()) + 1, 1)  # Целые значения
            
            if sum(arrays["outer_issues_array"]) == 0:
                empty_line_array = [1 for _ in range(len(arrays["outer_issues_array"]))] # Для спуска нулевой линии вниз
                
            plt.xlabel("Недели\nВнешняя (сайт/источник/вендор)")
            plt.plot(x, y, marker = "o", color="green")
            plt.plot(x, empty_line_array, linewidth=0)
            
            plt.xticks(xticks)  # Устанавливаем только целые значения для X
            plt.yticks(yticks)  # Устанавливаем только целые значения для Y
            plt.title(service_name)
            
            plt.tight_layout()
            
            base_dir_name = 'Plots'
            if not os.path.exists(base_dir_name):
                os.mkdir(base_dir_name)
            
            dir_name = f"Графики_{str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))}"
            if not os.path.exists(f"{base_dir_name}/{dir_name}"):
                os.mkdir(f"{base_dir_name}/{dir_name}")
            
            plt.savefig(f"{base_dir_name}/{dir_name}/{service_name}")
        