import sys
from config.database import collection_name, counters_collection, get_next_sequence_value

def generate_houses():
    houses = []
    
    # We want 32 houses total.
    # Each floor has 4 rooms: room 1 to 4.
    # Floor numbers: 1 to 8.
    # Floor 1: P101, P102, P103, P104
    # ...
    # Floor 8: P801, P802, P803, P804 (which makes 32)
    
    count = 0
    for floor in range(1, 9):
        for room in range(1, 5):
            if count >= 32:
                break
                
            room_str = f"P{floor}0{room}"
            title = room_str
            addressable_str = room_str.lower()
            
            # Vary price: base is 2.5B, adds 150M per floor, and 50M per room index
            price = 2500000000 + (floor * 150000000) + (room * 50000000)
            
            # Vary description, bedrooms, area, residential number based on room type
            # Room 1: 1 bedroom, smaller area
            # Room 2 & 3: 2 bedrooms, medium area
            # Room 4: 3 bedrooms, larger area
            if room == 1:
                area = 60.0 + (floor * 1.5)
                desc = "nha dep 1 ngu"
                residential_number = 2
            elif room in (2, 3):
                area = 85.0 + (floor * 2.0)
                desc = f"nha dep 2 ngu, phong {room}"
                residential_number = 4
            else:  # room == 4
                area = 115.0 + (floor * 2.5)
                desc = "nha dep 3 ngu rong rai"
                residential_number = 6
                
            image_url = "https://www.renderinghub.com/wp-content/uploads/2020/08/3d-Floor-plan-02-b.jpg"
                
            # Vary status: mostly Available, some Rented/Sold
            if (floor + room) % 4 == 0:
                status = "Rented"
            elif (floor + room) % 7 == 0:
                status = "Sold"
            else:
                status = "Available"
                
            house = {
                "title": title,
                "price": price,
                "description": desc,
                "image_url": image_url,
                "addressable_str": addressable_str,
                "area_m2": round(area, 1),
                "status": status,
                "residential_number": residential_number
            }
            houses.append(house)
            count += 1
            
    return houses

def main():
    clear_db = "--clear" in sys.argv
    
    if clear_db:
        print("Clearing the existing houses collection...")
        collection_name.delete_many({})
        print("Resetting sequence counters...")
        counters_collection.update_one(
            {"_id": "house_id"},
            {"$set": {"sequence_value": 0}},
            upsert=True
        )
        print("Database cleared and counter reset.")
        
    houses = generate_houses()
    print(f"Generated {len(houses)} houses.")
    
    inserted_count = 0
    for h in houses:
        h["id"] = get_next_sequence_value("house_id")
        collection_name.insert_one(h)
        inserted_count += 1
        print(f"Inserted: {h['title']} (ID: {h['id']}) - Price: {h['price']:,} - Area: {h['area_m2']}m2")
        
    print(f"\nSuccessfully inserted {inserted_count} houses into MongoDB!")

if __name__ == "__main__":
    main()
