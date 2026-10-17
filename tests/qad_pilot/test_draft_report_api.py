"""Draft reports stay unpublished and are still readable through the report API."""
import os

os.environ.setdefault("IIP_AUTH_USER", "founder")
os.environ.setdefault("IIP_AUTH_PASSWORD", "test-password-123")
os.environ.setdefault("IIP_AUTH_SECRET", "y" * 40)

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

SLUG = "unh-qad-pilot-2026-10-17"
client = TestClient(app)


def _login() -> None:
    response = client.post(
        "/api/auth/login",
        json={"username": "founder", "password": "test-password-123"},
    )
    assert response.status_code == 200, response.text


def test_draft_is_hidden_from_the_published_filter_and_readable_by_slug():
    _login()
    listed = client.get("/api/reports")
    assert listed.status_code == 200
    reports = listed.json()["reports"]
    draft = next(r for r in reports if r["slug"] == SLUG)
    assert draft["status"] == "draft"
    assert draft["subject"] == "UNH"

    published = client.get("/api/reports", params={"status": "published"})
    assert published.status_code == 200
    assert all(r["status"] == "published" for r in published.json()["reports"])
    assert SLUG not in {r["slug"] for r in published.json()["reports"]}

    only_drafts = client.get("/api/reports", params={"status": "draft"})
    assert only_drafts.status_code == 200
    drafts = only_drafts.json()["reports"]
    assert drafts
    assert all(r["status"] == "draft" for r in drafts)
    assert SLUG in {r["slug"] for r in drafts}

    article = client.get(f"/api/reports/{SLUG}")
    assert article.status_code == 200
    body = article.json()["report"]
    assert body["status"] == "draft"
    assert "## Independent Skeptic" in body["content"]
    assert "Independent Skeptic — pending" not in body["content"]
    assert "วิทยานิพนธ์ฝั่งเสื่อมโครงสร้าง" in body["content"]
    assert "ไม่ใช่คำแนะนำการลงทุน" in body["content"]
    assert body["content"].count("ราคาเป้าหมาย") >= 1
