import pandas as pd
import matplotlib.pyplot as plt
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
            os.mkdir('Reports')
        else:
            pass
        writer = pd.ExcelWriter(f'{dir_name}/1.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Детализация', index=False)
        writer._save()
        
class Plot:
    
    def __init__(self, array_1: list, array_2: list):
        self.array_1 = array_1
        self.array_2 = array_2
        
    
    def make_plot(self, service_name: str):
        plt.plot(self.array_1, self.array_2, marker='o')
        plt.xlabel('Неделя')
        plt.ylabel('Кол-во ошибок, шт.')
        plt.title('СКИП')
        plt.grid()
        plt.show()
        