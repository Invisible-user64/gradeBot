from sqlalchemy import select, update, delete, desc
from sqlalchemy.orm.attributes import flag_modified
from database.models import User, Targets, Roadmaps, async_session

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def set_targets(tg_id, title, description):
    async with async_session() as session:
        target = Targets(tg_id=tg_id,
                         title=title,
                         description=description,
                         status=False)
        session.add(target)
        await session.commit()

async def return_userlist(tg_id) -> list:
    async with async_session() as session:
        user = await session.scalars(select(Targets).where(Targets.tg_id == tg_id).order_by(Targets.id))
        user_list = list(user)
        return user_list
    
async def return_userlist_by_id(id): #Функция возвращает не лист а объект Target, переимёнывать её себе дороже
    async with async_session() as session:
        target = await session.scalar(select(Targets).where(Targets.id == id))
        return target
    
async def change_target_status(id): 
    async with async_session() as session:
        target = await session.scalar(select(Targets).where(Targets.id == id))
        if target.status:
            await session.execute(update(Targets).where(Targets.id == id).values(status = False))
        else:
            await session.execute(update(Targets).where(Targets.id == id).values(status = True))

        await session.commit()

async def delete_target_by_id(id):
    async with async_session() as session:
        target = await session.scalar(select(Targets).where(Targets.id == id))
        await session.delete(target)
        await session.commit()

async def set_roadmap(tg_id, title):
    async with async_session() as session:
        roadmap = Roadmaps(tg_id = tg_id,
                           title = title,
                           point = [])
        session.add(roadmap)
        await session.commit()

async def return_roadmap_list(tg_id):
    async with async_session() as session:
        roadmap_list = await session.scalars(select(Roadmaps).where(Roadmaps.tg_id == tg_id).order_by(Roadmaps.id))
        return roadmap_list
    
async def show_roadmap(id):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        return roadmap
    
async def create_point(id, title):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        new_point = {
            "title": title,
            "status": False
        }
        roadmap.point.append(new_point)

        flag_modified(roadmap, "point")

        await session.commit()

async def delete_roadmap_by_id(id):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        await session.delete(roadmap)
        await session.commit()

async def get_point(id, index):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        point = roadmap.point[index]
        return point
    
async def change_point_status(id, index):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        roadmap.point[index]["status"] = not roadmap.point[index]["status"]
        flag_modified(roadmap, "point")
        session.add(roadmap)
        await session.commit()
    
async def delete_point(id, index):
    async with async_session() as session:
        roadmap = await session.scalar(select(Roadmaps).where(Roadmaps.id == id))
        del roadmap.point[index]
        flag_modified(roadmap, "point")
        await session.commit()