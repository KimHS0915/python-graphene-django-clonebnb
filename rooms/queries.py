from .models import Room
from .types import RoomListResponse


def resolve_rooms(self, info, page=1):
    if page < 1:
        page = 1
    page_size = 5
    rooms = Room.objects.all()[page_size * (page - 1):page_size * page]
    total = Room.objects.count()
    return RoomListResponse(arr=rooms, total=total)


def resolve_room(self, info, id):
    return Room.objects.get(id=id)
