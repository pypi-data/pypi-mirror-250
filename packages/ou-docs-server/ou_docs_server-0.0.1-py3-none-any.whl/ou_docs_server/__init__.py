# SPDX-FileCopyrightText: 2024-present Mark Hall <mark.hall@work.room3b.eu>
#
# SPDX-License-Identifier: MIT
"""OU Docs Upload Server."""
import aiofiles
import asyncio
import os
import shutil

from fastapi import FastAPI, status, UploadFile, Depends, Header, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated


class Settings(BaseSettings):
    """Settings to validate the server configuration."""

    base_path: str
    auth_token: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
app = FastAPI()


def auth_token(authorization: str = Header("authorization")) -> str:
    """Return the auth token."""
    if authorization.startswith("Bearer "):
        if authorization[7:] == settings.auth_token:
            return authorization[7:]
    raise HTTPException(403)


@app.put("/upload/{module}/{presentation}", status_code=status.HTTP_202_ACCEPTED)
async def upload(
    module: str, presentation: str, archive: UploadFile, auth_token: Annotated[str, Depends(auth_token)]
) -> None:
    """Upload the data to the module/presentation prefix."""
    asyncio.create_task(extract(os.path.join(module, presentation), await archive.read()))


@app.put("/upload/{module}/{presentation}/{part}", status_code=status.HTTP_202_ACCEPTED)
async def upload_with_parth(
    module: str, presentation: str, part: str, archive: UploadFile, auth_token: Annotated[str, Depends(auth_token)]
) -> None:
    """Upload the data to the module/presentation/path prefix."""
    asyncio.create_task(extract(os.path.join(module, presentation, part), await archive.read()))


async def extract(path: str, data: bytes) -> None:
    """Extract the uploaded archive data."""
    path = os.path.join(settings.base_path, path)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    with open(os.path.join(path, "__archive__.tar.bz2"), mode="wb") as out_f:
        out_f.write(data)
    proc = await asyncio.create_subprocess_exec(
        "tar", "-xjf", os.path.join(path, "__archive__.tar.bz2"), "--strip-components=1", "-C", path
    )
    await proc.wait()
