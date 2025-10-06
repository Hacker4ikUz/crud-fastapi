from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from . import models, schemas



async def create_user(db: AsyncSession, user: schemas.CreateUser):
    new_user = models.User(name=user.name, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, id: int):
    result = await db.execute(select(models.User).filter(models.User.id == id))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()


async def update_user(db: AsyncSession, id: int, name: str | None = None, password: str | None = None):
    values = {}
    if name:
        values["name"] = name
    if password:
        values["password"] = password
    
    if not values:
        return None
    
    stmt = (
        update(models.User)
        .where(models.User.id == id)
        .values(**values)
        .returning(models.User)
    )
    result = await db.execute(stmt)
    await db.commit()

    return result.scalar_one_or_none()


async def delete_user(db: AsyncSession, id: int):
    result = await db.execute(select(models.User).filter(models.User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    
    await db.delete(user)
    await db.commit()

    return user
    
    