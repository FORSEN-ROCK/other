'''
    Save result in another database.
'''

def save_candidate(**kwargs):
    import os
    import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    connect_string = 'oracle+cx_oracle://%s:%s@%s' %(os.getenv(''),
                                                     os.getenv(''),
                                                     os.getenv(''))
    engine = create_engine(connect_string,
                           exclude_tablespaces=["DATA01", "SOME_TABLESPACE"])
    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)
    Candidate = candidate_maker(Base)
    session = Session()
    time = datetime.datetime.utcnow()
    row_id = 'HR-' + str(time.minute) + ':' + str(time.second)
    cand = Candidate(row_id=row_id,
                     created_by=kwargs.get('created_by', '0-1'),
                     last_upd_by=kwargs.get('last_upd_by', '0-1'),
                     education=kwargs.get('education', ''),
                     email=kwargs.get('email', ''),
                     experience=kwargs.get('experience', ''),
                     first_name=kwargs.get('first_name', ''),
                     gender=kwargs.get('gender', ''),
                     job_vacancy=kwargs.get('job_vacancy', ''),
                     last_name=kwargs.get('last_name', ''),
                     mid_name=kwargs.get('mid_name', ''),
                     phone=kwargs.get('phone', ''),
                     region=kwargs.get('region' ,''),
                     source=kwargs.get('source', ''),
                     auto_flg=kwargs.get('auto_flg', 'N'))
    session.add(cand)
    session.commit()
    session.close_all()
    return True

def candidate_maker(cls):
    import datetime
    from sqlalchemy import Column, Integer, String, Date, Char

    class Candidate(cls):
        __tablename__ = 'CX_CANDIDATE'
        __table_args__ = {
                         'schema': 'SIEBEL',##
                         'extend_existing': True,
                         'implicit_returning': False,
                         }
        row_id = Column(String(15), primary_key=True)
        created = Column(Date)
        created_by = Column(String(15))
        last_upd = Column(Date)
        last_upd_by =  Column(String(15))
        modification_num = Column(Integer(10))
        conflict_id = Column(String(15))
        db_last_upd = Column(Date)
        db_last_upd_src = Column(String(50))
        education = Column(String(50))
        email = Column(String(50))
        experience = Column(String(50))
        first_name = Column(String(50))
        gender = Column(String(10))
        job_vacancy = Column(String(50))
        last_name = Column(String(50))
        mid_name = Column(String(50))
        phone = Column(String(50))
        position = Column(String(50))
        region = Column(String(50))
        skype = Column(String(50))
        source = Column(String(50))
        status_cd = Column(String(50)) 
        auto_flg = Column(Char(1))
        communication = Column(Integer(10))
        computer_text = Column(String(250))
        experience_text = Column(String(250))
        interest_text = Column(String(250))
        internet_flg = Column(Char(1))
        making_decis = Column(Integer(10))
        recomended1 = Column(Char(1))
        recomended2 = Column(Char(1))
        recomended3 = Column(Char(1))
        result = Column(String(250))
        result_orient = Column(Integer(10))
        stress_block = Column(Integer(10))
        want_work = Column(Integer(10))

        def __init__(self, **kwargs):
            self.row_id = kwargs.get('row_id')
            self.created = datetime.datetime.utcnow()
            self.created_by = kwargs.get('created_by', '0-1')
            self.last_upd = datetime.datetime.utcnow()
            self.last_upd_by = kwargs.get('last_upd_by', '0-1')
            self.modification_num = kwargs.get('modification_num', '0')
            self.conflict_id = kwargs.get('conflict_id', '0')
            self.db_last_upd = datetime.datetime.utcnow()
            self.db_last_upd_src = kwargs.get('db_last_upd_src', '')
            self.education = kwargs.get('education')
            self.email = kwargs.get('email')
            self.experience = kwargs.get('experience')
            self.first_name = kwargs.get('first_name')
            self.gender = kwargs.get('gender')
            self.job_vacancy = kwargs.get('job_vacancy')
            self.last_name = kwargs.get('last_name')
            self.mid_name = kwargs.get('mid_name')
            self.phone = kwargs.get('phone')
            self.position = kwargs.get('position', '')
            self.region = kwargs.get('region')
            self.skype = kwargs.get('skype', '')
            self.source = kwargs.get('source')
            self.status_cd = kwargs.get('status_cd', '')
            self.auto_flg = kwargs.get('auto_flg')
            self.communication = kwargs.get('communication', '')
            self.computer_text = kwargs.get('computer_text', '')
            self.experience_text = kwargs.get('experience_text', '')
            self.interest_text = kwargs.get('interest_text', '')
            self.internet_flg = kwargs.get('internet_flg', 'N')
            self.making_decis = kwargs.get('making_decis', '')
            self.recomended1 = kwargs.get('recomended1', 'N')
            self.recomended2 = kwargs.get('recomended2', 'N')
            self.recomended3 = kwargs.get('recomended3', 'N')
            self.result = kwargs.get('result', '')
            self.result_orient = kwargs.get('result_orient', '')
            self.stress_block = kwargs.get('stress_block', '')
            self.want_work = kwargs.get('want_work', '')

    return Candidate