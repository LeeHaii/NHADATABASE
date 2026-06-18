from fastapi import APIRouter, HTTPException, status
from models.houses import House, UpdateHouse
from config.database import collection_name, get_next_sequence_value
from schema.schemas import house_serializer, houses_serializer

router = APIRouter(
    prefix="/houses",
    tags=["houses"]
)

@router.get("/")
async def get_houses():
    houses = houses_serializer(collection_name.find())
    return houses

@router.get("/{id}")
async def get_house(id: int):
    house = collection_name.find_one({"id": id})
    if house:
        return house_serializer(house)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_house(house: House):
    house_dict = house.model_dump()
    # Generate the auto-incrementing ID
    house_dict["id"] = get_next_sequence_value("house_id")
    _id = collection_name.insert_one(house_dict)
    new_house = collection_name.find_one({"_id": _id.inserted_id})
    return house_serializer(new_house)

@router.put("/{id}")
async def update_house(id: int, house: UpdateHouse):
    # Exclude unset to only update fields provided in the request
    update_data = house.model_dump(exclude_unset=True)
    # Prevent user from modifying the generated id if they try
    update_data.pop("id", None)
    
    if len(update_data) >= 1:
        update_result = collection_name.update_one({"id": id}, {"$set": update_data})
        if update_result.modified_count == 1:
            updated_house = collection_name.find_one({"id": id})
            if updated_house:
                return house_serializer(updated_house)
    
    existing_house = collection_name.find_one({"id": id})
    if existing_house:
        return house_serializer(existing_house)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house(id: int):
    delete_result = collection_name.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
