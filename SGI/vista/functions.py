from flask import request
from datetime import datetime

def paginate(data,route_pagination):
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(data) + per_page - 1) // per_page
    items_on_page = data[start:end]    
    return items_on_page, total_pages, route_pagination,page

def now():
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d')
    return formatted_now

