from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Table, create_engine,Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

# Association table for many-to-many relationship
scheduling_calc_association = Table(
    'scheduling_group_calc',
    Base.metadata,
    Column('calc_id', String(10), ForeignKey('calculations.calc_id'), primary_key=True),
    Column('schedling_group_id', Integer, ForeignKey('scheduling_group.id'), primary_key=True)
)

class Status(Base):
    __tablename__ = "calc_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    calc_id: Mapped[str] = mapped_column(String(10), ForeignKey('calculations.calc_id'), nullable=False)
    status: Mapped[str] = mapped_column(String(30))
    job_id: Mapped[Optional[str]] = mapped_column(String(64))
    airflow_run_id: Mapped[str] = mapped_column(String(128))

class Dependent(Base):
    __tablename__ = "dependency_set"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    calc_id = mapped_column(String(10), ForeignKey('calculations.calc_id'), nullable=False)
    dependency_calc = mapped_column(String(10), ForeignKey('calculations.calc_id'), nullable=False)
    comment = mapped_column(String(128), nullable=True)

class Calcs(Base):
    __tablename__ = "calculations"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    calc_id: Mapped[str] = mapped_column(String(10), unique=True)
    query: Mapped[str] = mapped_column(String(400))
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    time_in_sec: Mapped[int] = mapped_column(Integer, nullable=True)

    dependencies = relationship(
        'Dependent',
        primaryjoin="Calcs.calc_id == Dependent.calc_id",
        backref='parent',
        lazy='joined'
    )

    scheduling_groups = relationship(
        'Schedling',
        secondary=scheduling_calc_association,
        back_populates='calcs'
    )

    def __repr__(self):
        return f"<Calc(calc_id={self.calc_id}, query={self.query})>"

class Schedling(Base):
    __tablename__ = 'scheduling_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedling_group = mapped_column(String(30), nullable=False, unique=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    comment = mapped_column(String(128), nullable=True)

    calcs = relationship(
        'Calcs',
        secondary=scheduling_calc_association,
        back_populates='scheduling_groups'
    )

    def __repr__(self):
        return f"<Schedling(id={self.id}, schedling_group={self.schedling_group})>"

# Database setup
engine = create_engine('postgresql://airflow:airflow@localhost/pipline_db')
Base.metadata.drop_all(engine) # TODO: REMOVE the dropping table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

########################################################################################################
#                          INSERTING DUMMY DATA                                                        #
########################################################################################################

# Create Calc instances
calc1 = Calcs(calc_id='SA001', query="select 'SA001';", sequence=1, time_in_sec=180)
calc2 = Calcs(calc_id='SA002', query="select 'SA002';", sequence=1, time_in_sec=45)
calc3 = Calcs(calc_id='SA003', query="select 'SA003';", sequence=1, time_in_sec=45)
calc4 = Calcs(calc_id='SA004', query="select 'SA004';", sequence=2, time_in_sec=50)
calc5 = Calcs(calc_id='SA005', query="select 'SA005';", sequence=2, time_in_sec=55)
calc6 = Calcs(calc_id='SA006', query="select 'SA006';", sequence=3, time_in_sec=60)



# set dependency among calcs

dep1 = Dependent(calc_id=calc3.calc_id,dependency_calc=calc1.calc_id)
dep2 = Dependent(calc_id=calc3.calc_id,dependency_calc=calc2.calc_id)
dep3 = Dependent(calc_id=calc4.calc_id,dependency_calc=calc2.calc_id)
dep4 = Dependent(calc_id=calc5.calc_id,dependency_calc=calc3.calc_id)
dep5 = Dependent(calc_id=calc5.calc_id,dependency_calc=calc4.calc_id)

# Create Scheduling Group instances
scheduling_group1 = Schedling(schedling_group='EDW', sequence=10)
scheduling_group2 = Schedling(schedling_group='INSTA', sequence=20)

# Establish relationships
scheduling_group1.calcs = [calc1, calc2, calc3,calc4, calc5, calc6]
scheduling_group2.calcs = [calc4, calc5, calc6]

# Add and commit all instances
session.add_all([calc1, calc2, calc3, calc4, calc5, calc6, scheduling_group1, scheduling_group2,dep1,dep2,dep3,dep4,dep5])
session.commit()
