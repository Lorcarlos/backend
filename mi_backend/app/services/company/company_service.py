from ...models.company import Company


class CompanyService:

    @staticmethod
    def get_all_companies():
        companies = Company.query.filter(Company.deleted_at.is_(None)).all()

        return [company.to_dict() for company in companies]

    @staticmethod
    def get_company_by_id(id_company):

        company = Company.query.filter(
            Company.deleted_at.is_(None), Company.id == id_company
        ).first()

        if company is None:
            raise ValueError("No se encontró la compañía")

        return company.to_dict()
