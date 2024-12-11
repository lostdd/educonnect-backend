import asyncio

from app.auth.dao import RoleDAO
import app.projects.dao
from app.auth.pydantic_models import RoleModel, RoleEnum
from app.dao import database
from app.dao.session import session_manager

async def init_db():
    db_session = session_manager.session_maker()
    await database.init_db()
    c = 1
    for role in RoleEnum:
        await RoleDAO.add(db_session, RoleModel(id=c, name=role.name))
        c += 1
    await db_session.commit()

asyncio.run(init_db())