from fastapi import APIRouter
from gcp_service import GCPService

router = APIRouter()


@router.get("/getSupportedLanguages")
async def get_supported_languages():
    return GCPService.get_supported_languages()


@router.get("/detectLanguage")
async def detect_language(text: str):
    return GCPService.detect_language(text)
