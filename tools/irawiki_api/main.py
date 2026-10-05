from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import sys
import datetime
import uuid
import os
import hmac
import json
import re
import yaml

sys.path.insert(0, "/home/ubuntu/irawiki_api")
import wiki_query  # lapisan baca wiki_index.db (Fase 3)

app = FastAPI(title="Irawiki Knowledge API")

# ============================================================
# API KEY AUTH FOR MUSE.AI CONNECTOR
# ============================================================

MUSE_API_KEY = os.environ.get("IRAWIKI_MUSE_API_KEY", "")

def verify_muse_key(authorization: str = Header(None), x_api_key: str = Header(None)):
    """Verify API key for Muse.ai connector endpoints.
    
    Accepts either:
    - Authorization: Bearer <key>
    - X-API-Key: <key>
    
    Raises 401 if key is missing or invalid.
    """
    if not MUSE_API_KEY:
        # No key configured — deny all POST requests
        raise HTTPException(status_code=401, detail="unauthorized")
    
    provided = None
    if authorization and authorization.startswith("Bearer "):
        provided = authorization[7:]
    elif x_api_key:
        provided = x_api_key
    
    if not provided or not hmac.compare_digest(provided, MUSE_API_KEY):
        raise HTTPException(status_code=401, detail="unauthorized")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    """Custom exception handler to return consistent error format."""
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": "unauthorized"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

CONTENT_ROOT = Path("/home/ubuntu/irawiki/content")
PROPOSALS_ROOT = Path("/home/ubuntu/irawiki/proposals")
PROPOSALS_ROOT.mkdir(parents=True, exist_ok=True)

# ============================================================
# TEMPLATE CONFIGURATION
# ============================================================

TEMPLATES_DIR = Path("/home/ubuntu/irawiki/templates")

# Map entity_type to template file and required frontmatter fields
TEMPLATE_CONFIG = {
    "aktor": {
        "template_file": "01_aktor_master_template.md",
        "required_fields": ["nama_lengkap"],
        "content_dir": "aktor"
    },
    "peristiwa": {
        "template_file": "02_peristiwa_template.md",
        "required_fields": ["tanggal"],
        "content_dir": "peristiwa"
    },
    "analisis": {
        "template_file": "03_analysis_template.md",
        "required_fields": ["aktor_fokus", "peristiwa"],
        "content_dir": "analisis"
    }
}

def _parse_frontmatter(md_text: str) -> dict:
    """Parse YAML frontmatter from markdown text using PyYAML safe_load."""
    if not md_text.startswith("---"):
        return {}
    
    end_match = re.search(r'^---\s*$', md_text[3:], re.MULTILINE)
    if not end_match:
        return {}
    
    fm_text = md_text[3:3 + end_match.start()]
    try:
        result = yaml.safe_load(fm_text)
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}

def _validate_frontmatter(entity_type: str, md_text: str) -> list:
    """Validate required frontmatter fields. Returns list of missing fields."""
    if entity_type not in TEMPLATE_CONFIG:
        return []
    
    required = TEMPLATE_CONFIG[entity_type]["required_fields"]
    fm = _parse_frontmatter(md_text)
    
    missing = []
    for field in required:
        if field not in fm or fm[field] is None:
            missing.append(field)
        elif isinstance(fm[field], str) and not fm[field].strip():
            missing.append(field)
        elif isinstance(fm[field], list):
            # For list fields: each item must be a non-empty string
            if not fm[field] or not all(isinstance(item, str) and item.strip() for item in fm[field]):
                missing.append(field)
    
    return missing

# ============================================================
# EXISTING ENDPOINTS (PRESERVED)
# ============================================================

class ProposalRequest(BaseModel):
    entity_id: str
    entity_type: str
    proposed_markdown: str
    reason: str

def _load_markdown(subdir: str, identifier: str) -> str:
    file_path = CONTENT_ROOT / subdir / f"{identifier}.md"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"{subdir[:-1].capitalize()} '{identifier}' not found")
    return file_path.read_text(encoding="utf-8")

@app.get("/actors/{actor_id}")
async def get_actor(actor_id: str):
    return {"id": actor_id, "markdown": _load_markdown("aktor", actor_id)}

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    return {"id": event_id, "markdown": _load_markdown("peristiwa", event_id)}

