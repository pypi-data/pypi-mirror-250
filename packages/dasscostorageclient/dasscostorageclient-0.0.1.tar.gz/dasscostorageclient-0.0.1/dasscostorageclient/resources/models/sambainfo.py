import pydantic


class SambaInfoModel(pydantic.BaseModel):
    port: int | None
    hostname: str | None
    smb_name: str | None
    token: str | None
    samba_request_status: str | None = pydantic.Field(alias='sambaRequestStatus')
    samba_request_status_message: str | None = pydantic.Field(alias='sambaRequestStatusMessage')
