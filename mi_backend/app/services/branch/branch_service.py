from ...models.branch.branch import Branch
from ...services.log.log_service import LogService


class BranchService:

    @staticmethod
    def get_all_branches():

        branches = Branch.query.filter(Branch.deleted_at.is_(None)).all()

        return [branch.to_dict() for branch in branches]

    @staticmethod
    def get_branch_by_id(id_branch):

        branch = Branch.query.filter(
            Branch.deleted_at.is_(None), Branch.id == id_branch
        ).first()

        if branch is None:
            LogService.create_log(
                {
                    "module": f"{BranchService.__name__}.{BranchService.get_branch_by_id.__name__}",
                    "message": "No se encontró la sede buscada por id",
                }
            )
            raise ValueError("No se encontró la sede")

        return branch.to_dict()
