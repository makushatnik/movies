from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from myfastapi.services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str
    description: str


@router.get('/', response_model=Genre)
async def genres(service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    res = await service.get_all()
    return res


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')

    return Genre(**genre.__dict__)
