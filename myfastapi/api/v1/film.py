from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from myfastapi.services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str


@router.get('/', response_model=Film)
async def films(service: FilmService = Depends(get_film_service)) -> List[Film]:
    res = await service.get_all()
    return res


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, service: FilmService = Depends(get_film_service)) -> Film:
    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return Film(id=film.id, title=film.title)