@app.get("/search")
async def search(q: str, limit: int = 10, tipe: str = ""):
    """FTS5 BM25 berbobot (title x3, section x2, body x1) + ekspansi alias.

    `tipe` menerima nilai pages.type (individu|organisasi|peristiwa|analisis)
    atau nama folder konten (aktor|peristiwa|analisis). Kosong = semua.
    """
    if not wiki_query.available():
        raise HTTPException(status_code=503, detail="wiki_index.db belum tersedia")
    res = wiki_query.search(q, tipe=(tipe or None), limit=limit)
    # bentuk lama dipertahankan (type/id/snippet) + field baru
    results = [{
        "type": r["type"],
        "id": r["page_path"].split("/")[-1],
        "page_path": r["page_path"],
        "title": r["title"],
        "section": r["section"],
        "snippet": r["snippet"],
        "score": r["score"],
    } for r in res["results"]]
    out = {"query": q, "limit": limit, "results": results, "count": len(results)}
    if res.get("alias_expanded_to"):
        out["alias_expanded_to"] = res["alias_expanded_to"]
    return out

@app.post("/proposals")
async def create_proposal(proposal: ProposalRequest):
    """Submit an update proposal for human review."""
    proposal_id = str(uuid.uuid4())[:8]
    now = datetime.datetime.now().isoformat()
    
    # Save the proposed markdown
    md_filename = f"{proposal.entity_id}_{proposal_id}.md"
    md_path = PROPOSALS_ROOT / md_filename
    md_path.write_text(proposal.proposed_markdown, encoding="utf-8")
    
    # Save metadata
    meta_filename = f"{proposal.entity_id}_{proposal_id}.meta.json"
    meta_path = PROPOSALS_ROOT / meta_filename
    meta_content = {
        "id": proposal_id,
        "entity_id": proposal.entity_id,
        "entity_type": proposal.entity_type,
        "reason": proposal.reason,
        "status": "PENDING",
        "created_at": now
    }
    meta_path.write_text(json.dumps(meta_content, indent=2), encoding="utf-8")
    
    return {"status": "success", "proposal_id": proposal_id, "message": "Proposal submitted for review."}

# ============================================================
# MUSE.AI CUSTOM CONNECTOR ENDPOINTS
# ============================================================

def _is_stub(md_text: str) -> bool:
    """Heuristic: a stub is a very short markdown with minimal sections."""
    lines = [l for l in md_text.strip().split("\n") if l.strip()]
    # Remove frontmatter
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i+1:]
                break
    # Count meaningful content lines (non-empty, non-header)
    content_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]
    return len(content_lines) < 5

def _get_stub_candidates(subdir: str, limit: int = 50) -> list:
    """Find stub pages in a subdirectory."""
    base = CONTENT_ROOT / subdir
    if not base.exists():
        return []
    stubs = []
    for md_file in sorted(base.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        if _is_stub(text):
            stubs.append({
                "id": md_file.stem,
                "type": subdir[:-1],  # "aktor" -> "actor"
                "size_bytes": len(text),
                "preview": text[:300].replace("\n", " ") + "..."
            })
            if len(stubs) >= limit:
                break
    return stubs

@app.get("/muse/stubs")
async def muse_get_stubs(entity_type: str = "", limit: int = 50):
    """List stub pages that need enrichment.
    
    Query params:
    - entity_type: filter by 'aktor', 'peristiwa', or 'analisis' (empty = all)
    - limit: max results (default 50)
    """
    valid_types = ("aktor", "peristiwa", "analisis")
    if entity_type:
        if entity_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"entity_type must be one of {valid_types}")
        stubs = _get_stub_candidates(entity_type, limit)
        return {"total": len(stubs), "entity_type": entity_type, "stubs": stubs}
    
    all_stubs = []
    for subdir in valid_types:
        all_stubs.extend(_get_stub_candidates(subdir, limit))
    return {"total": len(all_stubs), "entity_type": "all", "stubs": all_stubs}

