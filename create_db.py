from app.utils.database import Base, engine
Base.metadata.create_all(bind=engine)