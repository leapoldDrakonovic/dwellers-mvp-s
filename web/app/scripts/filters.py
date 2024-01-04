def range_filter(values: list, range_side: str = 'min'):
    values = list(values) if type(values != list) else values
    if len(values) > 0:
        if range_side == 'min':
            return min(values)
        elif range_side == 'max':
            return max(values)
    return -1


def simple_filter(table, filters: dict):
    query = table.select()
    if 'group_id' in filters.keys() and 'city' in filters.keys() and 'country' in filters.keys(
    ) and '!id' in filters.keys() and 'limit' in filters.keys():
        query = query.where((table.id == filters['group_id'] or table.city == filters['city']
                            or table.country == filters['country']) and table.id != filters['!id']).limit(filters['limit'])
        return query.execute()
    elif 'group_id' in filters.keys() and '!id' in filters.keys():
        query = query.where(
            table.id != filters['!id'] and table.group_id == filters['group_id'])
        return query.execute()

    for filter_key, filter_value in filters.items():
        if filter_key == 'group_id':
            query = query.where(table.id == filter_value)
        elif filter_key == 'city':
            query = query.where(table.city == filter_value)
        elif filter_key == 'country':
            query = query.where(table.country == filter_value)
        elif filter_key == 'limit':
            query = query.limit(filter_value)
    return query.execute()


def apply_filter(table, filters, flats=None):
    query = table.select()
    for filter_key, filter_value in filters.items():
        if filter_key == 'name':
            query = query.where(
                (table.name.contains(filter_value))
                | (table.address.contains(filter_value))
                | (table.city.contains(filter_value))
                | (table.country.contains(filter_value))
                | (table.city__lang_hebrew.contains(filter_value))
                | (table.country__lang_hebrew.contains(filter_value))
                | (table.address__lang_hebrew.contains(filter_value))
            )
        elif filter_key == 'type_of_building':
            query = query.where(table.type_of_building.in_(filter_value))
        elif filter_key == 'rooms':
            table_ids = []
            for flat in flats.select().where(flats.rooms.in_(filter_value)):
                if flat.group_id not in table_ids:
                    table_ids.append(flat.group_id)
            query = query.where(table.id.in_(table_ids))
        elif filter_key == 'all_size_m2_min':
            table_ids = []
            if 'all_size_m2_max' not in filters.keys():
                for flat in flats.select().where(flats.all_size_m2 >= filter_value):
                    if flat.group_id not in table_ids:
                        table_ids.append(flat.group_id)
            else:
                for flat in flats.select().where(
                    (flats.all_size_m2 >= filter_value) & (
                        flats.all_size_m2 <= filters['all_size_m2_max'])):
                    if flat.group_id not in table_ids:
                        table_ids.append(flat.group_id)
            query = query.where(table.id.in_(table_ids))
        elif filter_key == 'all_size_m2_max':
            table_ids = []
            for flat in flats.select().where(flats.all_size_m2 <= filter_value):
                if flat.group_id not in table_ids:
                    table_ids.append(flat.group_id)
            query = query.where(table.id.in_(table_ids))
        elif filter_key == 'price_min':
            table_ids = []
            if 'price_max' not in filters.keys():
                for flat in flats.select().where(flats.price >= filter_value):
                    if flat.group_id not in table_ids:
                        table_ids.append(flat.group_id)
            else:
                for flat in flats.select().where(
                    (flats.price >= filter_value) & (
                        flats.price <= filters['price_max'])):
                    if flat.group_id not in table_ids:
                        table_ids.append(flat.group_id)
            query = query.where(table.id.in_(table_ids))
        elif filter_key == 'price_max':
            table_ids = []
            for flat in flats.select().where(flats.price <= filter_value):
                if flat.group_id not in table_ids:
                    table_ids.append(flat.group_id)
            query = query.where(table.id.in_(table_ids))
    return query.execute()
