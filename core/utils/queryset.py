from sqlalchemy.orm import sessionmaker
from models.db import Schedling,Calcs,Dependent

def get_calc_details_from_db(engine,scheduling_group,calc_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    group = session.query(Schedling).filter_by(schedling_group=scheduling_group).first()
    print(group)
    session.commit()

