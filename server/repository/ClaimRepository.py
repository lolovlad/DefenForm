from sqlalchemy.orm import Session
from ..database import ServiceSelection, Priority, Status, Claim, Contract

from uuid import uuid4


class ClaimRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_claim_by_user(self, id_user: int) -> list[Claim]:
        return self.__session.query(Claim).where(Claim.id_user == id_user).all()

    def get_claim_by_worker(self, id_user: int) -> list[Claim]:
        return self.__session.query(Claim).where(Claim.id_worker == id_user).all()

    def get_claim_by_uuid(self, uuid_claim: str) -> Claim:
        return self.__session.query(Claim).where(Claim.trace_id == uuid_claim).first()

    def get_all_service_selection(self) -> list[ServiceSelection]:
        return self.__session.query(ServiceSelection).all()

    def get_state_claim_bu_name(self, name: str) -> Status:
        return self.__session.query(Status).where(Status.name == name).first()

    def get(self, id_claim: int) -> Claim:
        return self.__session.get(Claim, id_claim)

    def get_contract_by_id_claim(self, id_claim: int) -> Contract:
        return self.__session.query(Contract).where(Contract.id_claim == id_claim).first()

    def get_status_all(self) -> list[Status]:
        return self.__session.query(Status).all()

    def get_priority_all(self) -> list[Priority]:
        return self.__session.query(Priority).all()

    def edit(self, entity: Claim) -> Claim | None:
        try:
            self.__session.add(entity)
            self.__session.commit()
            return entity
        except:
            self.__session.rollback()
            return None

    def get_claim_work_search(self, id_worker: int, trace: str, id_status: int, id_priority: int) -> list[Claim]:
        q = self.__session.query(Claim).where(Claim.id_worker == id_worker).join(Priority)
        if trace:
            q = q.where(Claim.trace_id.ilike(f"%{trace}%"))
        if id_status != -1:
            q = q.where(Claim.id_status == id_status)
        if id_priority != -1:
            q = q.where(Claim.id_priority == id_priority)
        return q.order_by(Claim.id_status.asc(), Priority.coast.desc()).all()