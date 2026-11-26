"""Vùng định nghĩa 13 bảng Core của Dev Fullstack (triển khai chi tiết tại US-02).

Lưu ý Zero File-Overlap:
- File này chỉ chứa các model nghiệp vụ cốt lõi (users, categories, dishes,
  areas, tables, reservations, reservation_items, deposit_transactions, ...).
- 3 bảng AI (knowledge_docs, chat_sessions, chat_messages) thuộc `ai_models.py`
  do AI Dev phụ trách độc lập.
"""

from app.core.database import Base

__all__ = ["Base"]
