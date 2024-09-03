from pprint import pprint
from stats import Plot

from zammad_api import ZammadTickets
from stats import Tables
from tags_manager import TagsManager

tickets = ZammadTickets(pages=5)
tickets_list = tickets.get_tickets_by_period(start_date="15.08.2024", end_date="03.09.2024")
tags = tickets.get_valid_tags(ticket_list=tickets_list)

table = Tables(tags_list=tags)
frame = table.to_dataframe()
print(frame)
valid_tags = tickets.get_valid_tags(tickets_list)

sorted_tags = tickets.tags_sort_by_week(tags_list=valid_tags)

tags_manager = TagsManager()

pprint(tags_manager.format_tags_view(sorted_tags_list=sorted_tags))

# table.to_excel(dataframe=frame)