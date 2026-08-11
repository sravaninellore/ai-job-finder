from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.file_storage import file_storage_service
from app.services.text_extractor import text_extractor_service
from app.services.resume_parser import resume_parser_service
from app.models.resume import Resume
from app.models.candidate import CandidateProfile
from app.schemas.resume import ResumeUploadResponse, ResumeResponse

router = APIRouter()

@router.post("/upload", response_model=ResumeUploadResponse)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload PDF or DOCX resume, extract text, run LLM candidate parser, and save to DB."""
    # 1. Save file to disk
    file_path, file_type, file_size = file_storage_service.save_file(file)

    try:
        # 2. Extract raw text from file
        raw_text = text_extractor_service.extract_text(file_path, file_type)

        # 3. Parse resume with LLM (or fallback heuristic parser)
        candidate_profile_schema = resume_parser_service.parse_resume(raw_text)

        # 4. Store Resume in Database
        db_resume = Resume(
            filename=file.filename or "resume",
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            raw_text=raw_text
        )
        db.add(db_resume)
        db.flush()

        # 5. Store CandidateProfile in Database
        db_profile = CandidateProfile(
            resume_id=db_resume.id,
            profile_data=candidate_profile_schema.model_dump()
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_resume)

        return ResumeUploadResponse(
            id=db_resume.id,
            filename=db_resume.filename,
            file_type=db_resume.file_type,
            file_size=db_resume.file_size,
            uploaded_at=db_resume.uploaded_at,
            candidate_profile=candidate_profile_schema
        )

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return resume
