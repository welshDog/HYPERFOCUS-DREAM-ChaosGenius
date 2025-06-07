"""
🔍 BROSKI CREW ULTRA SEARCH ENGINE
Finding files instantly with AI-powered semantic search!
"""

import hashlib
import json
import mimetypes
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class BROskiUltraSearchEngine:
    """Ultra-powered search engine for instant file discovery"""

    def __init__(self):
        self.search_db = "🗄️ Databases/search_index.db"
        self.workspace_root = "/root/chaosgenius"
        self.index_cache = {}
        self.search_history = []
        self.init_search_system()

    def init_search_system(self):
        """Initialize the ultra search database"""
        os.makedirs("🗄️ Databases", exist_ok=True)

        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        # Create search index tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS file_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                file_name TEXT,
                file_type TEXT,
                file_size INTEGER,
                content_preview TEXT,
                keywords TEXT,
                last_modified TIMESTAMP,
                last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                search_score REAL DEFAULT 1.0
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_query TEXT,
                results_found INTEGER,
                search_time REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_satisfaction REAL DEFAULT 0.8
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_a TEXT,
                file_b TEXT,
                relationship_type TEXT,
                strength REAL DEFAULT 0.5,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

        print("🔍 Ultra Search Engine initialized!")

    def index_workspace(self, force_reindex: bool = False):
        """Index the entire workspace for lightning-fast search"""
        print("🔍 Indexing workspace for ultra-fast search...")

        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        indexed_count = 0

        for root, dirs, files in os.walk(self.workspace_root):
            # Skip certain directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["__pycache__", "node_modules"]
            ]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.workspace_root)

                # Check if already indexed
                if not force_reindex:
                    cursor.execute(
                        "SELECT last_indexed FROM file_index WHERE file_path = ?",
                        (relative_path,),
                    )
                    existing = cursor.fetchone()
                    if existing:
                        continue

                try:
                    # Get file info
                    stat = os.stat(file_path)
                    file_size = stat.st_size
                    file_type = self._get_file_type(file_path)

                    # Extract content preview and keywords
                    content_preview, keywords = self._extract_file_content(
                        file_path, file_type
                    )

                    # Insert or update index
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO file_index
                        (file_path, file_name, file_type, file_size, content_preview, keywords, last_modified)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            relative_path,
                            file,
                            file_type,
                            file_size,
                            content_preview,
                            json.dumps(keywords),
                            datetime.fromtimestamp(stat.st_mtime),
                        ),
                    )

                    indexed_count += 1

                except Exception as e:
                    print(f"⚠️ Could not index {relative_path}: {e}")

        conn.commit()
        conn.close()

        print(f"✅ Indexed {indexed_count} files for ultra-fast search!")
        return indexed_count

    def search(self, query: str, search_type: str = "smart") -> List[Dict]:
        """Ultra-smart search with multiple search strategies"""
        start_time = datetime.now()

        results = []

        if search_type == "smart" or search_type == "all":
            results.extend(self._semantic_search(query))
            results.extend(self._keyword_search(query))
            results.extend(self._fuzzy_search(query))
        elif search_type == "semantic":
            results = self._semantic_search(query)
        elif search_type == "keyword":
            results = self._keyword_search(query)
        elif search_type == "fuzzy":
            results = self._fuzzy_search(query)

        # Remove duplicates and rank results
        results = self._deduplicate_and_rank(results, query)

        # Record search performance
        search_time = (datetime.now() - start_time).total_seconds()
        self._record_search(query, len(results), search_time)

        return results[:20]  # Top 20 results

    def _semantic_search(self, query: str) -> List[Dict]:
        """Intelligent semantic search"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        # Search by content meaning
        query_words = query.lower().split()

        results = []
        cursor.execute("SELECT * FROM file_index")

        for row in cursor.fetchall():
            score = 0.0
            file_data = {
                "path": row[1],
                "name": row[2],
                "type": row[3],
                "size": row[4],
                "preview": row[5],
                "score": 0.0,
                "match_type": "semantic",
            }

            # Check content preview
            if row[5]:  # content_preview
                content_lower = row[5].lower()
                for word in query_words:
                    if word in content_lower:
                        score += 2.0
                    # Check for similar concepts
                    if self._semantic_similarity(word, content_lower):
                        score += 1.0

            # Check keywords
            if row[6]:  # keywords
                try:
                    keywords = json.loads(row[6])
                    for word in query_words:
                        if word in [k.lower() for k in keywords]:
                            score += 3.0
                except:
                    pass

            if score > 0:
                file_data["score"] = score
                results.append(file_data)

        conn.close()
        return results

    def _keyword_search(self, query: str) -> List[Dict]:
        """Fast keyword-based search"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        # SQL search with LIKE
        search_pattern = f"%{query}%"

        cursor.execute(
            """
            SELECT * FROM file_index
            WHERE file_name LIKE ? OR content_preview LIKE ? OR keywords LIKE ?
            ORDER BY search_score DESC
        """,
            (search_pattern, search_pattern, search_pattern),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "path": row[1],
                    "name": row[2],
                    "type": row[3],
                    "size": row[4],
                    "preview": row[5],
                    "score": row[9] + 1.0,  # Base score + keyword match
                    "match_type": "keyword",
                }
            )

        conn.close()
        return results

    def _fuzzy_search(self, query: str) -> List[Dict]:
        """Fuzzy search for approximate matches"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM file_index")

        results = []
        for row in cursor.fetchall():
            # Calculate fuzzy match score
            file_name = row[2].lower()
            query_lower = query.lower()

            # Simple fuzzy matching
            score = 0.0
            if query_lower in file_name:
                score = 3.0
            else:
                # Check for partial matches
                common_chars = set(query_lower) & set(file_name)
                if len(common_chars) > len(query_lower) * 0.5:
                    score = len(common_chars) / len(query_lower) * 2.0

            if score > 0.5:
                results.append(
                    {
                        "path": row[1],
                        "name": row[2],
                        "type": row[3],
                        "size": row[4],
                        "preview": row[5],
                        "score": score,
                        "match_type": "fuzzy",
                    }
                )

        conn.close()
        return results

    def _semantic_similarity(self, word: str, content: str) -> bool:
        """Check for semantic similarity (simple version)"""
        # Simple semantic matching - can be enhanced with AI
        synonyms = {
            "discord": ["bot", "server", "chat", "community"],
            "database": ["db", "data", "storage", "sqlite"],
            "config": ["configuration", "settings", "env", "setup"],
            "deploy": ["deployment", "launch", "production", "live"],
            "test": ["testing", "check", "validate", "verify"],
        }

        for synonym_group in synonyms.values():
            if word in synonym_group:
                return any(syn in content for syn in synonym_group)

        return False

    def _deduplicate_and_rank(self, results: List[Dict], query: str) -> List[Dict]:
        """Remove duplicates and rank results by relevance"""
        seen_paths = set()
        unique_results = []

        for result in results:
            if result["path"] not in seen_paths:
                seen_paths.add(result["path"])
                unique_results.append(result)

        # Sort by score (descending)
        unique_results.sort(key=lambda x: x["score"], reverse=True)

        return unique_results

    def _get_file_type(self, file_path: str) -> str:
        """Determine file type"""
        mime_type, _ = mimetypes.guess_type(file_path)

        if file_path.endswith(".py"):
            return "python"
        elif file_path.endswith(".js"):
            return "javascript"
        elif file_path.endswith(".html"):
            return "html"
        elif file_path.endswith(".md"):
            return "markdown"
        elif file_path.endswith(".json"):
            return "json"
        elif file_path.endswith(".db"):
            return "database"
        elif mime_type:
            return mime_type.split("/")[0]
        else:
            return "unknown"

    def _extract_file_content(
        self, file_path: str, file_type: str
    ) -> Tuple[str, List[str]]:
        """Extract searchable content and keywords from file"""
        try:
            if file_type in ["python", "javascript", "html", "markdown", "json"]:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()[:1000]  # First 1000 chars

                # Extract keywords based on file type
                keywords = self._extract_keywords(content, file_type)

                return content, keywords
            else:
                return "", []
        except Exception:
            return "", []

    def _extract_keywords(self, content: str, file_type: str) -> List[str]:
        """Extract relevant keywords from content"""
        keywords = []

        if file_type == "python":
            # Extract function and class names
            keywords.extend(re.findall(r"def (\w+)", content))
            keywords.extend(re.findall(r"class (\w+)", content))
            keywords.extend(re.findall(r"import (\w+)", content))

        elif file_type == "javascript":
            keywords.extend(re.findall(r"function (\w+)", content))
            keywords.extend(re.findall(r"const (\w+)", content))

        elif file_type == "html":
            keywords.extend(re.findall(r"<title>(.*?)</title>", content, re.IGNORECASE))
            keywords.extend(re.findall(r'id="(\w+)"', content))

        # Extract general keywords (capitalized words, technical terms)
        keywords.extend(re.findall(r"\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b", content))

        return list(set(keywords))  # Remove duplicates

    def _record_search(self, query: str, results_count: int, search_time: float):
        """Record search performance for analytics"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO search_history (search_query, results_found, search_time)
            VALUES (?, ?, ?)
        """,
            (query, results_count, search_time),
        )

        conn.commit()
        conn.close()

    def get_search_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        # Count indexed files
        cursor.execute("SELECT COUNT(*) FROM file_index")
        indexed_files = cursor.fetchone()[0]

        # Count searches performed
        cursor.execute("SELECT COUNT(*) FROM search_history")
        total_searches = cursor.fetchone()[0]

        # Average search time
        cursor.execute("SELECT AVG(search_time) FROM search_history")
        avg_search_time = cursor.fetchone()[0] or 0

        # Most common search terms
        cursor.execute(
            """
            SELECT search_query, COUNT(*) as frequency
            FROM search_history
            GROUP BY search_query
            ORDER BY frequency DESC
            LIMIT 5
        """
        )
        common_searches = cursor.fetchall()

        conn.close()

        return {
            "indexed_files": indexed_files,
            "total_searches": total_searches,
            "avg_search_time": round(avg_search_time, 3),
            "common_searches": [
                {"query": q[0], "frequency": q[1]} for q in common_searches
            ],
        }

    def smart_suggestions(self, partial_query: str) -> List[str]:
        """Generate smart search suggestions"""
        conn = sqlite3.connect(self.search_db)
        cursor = conn.cursor()

        # Get suggestions from file names
        cursor.execute(
            """
            SELECT DISTINCT file_name FROM file_index
            WHERE file_name LIKE ?
            LIMIT 10
        """,
            (f"%{partial_query}%",),
        )

        suggestions = [row[0] for row in cursor.fetchall()]

        # Add suggestions from search history
        cursor.execute(
            """
            SELECT DISTINCT search_query FROM search_history
            WHERE search_query LIKE ?
            LIMIT 5
        """,
            (f"%{partial_query}%",),
        )

        suggestions.extend([row[0] for row in cursor.fetchall()])

        conn.close()
        return list(set(suggestions))[:10]


# Create global search engine instance
ultra_search = BROskiUltraSearchEngine()


class SearchInterface:
    """User-friendly search interface"""

    def __init__(self):
        self.search_engine = ultra_search

    def find(self, query: str, search_type: str = "smart") -> Dict[str, Any]:
        """Main search interface"""
        print(f"🔍 Searching for: '{query}' using {search_type} search...")

        results = self.search_engine.search(query, search_type)

        search_result = {
            "query": query,
            "results_count": len(results),
            "results": results,
            "search_type": search_type,
            "suggestions": (
                self.search_engine.smart_suggestions(query[:5])
                if len(query) >= 2
                else []
            ),
        }

        # Display results
        if results:
            print(f"✅ Found {len(results)} results!")
            for i, result in enumerate(results[:5], 1):
                print(f"  {i}. {result['name']} (Score: {result['score']:.1f})")
                print(f"     📁 {result['path']}")
                if result.get("preview"):
                    preview = (
                        result["preview"][:100] + "..."
                        if len(result["preview"]) > 100
                        else result["preview"]
                    )
                    print(f"     👁️ {preview}")
                print()
        else:
            print("❌ No results found. Try a different search term.")

        return search_result

    def index_all(self):
        """Index the entire workspace"""
        return self.search_engine.index_workspace(force_reindex=True)

    def stats(self):
        """Show search engine statistics"""
        stats = self.search_engine.get_search_stats()
        print("📊 Search Engine Statistics:")
        print(f"  📁 Indexed Files: {stats['indexed_files']}")
        print(f"  🔍 Total Searches: {stats['total_searches']}")
        print(f"  ⚡ Avg Search Time: {stats['avg_search_time']}s")

        if stats["common_searches"]:
            print("  🔥 Popular Searches:")
            for search in stats["common_searches"]:
                print(f"    - '{search['query']}' ({search['frequency']} times)")

        return stats


# Create search interface
search_interface = SearchInterface()

if __name__ == "__main__":
    print("🔍 BROSKI ULTRA SEARCH ENGINE ACTIVATED!")
    print("=" * 50)

    # Index workspace
    indexed = search_interface.index_all()
    print(f"📚 Workspace indexed: {indexed} files")

    # Show stats
    stats = search_interface.stats()

    # Test search
    print("\n🧪 Testing search capabilities...")
    test_results = search_interface.find("discord bot")

    print("\n🎉 Ultra Search Engine ready for lightning-fast file discovery!")