@app.get("/muse/stub/{entity_type}/{entity_id}")
async def muse_get_stub_detail(entity_type: str, entity_id: str):
    """Get a single stub page with its template for enrichment.
    
    Returns the current markdown + the appropriate template so Muse
    knows what structure to fill in.
    """
    if entity_type not in TEMPLATE_CONFIG:
        raise HTTPException(status_code=400, detail=f"entity_type must be one of {list(TEMPLATE_CONFIG.keys())}")
    
    file_path = CONTENT_ROOT / entity_type / f"{entity_id}.md"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"{entity_type} '{entity_id}' not found")
    
    current_md = file_path.read_text(encoding="utf-8")
    
    # Get the appropriate template
    template_file = TEMPLATE_CONFIG[entity_type]["template_file"]
    template_path = TEMPLATES_DIR / template_file
    template = template_path.read_text(encoding="utf-8") if template_path.exists() else ""
    
    # Get related entities for context (search by name in content)
    related = []
    name_parts = entity_id.replace("-", " ").split()
    for subdir in ("aktor", "peristiwa"):
        base = CONTENT_ROOT / subdir
        if not base.exists():
            continue
        for md_file in base.glob("*.md"):
            if md_file.stem == entity_id:
                continue
            text = md_file.read_text(encoding="utf-8")
            if any(part in text for part in name_parts if len(part) > 3):
                related.append({
                    "type": subdir[:-1],
                    "id": md_file.stem,
                    "snippet": text[:150].replace("\n", " ") + "..."
                })
            if len(related) >= 5:
                break
        if len(related) >= 5:
            break
    
    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "is_stub": _is_stub(current_md),
        "current_markdown": current_md,
        "template": template,
        "related_entities": related
    }

@app.get("/muse/templates/{entity_type}")
async def muse_get_template(entity_type: str):
    """Get the master template for a given entity_type.
    
    Returns the verbatim template content so Muse always follows
    the latest template version without needing to read from Drive.
    """
    if entity_type not in TEMPLATE_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"entity_type must be one of {list(TEMPLATE_CONFIG.keys())}"
        )
    
    template_file = TEMPLATE_CONFIG[entity_type]["template_file"]
    template_path = TEMPLATES_DIR / template_file
    
    if not template_path.exists():
        raise HTTPException(status_code=404, detail=f"Template file not found: {template_file}")
    
    content = template_path.read_text(encoding="utf-8")
    
    return {
        "entity_type": entity_type,
        "template_file": template_file,
        "content": content
    }

class MuseProposeRequest(BaseModel):
    entity_id: str
    entity_type: str  # "aktor", "peristiwa", or "analisis"
    proposed_markdown: str
    reason: str
    source: str = "muse_ai"  # track who submitted

@app.post("/muse/propose")
async def muse_propose(request: MuseProposeRequest, auth: str = Depends(verify_muse_key)):
    """Submit an enrichment proposal OR new page proposal from Muse.ai for human review.
    
    This endpoint supports two modes:
    1. ENRICHMENT: entity_id already exists in content -> update existing page
    2. NEW PAGE: entity_id does NOT exist -> create new page (requires valid frontmatter)
    
    The proposal is saved to proposals/ and must be reviewed by a human
    before being merged into the actual content.
    """
    # Validate entity_type
    if request.entity_type not in TEMPLATE_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"entity_type must be one of {list(TEMPLATE_CONFIG.keys())}"
        )
    
    content_dir = TEMPLATE_CONFIG[request.entity_type]["content_dir"]
    file_path = CONTENT_ROOT / content_dir / f"{request.entity_id}.md"
    is_new_page = not file_path.is_file()
    
    # Check for duplicate PENDING proposal (both new page and enrichment)
    for meta_file in PROPOSALS_ROOT.glob(f"{request.entity_id}_*.meta.json"):
        try:
            existing = json.loads(meta_file.read_text(encoding="utf-8"))
            if existing.get("entity_type") == request.entity_type and existing.get("status") == "PENDING":
                raise HTTPException(
                    status_code=409,
                    detail=f"sudah ada proposal PENDING untuk entity_id '{request.entity_id}'"
                )
        except json.JSONDecodeError:
            continue
    
    # For new pages: validate frontmatter
    if is_new_page:
        missing_fields = _validate_frontmatter(request.entity_type, request.proposed_markdown)
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required frontmatter fields for {request.entity_type}: {', '.join(missing_fields)}"
            )
    
    proposal_id = str(uuid.uuid4())[:8]
    now = datetime.datetime.now().isoformat()
    
    # Save the proposed markdown
    md_filename = f"{request.entity_id}_{proposal_id}.md"
    md_path = PROPOSALS_ROOT / md_filename
    md_path.write_text(request.proposed_markdown, encoding="utf-8")
    
    # Save metadata
    meta_filename = f"{request.entity_id}_{proposal_id}.meta.json"
    meta_path = PROPOSALS_ROOT / meta_filename
    meta_content = {
        "id": proposal_id,
        "entity_id": request.entity_id,
        "entity_type": request.entity_type,
        "reason": request.reason,
        "source": request.source,
        "is_new_page": is_new_page,
        "status": "PENDING",
        "created_at": now
    }
    meta_path.write_text(json.dumps(meta_content, indent=2), encoding="utf-8")
    
    message = "New page proposal submitted for human review." if is_new_page else "Enrichment proposal submitted for human review."
    
    return {
        "status": "success",
        "proposal_id": proposal_id,
        "message": message,
        "entity_id": request.entity_id,
        "entity_type": request.entity_type,
        "is_new_page": is_new_page
    }

