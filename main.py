from pprint import pprint
from stats import Plot

from zammad_api import ZammadTickets
from stats import Tables

tickets = ZammadTickets(pages=5)
pprint(tickets.all_tickets_list)
tickets_list = tickets.get_tickets_by_period(start_date="15.08.2024", end_date="02.09.2024")
tags = tickets.get_valid_tags(ticket_list=tickets_list)

pprint(tags)

table = Tables(tags_list=tags)
frame = table.to_dataframe()
print(frame)
table.to_excel(dataframe=frame)