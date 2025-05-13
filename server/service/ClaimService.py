from ..repository import ClaimRepository
from ..database import db, Claim, ServiceSelection, Contract, Status, Priority
from ..forms import AddClaimForm


class ClaimService:
    def __init__(self):
        self.__repository: ClaimRepository = ClaimRepository(db.session)

    def get_claim_by_user(self, id_user: int) -> list[Claim]:
        return self.__repository.get_claim_by_user(id_user)

    def get_claim_by_uuid(self, uuid_claim: str) -> Claim:
        return self.__repository.get_claim_by_uuid(uuid_claim)

    def get_all_service_selection(self) -> list[ServiceSelection]:
        return self.__repository.get_all_service_selection()

    def get_contract_by_id_claim(self, id_claim: int) -> Contract:
        return self.__repository.get_contract_by_id_claim(id_claim)

    def get_claim_by_worker(self, id_worker: int) -> list[Claim]:
        return self.__repository.get_claim_by_worker(id_worker)

    def add_claim(self, form: AddClaimForm, id_user: int, ):
        claim = Claim(
            datetime_claim=form.datetime_claim.data,
            address=form.address.data,
            description=form.description.data,
            id_user=id_user,
            id_service_selection=form.id_service_selection.data,
            id_priority=2,
            id_status=1
        )
        self.__repository.edit(claim)

    def change_status(self, uuid: str):
        claim = self.__repository.get_claim_by_uuid(uuid)
        if not claim:
            return False

        status = self.__repository.get_state_claim_bu_name("Закрыта")
        claim.id_status = status.id
        self.__repository.edit(claim)
        return True

    def get_status_all(self) -> list[Status]:
        return self.__repository.get_status_all()

    def get_priority_all(self) -> list[Priority]:
        return self.__repository.get_priority_all()

    def get_claim_work_search(self, id_worker: int, trace: str, id_status: int, id_priority: int) -> list[Claim]:
        return self.__repository.get_claim_work_search(id_worker, trace, id_status, id_priority)

