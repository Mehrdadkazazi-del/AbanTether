import logging

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.controllers import user_controller, order_controller
from app.models.User import User
from app.security import authentication
from app.services.currency_service import load_currencies
from app.services.job.batch_job import BatchJob
from app.utils.database import SessionLocal
from app.utils.hash import Hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = FastAPI()
app.include_router(user_controller.router)
app.include_router(order_controller.router)
app.include_router(authentication.router)
batch_job = None
consumer_job = None


@app.on_event("startup")
async def startup_event():
    create_admin_user()
    load_currencies()
    logger.info("Currencies loaded successfully.")
    global batch_job
    global consumer_job
    db = SessionLocal()
    batch_job = BatchJob(db)
    batch_job.start()
    logger.info("Batch job scheduler started.")


@app.on_event("shutdown")
async def shutdown_event():
    if batch_job:
        batch_job.shutdown()
    if batch_job.db:
        batch_job.db.close()
    logger.info("Batch job scheduler and database session closed.")


def create_admin_user():
    db: Session = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.national_code == "0000000000").first()
        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="User",
                national_code="0000000000",
                password=Hash.bcrypt("admin123"),
            )
            db.add(admin_user)
            db.commit()
            logger.info("Admin user created successfully!")
        else:
            logger.info("Admin user already exists.")
    finally:
        db.close()
