"""
Database module for AI Company institutional memory and runtime persistence.
"""

from ai_company.database.schema import init_db
from ai_company.database.repository import repo, CompanyRepository

__all__ = ["init_db", "repo", "CompanyRepository"]
