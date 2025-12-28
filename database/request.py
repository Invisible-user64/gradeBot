from sqlalchemy import select, update, delete, desc

from database.models import User, Targets, async_session

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
    
async def change_target_status(id): #Функция возвращает не лист а объект Target, переимёнывать её себе дороже
    async with async_session() as session:
        target = await session.scalar(select(Targets).where(Targets.id == id))
        if target.status:
            await session.execute(update(Targets).where(Targets.id == id).values(status = False))
        else:
            await session.execute(update(Targets).where(Targets.id == id).values(status = True))

        await session.commit()

