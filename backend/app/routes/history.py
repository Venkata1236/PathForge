from fastapi import APIRouter
from app.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import Depends

router = APIRouter()

@router.get("/history")
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT session_id, learner_name, target_role,
                   total_weeks, course_count, created_at, path_data
            FROM learning_paths
            ORDER BY created_at DESC
            LIMIT 20
        """)
    )
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
