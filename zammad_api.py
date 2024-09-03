
import requests
from datetime import datetime, timedelta
from pprint import pprint
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class ZammadTickets:
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ.get("ZAMMAD_TOKEN")
    }
    
    issues_tags = [
    "Код (Backend/Frontend)",
    "Внутренняя (системная)",
    "Внешняя (сайт/источник/вендор)"
    ]  
       
    
    def __init__(self, pages: int) -> None:
        self.ticket_url = os.environ.get("TICKET_URL")
        self.tags_url = os.environ.get("TAGS_URL")
        self.pages = pages
        self.all_tickets_list = self.get_all_ticket()
    
    
    def get_all_ticket(self) -> list[dict]:
        '''
        Наполнение списка всех тикетов Заммад с указанием кол-ва страниц
        '''
        result_list = []
        for page in range(1, self.pages + 1):
            response_ticket_list = requests.get(url=self.ticket_url + str(page), headers=self.headers)
            result_list.extend(response_ticket_list.json())
        return result_list
    
    
    def get_tickets_by_period(self, start_date: str, end_date: str) -> list[dict]:
        '''
        Получение списка тикетов за период. Добавление номера недели создания тикета.
        '''
        tickets_by_period = []
        if self.all_tickets_list:
            start_date = datetime.strptime(start_date, "%d.%m.%Y")
            end_date = datetime.strptime(end_date, "%d.%m.%Y") + timedelta(hours=23, minutes=59, seconds=59)
            for ticket in self.all_tickets_list:
                create_date = datetime.strptime(ticket.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=3)
                if start_date <= create_date <= end_date:
                    ticket['week'] = create_date.isocalendar()[1]
                    tickets_by_period.append(ticket)
            return tickets_by_period
        return []
    
    def get_valid_tags(self, ticket_list: list[dict]) -> list[dict]:
        '''
        Получение тегов с наличием поля типа ошибки из списка issues_tags
        '''
        tags_list = []
        for ticket in ticket_list:
            tags = requests.get(url=self.tags_url + str(ticket.get('id')), headers=self.headers)
            week = ticket.get('week')
            ticket_tags_list = tags.json().get('tags')
            if any(map(lambda issue: issue in ticket_tags_list, self.issues_tags)):
                tags_info = {
                    'service': ticket_tags_list[0],
                    'issue_type': ticket_tags_list[1],
                    'issues_count': int(ticket_tags_list[2]),
                    'after_release': ticket_tags_list[3][15:],
                    'week': week
                }
                tags_list.append(tags_info)
        return tags_list


            
        
            
            
    
    


    