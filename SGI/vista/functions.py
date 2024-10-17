from flask import request
from datetime import datetime

<<<<<<< HEAD
def paginate(data,route_pagination):
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(data) + per_page - 1) // per_page
    items_on_page = data[start:end]    
    return items_on_page, total_pages, route_pagination,page
=======
def paginate(data, route_pagination):
    try:
        page = max(1, request.args.get('page', 1, type=int))
        per_page = 10  # Aumentado a 10 para mostrar más elementos por página
        total_items = len(data)
        total_pages = (total_items + per_page - 1) // per_page
        page = min(page, total_pages)  # Asegura que la página no exceda el total de páginas
        
        start = (page - 1) * per_page
        end = min(start + per_page, total_items)
        
        items_on_page = data[start:end]
        return items_on_page, total_pages, route_pagination, page
    except Exception as e:
        print(f"Error en la función paginate: {str(e)}")
        return [], 1, route_pagination, 1  # Valores por defecto en caso de error
>>>>>>> d57e711f4488251d32952eec002d502a4355f9b6

def now():
    return datetime.now().strftime('%Y-%m-%d')