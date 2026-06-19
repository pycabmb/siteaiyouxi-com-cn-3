from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

# Configuration: known site and keyword
REFERENCE_URL = "https://siteaiyouxi.com.cn"
FOCUS_KEYWORD = "爱游戏"

@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    source_url: str = field(default=REFERENCE_URL)
    note: str = field(default="")
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tags: List[str] = field(default_factory=list)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_brief(self) -> str:
        return f"[{self.created_at}] {self.keyword} from {self.source_url}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["note_preview"] = self.note[:50] + "..." if len(self.note) > 50 else self.note
        return d

    def __str__(self) -> str:
        return (
            f"KeywordNote(keyword={self.keyword!r}, "
            f"source_url={self.source_url!r}, "
            f"note={self.note!r}, "
            f"created_at={self.created_at!r}, "
            f"tags={self.tags})"
        )


@dataclass
class KeywordNoteCollection:
    """A container for multiple KeywordNote entries with formatting output."""
    notes: List[KeywordNote] = field(default_factory=list)
    default_source: str = field(default=REFERENCE_URL)

    def add_note(self, keyword: str, note: str = "", tags: Optional[List[str]] = None) -> KeywordNote:
        """Add a new note to the collection."""
        new_note = KeywordNote(
            keyword=keyword,
            source_url=self.default_source,
            note=note,
            tags=tags or []
        )
        self.notes.append(new_note)
        return new_note

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return all notes matching the given keyword (case-insensitive)."""
        return [note for note in self.notes if note.keyword.lower() == keyword.lower()]

    def list_all_briefs(self) -> List[str]:
        """Return a list of brief strings for all notes."""
        return [note.to_brief() for note in self.notes]

    def format_as_report(self) -> str:
        """Return a human-readable report of all notes."""
        if not self.notes:
            return "No keyword notes available."
        lines = ["=== Keyword Notes Report ==="]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.to_brief()}")
            if note.note:
                lines.append(f"   Note: {note.note}")
            if note.tags:
                lines.append(f"   Tags: {', '.join(note.tags)}")
            lines.append("")
        lines.append(f"Total notes: {len(self.notes)}")
        lines.append(f"Default source: {self.default_source}")
        return "\n".join(lines)

    def format_as_json_like(self) -> str:
        """Return a simple JSON-like representation (without external lib)."""
        dicts = [note.to_dict() for note in self.notes]
        result = "[\n"
        for d in dicts:
            items = []
            for k, v in d.items():
                items.append(f"    \"{k}\": \"{v}\"")
            inner = ",\n".join(items)
            result += "  {\n" + inner + "\n  },\n"
        result = result.rstrip(",\n") + "\n]"
        return result

    def __len__(self) -> int:
        return len(self.notes)


# Preloaded example usage / demo data
if __name__ == "__main__":
    collection = KeywordNoteCollection(default_source=REFERENCE_URL)

    # Add some example notes related to the focus keyword
    note1 = collection.add_note(
        keyword=FOCUS_KEYWORD,
        note="这是一个关于爱游戏的笔记示例，记录核心关键词。",
        tags=["游戏", "示例"]
    )
    note2 = collection.add_note(
        keyword="爱游戏-攻略",
        note="爱游戏平台的攻略收集与整理思路。",
        tags=["攻略", "平台"]
    )
    note3 = collection.add_note(
        keyword="爱游戏-评测",
        note="对爱游戏平台上热门游戏的简要评测。",
        tags=["评测", "热门"]
    )

    # Add a tag to an existing note
    note1.add_tag("关键词")

    # Display results
    print(collection.format_as_report())
    print("\n--- JSON-like format ---")
    print(collection.format_as_json_like())

    # Demonstrate find
    print("\n--- Find by keyword (case-insensitive) ---")
    results = collection.find_by_keyword("爱游戏")
    for r in results:
        print(r)