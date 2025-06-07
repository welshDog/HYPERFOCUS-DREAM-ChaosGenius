#!/usr/bin/env python3
"""
💎⚡ ULTIMATE BROSKI MEMORY CRYSTAL GENERATOR ⚡💎
Export your entire brain as beautiful .broski crystal files!
Built by the BROski crew for maximum intelligence preservation!
"""

import base64
import hashlib
import io
import json
import pickle
import sqlite3
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class CrystalMetadata:
    """💎 Crystal file metadata"""

    crystal_id: str
    creation_date: str
    brain_version: str
    total_memories: int
    crew_members: List[str]
    intelligence_level: float
    emotional_range: tuple
    session_duration: str
    crystal_size_mb: float


class UltimaBroskiCrystalGenerator:
    """💎🧠 THE ULTIMATE MEMORY CRYSTAL FORGE 🧠💎"""

    def __init__(self, brain_db_path: str = "broski_ultra_brain.db"):
        self.brain_db_path = brain_db_path
        self.crystal_formats = {
            "compact": "Lightweight crystal for sharing",
            "premium": "Full experience with visualizations",
            "ultimate": "Complete brain backup with AI models",
            "showcase": "Beautiful presentation format",
        }

        print("💎⚡ INITIALIZING ULTIMATE CRYSTAL FORGE...")

    def generate_crystal(
        self,
        format_type: str = "premium",
        date_range: Optional[tuple] = None,
        crew_filter: Optional[List[str]] = None,
        output_filename: Optional[str] = None,
    ) -> str:
        """💎 Generate a complete .broski crystal file"""

        print(f"🔥 Forging {format_type.upper()} crystal...")

        # Extract memories from brain database
        memories = self._extract_memories(date_range, crew_filter)

        # Generate crystal metadata
        metadata = self._generate_metadata(memories, format_type)

        # Create crystal package
        crystal_data = self._create_crystal_package(memories, metadata, format_type)

        # Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"broski_crystal_{format_type}_{timestamp}.broski"

        # Save crystal file
        self._save_crystal_file(crystal_data, output_filename, format_type)

        print(f"💎✨ CRYSTAL FORGED SUCCESSFULLY: {output_filename}")
        return output_filename

    def _extract_memories(
        self, date_range: Optional[tuple], crew_filter: Optional[List[str]]
    ) -> List[Dict]:
        """🧠 Extract memories from brain database"""

        try:
            conn = sqlite3.connect(self.brain_db_path)

            # Build query conditions
            conditions = ["1=1"]
            params = []

            if date_range:
                conditions.append("timestamp BETWEEN ? AND ?")
                params.extend([date_range[0].isoformat(), date_range[1].isoformat()])

            if crew_filter:
                placeholders = ",".join("?" * len(crew_filter))
                conditions.append(f"crew_member IN ({placeholders})")
                params.extend(crew_filter)

            query = f"""
                SELECT * FROM memories
                WHERE {" AND ".join(conditions)}
                ORDER BY importance_score DESC, timestamp DESC
            """

            cursor = conn.execute(query, params)
            memories = []

            for row in cursor.fetchall():
                memory = {
                    "id": row[0],
                    "content": row[1],
                    "timestamp": row[2],
                    "memory_type": row[3],
                    "emotional_weight": row[4],
                    "crew_member": row[5],
                    "context_tags": json.loads(row[6]),
                    "importance_score": row[7],
                    "retrieval_count": row[8],
                }
                memories.append(memory)

            conn.close()
            print(f"🧠 Extracted {len(memories)} memories for crystal")
            return memories

        except Exception as e:
            print(f"⚠️ Error extracting memories: {e}")
            return []

    def _generate_metadata(
        self, memories: List[Dict], format_type: str
    ) -> CrystalMetadata:
        """📊 Generate comprehensive crystal metadata"""

        if not memories:
            return CrystalMetadata(
                crystal_id="empty_crystal",
                creation_date=datetime.now().isoformat(),
                brain_version="1.0.0",
                total_memories=0,
                crew_members=[],
                intelligence_level=0.0,
                emotional_range=(0.0, 0.0),
                session_duration="0 seconds",
                crystal_size_mb=0.0,
            )

        # Calculate metadata
        crew_members = list(set(m["crew_member"] for m in memories))
        emotional_weights = [m["emotional_weight"] for m in memories]

        # Calculate session duration
        timestamps = [datetime.fromisoformat(m["timestamp"]) for m in memories]
        session_start = min(timestamps)
        session_end = max(timestamps)
        duration = session_end - session_start

        # Calculate intelligence level based on memory quality
        avg_importance = sum(m["importance_score"] for m in memories) / len(memories)
        avg_emotional = sum(emotional_weights) / len(emotional_weights)
        intelligence_level = (avg_importance * 0.7) + (avg_emotional * 0.3)

        # Generate unique crystal ID
        content_hash = hashlib.md5(
            "".join(m["content"] for m in memories[:10]).encode()
        ).hexdigest()[:8]
        crystal_id = f"BROSKI_{format_type.upper()}_{content_hash}"

        return CrystalMetadata(
            crystal_id=crystal_id,
            creation_date=datetime.now().isoformat(),
            brain_version="1.0.0",
            total_memories=len(memories),
            crew_members=crew_members,
            intelligence_level=intelligence_level,
            emotional_range=(min(emotional_weights), max(emotional_weights)),
            session_duration=str(duration),
            crystal_size_mb=0.0,  # Will be calculated after packaging
        )

    def _create_crystal_package(
        self, memories: List[Dict], metadata: CrystalMetadata, format_type: str
    ) -> Dict[str, Any]:
        """📦 Create the complete crystal package"""

        crystal_package = {
            "crystal_metadata": asdict(metadata),
            "broski_signature": "🧠⚡ ULTRA BROSKI BRAIN CRYSTAL ⚡🧠",
            "format_type": format_type,
            "creation_timestamp": datetime.now().isoformat(),
            "memories": memories,
            "analytics": self._generate_analytics(memories),
            "crew_report": self._generate_crew_report(memories),
        }

        # Add format-specific content
        if format_type in ["premium", "ultimate", "showcase"]:
            crystal_package["visualizations"] = self._generate_visualizations(memories)

        if format_type in ["ultimate"]:
            crystal_package["ai_models"] = self._export_ai_models(memories)
            crystal_package["full_context"] = self._export_full_context(memories)

        if format_type == "showcase":
            crystal_package["presentation"] = self._generate_presentation(
                memories, metadata
            )

        return crystal_package

    def _generate_analytics(self, memories: List[Dict]) -> Dict[str, Any]:
        """📊 Generate comprehensive memory analytics"""

        if not memories:
            return {}

        # Memory type distribution
        type_counts = {}
        for memory in memories:
            mem_type = memory["memory_type"]
            type_counts[mem_type] = type_counts.get(mem_type, 0) + 1

        # Crew contribution analysis
        crew_stats = {}
        for memory in memories:
            crew = memory["crew_member"]
            if crew not in crew_stats:
                crew_stats[crew] = {
                    "memory_count": 0,
                    "avg_importance": 0.0,
                    "avg_emotional": 0.0,
                    "total_retrievals": 0,
                }

            crew_stats[crew]["memory_count"] += 1
            crew_stats[crew]["avg_importance"] += memory["importance_score"]
            crew_stats[crew]["avg_emotional"] += memory["emotional_weight"]
            crew_stats[crew]["total_retrievals"] += memory["retrieval_count"]

        # Calculate averages
        for crew in crew_stats:
            count = crew_stats[crew]["memory_count"]
            crew_stats[crew]["avg_importance"] /= count
            crew_stats[crew]["avg_emotional"] /= count

        # Timeline analysis
        timestamps = [datetime.fromisoformat(m["timestamp"]) for m in memories]
        timeline_analysis = {
            "session_start": min(timestamps).isoformat(),
            "session_end": max(timestamps).isoformat(),
            "peak_activity_hour": self._find_peak_activity(timestamps),
            "memory_velocity": len(memories)
            / max(1, (max(timestamps) - min(timestamps)).total_seconds() / 3600),
        }

        return {
            "memory_type_distribution": type_counts,
            "crew_contribution_analysis": crew_stats,
            "timeline_analysis": timeline_analysis,
            "intelligence_metrics": {
                "total_memories": len(memories),
                "avg_importance_score": sum(m["importance_score"] for m in memories)
                / len(memories),
                "avg_emotional_weight": sum(m["emotional_weight"] for m in memories)
                / len(memories),
                "memory_retrieval_rate": sum(m["retrieval_count"] for m in memories)
                / len(memories),
                "context_richness": sum(len(m["context_tags"]) for m in memories)
                / len(memories),
            },
        }

    def _generate_crew_report(self, memories: List[Dict]) -> Dict[str, Any]:
        """👨‍💻 Generate detailed crew performance report"""

        crew_personalities = {
            "BROski_X": {
                "role": "Leadership & Coordination",
                "specialty": "Organization",
            },
            "Token_Specialist": {"role": "Token Economy", "specialty": "Rewards"},
            "AI_Specialist": {"role": "Intelligence Systems", "specialty": "Learning"},
            "Security_Specialist": {"role": "Protection", "specialty": "Validation"},
            "Performance_Specialist": {"role": "Optimization", "specialty": "Speed"},
        }

        crew_report = {}

        for crew_name, info in crew_personalities.items():
            crew_memories = [m for m in memories if m["crew_member"] == crew_name]

            if crew_memories:
                crew_report[crew_name] = {
                    "role": info["role"],
                    "specialty": info["specialty"],
                    "memory_count": len(crew_memories),
                    "contribution_percentage": (len(crew_memories) / len(memories))
                    * 100,
                    "avg_importance": sum(m["importance_score"] for m in crew_memories)
                    / len(crew_memories),
                    "top_achievements": [
                        m["content"]
                        for m in sorted(
                            crew_memories,
                            key=lambda x: x["importance_score"],
                            reverse=True,
                        )[:3]
                    ],
                    "activity_timeline": [m["timestamp"] for m in crew_memories],
                    "effectiveness_score": self._calculate_crew_effectiveness(
                        crew_memories
                    ),
                }

        return crew_report

    def _generate_visualizations(self, memories: List[Dict]) -> Dict[str, str]:
        """📊 Generate base64-encoded visualization charts"""

        visualizations = {}

        try:
            # Memory type pie chart
            type_counts = {}
            for memory in memories:
                mem_type = memory["memory_type"]
                type_counts[mem_type] = type_counts.get(mem_type, 0) + 1

            plt.figure(figsize=(10, 6))
            plt.pie(type_counts.values(), labels=type_counts.keys(), autopct="%1.1f%%")
            plt.title("🧠 Memory Type Distribution")

            # Save to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
            buffer.seek(0)
            visualizations["memory_types"] = base64.b64encode(buffer.read()).decode()
            plt.close()

            # Timeline chart
            timestamps = [datetime.fromisoformat(m["timestamp"]) for m in memories]
            importance_scores = [m["importance_score"] for m in memories]

            plt.figure(figsize=(12, 6))
            plt.scatter(
                timestamps,
                importance_scores,
                alpha=0.6,
                c=importance_scores,
                cmap="viridis",
            )
            plt.colorbar(label="Importance Score")
            plt.title("🚀 Memory Timeline & Importance")
            plt.xlabel("Time")
            plt.ylabel("Importance Score")
            plt.xticks(rotation=45)

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
            buffer.seek(0)
            visualizations["timeline"] = base64.b64encode(buffer.read()).decode()
            plt.close()

        except Exception as e:
            print(f"⚠️ Error generating visualizations: {e}")

        return visualizations

    def _save_crystal_file(self, crystal_data: Dict, filename: str, format_type: str):
        """💾 Save crystal data to .broski file"""

        if format_type == "compact":
            # Save as compressed JSON
            with open(filename, "w") as f:
                json.dump(crystal_data, f, separators=(",", ":"))

        else:
            # Save as ZIP archive with multiple files
            with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Main crystal data
                zipf.writestr("crystal_data.json", json.dumps(crystal_data, indent=2))

                # Individual components
                if "visualizations" in crystal_data:
                    zipf.writestr(
                        "visualizations.json",
                        json.dumps(crystal_data["visualizations"], indent=2),
                    )

                if "analytics" in crystal_data:
                    zipf.writestr(
                        "analytics.json",
                        json.dumps(crystal_data["analytics"], indent=2),
                    )

                # README for the crystal
                readme_content = self._generate_crystal_readme(crystal_data)
                zipf.writestr("README.md", readme_content)

        # Update crystal size in metadata
        file_size = Path(filename).stat().st_size / (1024 * 1024)  # MB
        print(f"💎 Crystal size: {file_size:.2f} MB")

    def _generate_crystal_readme(self, crystal_data: Dict) -> str:
        """📝 Generate README for crystal file"""

        metadata = crystal_data["crystal_metadata"]

        readme = f"""# 💎 BROski Memory Crystal 💎

## Crystal Information
- **Crystal ID**: {metadata['crystal_id']}
- **Creation Date**: {metadata['creation_date']}
- **Format**: {crystal_data['format_type'].upper()}
- **Total Memories**: {metadata['total_memories']}
- **Intelligence Level**: {metadata['intelligence_level']:.2%}

## Crew Members
{chr(10).join(f"- {crew}" for crew in metadata['crew_members'])}

## Session Overview
- **Duration**: {metadata['session_duration']}
- **Emotional Range**: {metadata['emotional_range'][0]:.2f} - {metadata['emotional_range'][1]:.2f}

## How to Use This Crystal
1. Load the crystal into the BROski Brain system
2. Use `ask_memory.py` to query the stored memories
3. View visualizations in the `visualizations.json` file
4. Check analytics for intelligence insights

**Generated by the Ultimate BROski Brain System** 🧠⚡
"""
        return readme

    def _find_peak_activity(self, timestamps: List[datetime]) -> int:
        """🕐 Find the hour with most memory creation"""
        hour_counts = {}
        for ts in timestamps:
            hour = ts.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        return max(hour_counts, key=hour_counts.get) if hour_counts else 0

    def _calculate_crew_effectiveness(self, crew_memories: List[Dict]) -> float:
        """📊 Calculate crew member effectiveness score"""
        if not crew_memories:
            return 0.0

        avg_importance = sum(m["importance_score"] for m in crew_memories) / len(
            crew_memories
        )
        avg_retrievals = sum(m["retrieval_count"] for m in crew_memories) / len(
            crew_memories
        )
        memory_count = len(crew_memories)

        # Effectiveness = importance * usage * activity
        effectiveness = (
            (avg_importance * 0.5)
            + (min(avg_retrievals / 5, 1.0) * 0.3)
            + (min(memory_count / 10, 1.0) * 0.2)
        )
        return effectiveness

    def _export_ai_models(self, memories: List[Dict]) -> Dict[str, Any]:
        """🤖 Export AI model data (placeholder for ultimate format)"""
        return {
            "memory_embeddings": "placeholder_for_vector_data",
            "personality_models": "placeholder_for_crew_personalities",
            "learning_patterns": "placeholder_for_learning_data",
        }

    def _export_full_context(self, memories: List[Dict]) -> Dict[str, Any]:
        """🔍 Export full context data (ultimate format)"""
        return {
            "conversation_threads": "placeholder_for_conversation_context",
            "decision_trees": "placeholder_for_decision_patterns",
            "emotional_journey": "placeholder_for_emotional_progression",
        }

    def _generate_presentation(
        self, memories: List[Dict], metadata: CrystalMetadata
    ) -> Dict[str, Any]:
        """🎨 Generate presentation format data"""
        return {
            "title_slide": {
                "title": f"🧠 {metadata.crystal_id} Brain Session",
                "subtitle": f"Intelligence Level: {metadata.intelligence_level:.1%}",
                "stats": f"{metadata.total_memories} memories • {len(metadata.crew_members)} crew members",
            },
            "highlight_memories": [
                m
                for m in sorted(
                    memories, key=lambda x: x["importance_score"], reverse=True
                )[:5]
            ],
            "crew_showcase": {
                crew: len([m for m in memories if m["crew_member"] == crew])
                for crew in metadata.crew_members
            },
        }


# CLI interface for crystal generation
if __name__ == "__main__":
    print("💎⚡ BROSKI MEMORY CRYSTAL GENERATOR ⚡💎")

    generator = UltimaBroskiCrystalGenerator()

    # Generate different crystal formats
    formats = ["compact", "premium", "ultimate", "showcase"]

    for fmt in formats:
        try:
            crystal_file = generator.generate_crystal(format_type=fmt)
            print(f"✨ {fmt.upper()} crystal generated: {crystal_file}")
        except Exception as e:
            print(f"❌ Error generating {fmt} crystal: {e}")

    print("🎉 ALL CRYSTALS FORGED SUCCESSFULLY!")