@app.get("/muse/proposals")
async def muse_list_proposals(status: str = "PENDING"):
    """List all proposals (for review dashboard)."""
    proposals = []
    for meta_file in sorted(PROPOSALS_ROOT.glob("*.meta.json")):
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            if status and data.get("status") != status:
                continue
            proposals.append(data)
        except:
            continue
    return {"total": len(proposals), "proposals": proposals}

@app.post("/muse/proposals/{proposal_id}/approve")
async def muse_approve_proposal(proposal_id: str, auth: str = Depends(verify_muse_key)):
    """Approve a proposal and merge into content."""
    # Find the proposal files
    md_files = list(PROPOSALS_ROOT.glob(f"*_{proposal_id}.md"))
    meta_files = list(PROPOSALS_ROOT.glob(f"*_{proposal_id}.meta.json"))
    
    if not md_files or not meta_files:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    
    md_path = md_files[0]
    meta_path = meta_files[0]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    
    entity_id = meta["entity_id"]
    entity_type = meta["entity_type"]
    is_new_page = meta.get("is_new_page", False)
    
    # Get content directory
    if entity_type in TEMPLATE_CONFIG:
        content_dir = TEMPLATE_CONFIG[entity_type]["content_dir"]
    else:
        # Fallback for legacy proposals
        content_dir = "aktor" if entity_type == "aktor" else "peristiwa"
    
    # Backup original (if exists)
    original_path = CONTENT_ROOT / content_dir / f"{entity_id}.md"
    backup_path = CONTENT_ROOT / content_dir / f"{entity_id}.md.bak"
    if original_path.exists():
        backup_path.write_text(original_path.read_text(encoding="utf-8"), encoding="utf-8")
    
    # Merge proposal into content
    proposed_md = md_path.read_text(encoding="utf-8")
    
    # Ensure directory exists
    original_path.parent.mkdir(parents=True, exist_ok=True)
    original_path.write_text(proposed_md, encoding="utf-8")
    
    # Update metadata
    meta["status"] = "APPROVED"
    meta["approved_at"] = datetime.datetime.now().isoformat()
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    
    action = "created" if is_new_page else "merged"
    
    return {
        "status": "approved",
        "proposal_id": proposal_id,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "is_new_page": is_new_page,
        "message": f"Proposal {action} in {content_dir}/{entity_id}.md"
    }

@app.post("/muse/proposals/{proposal_id}/reject")
async def muse_reject_proposal(proposal_id: str, auth: str = Depends(verify_muse_key)):
    """Reject a proposal."""
    meta_files = list(PROPOSALS_ROOT.glob(f"*_{proposal_id}.meta.json"))
    if not meta_files:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    
    meta_path = meta_files[0]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["status"] = "REJECTED"
    meta["rejected_at"] = datetime.datetime.now().isoformat()
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    
    return {"status": "rejected", "proposal_id": proposal_id}
