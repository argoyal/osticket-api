from utils.base_forms import Field, BaseForm
from services import OrganizationService, UserService

org_service = OrganizationService()
user_service = UserService()


class OrganizationForm(BaseForm):

    name = Field({"type": str, "required": True})
    manager = Field({"type": int, "required": False})
    status = Field({"type": int, "required": False})
    domain = Field({"type": str, "required": False})
    address = Field({"type": str, "required": False})
    phone = Field({"type": str, "required": False})
    website = Field({"type": str, "required": False})
    notes = Field({"type": str, "required": False})

    def save(self, validated_data):
        return org_service.add_organization(**validated_data)


class UserForm(BaseForm):

    email = Field({"type": str, "required": True})
    name = Field({"type": str, "required": True})
    password = Field({"type": str, "required": True})
    org_id = Field({"type": int, "required": True})
    phone = Field({"type": str, "required": False})
    username = Field({"type": str, "required": False})

    def save(self, validated_data):
        return user_service.add_user(**validated_data)
