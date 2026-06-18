def house_serializer(house) -> dict:
    return {
        "id": house.get("id"),
        "_id": str(house["_id"]),
        "title": house.get("title"),
        "price": house.get("price"),
        "description": house.get("description"),
        "image_url": house.get("image_url"),
        "addressable_str": house.get("addressable_str"),
        "area_m2": house.get("area_m2"),
        "status": house.get("status"),
        "residential_number": house.get("residential_number")
    }

def houses_serializer(houses) -> list:
    return [house_serializer(house) for house in houses]
