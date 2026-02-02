"""
Dictionary Manager for loading and managing word lists.
Supports both French and English dictionaries.
"""

import os
from typing import List, Set


class DictionaryManager:
    """Manages word dictionaries for Wordle solving."""

    def __init__(self, word_length: int = 5):
        """
        Initialize dictionary manager.

        Args:
            word_length: Length of words to load
        """
        self.word_length = word_length
        self.words: Set[str] = set()

    def load_from_file(self, filepath: str) -> None:
        """
        Load words from a text file (one word per line).
        Resolves relative paths relative to the module's directory.

        Args:
            filepath: Path to dictionary file (absolute or relative to src/ directory)
        """
        # If filepath is relative, resolve it relative to the src/ directory
        if not os.path.isabs(filepath):
            module_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(module_dir, filepath)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dictionary file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if len(word) == self.word_length and word.isalpha():
                    self.words.add(word)

    def load_default_english(self) -> None:
        """Load default English word list."""
        # Common 5-letter English words for Wordle
        common_words = [
            "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
            "agent", "agree", "ahead", "alarm", "album", "alert", "align", "alike", "alive", "allow",
            "alone", "along", "alter", "among", "anger", "angle", "angry", "apart", "apple", "apply",
            "arena", "argue", "arise", "array", "aside", "asset", "audio", "audit", "avoid", "award",
            "aware", "badly", "baker", "bases", "basic", "basis", "beach", "began", "begin", "begun",
            "being", "below", "bench", "billy", "birth", "black", "blade", "blame", "blind", "block",
            "blood", "board", "boost", "booth", "bound", "brain", "brand", "bread", "break", "breed",
            "brief", "bring", "broad", "broke", "brown", "build", "built", "buyer", "cable", "calif",
            "carry", "catch", "cause", "chain", "chair", "chart", "chase", "cheap", "check", "chest",
            "chief", "child", "china", "chose", "civil", "claim", "class", "clean", "clear", "click",
            "clock", "close", "coach", "coast", "could", "count", "court", "cover", "crack", "craft",
            "crash", "crazy", "cream", "crime", "cross", "crowd", "crown", "crude", "curve", "cycle",
            "daily", "dance", "dated", "dealt", "death", "debut", "delay", "depth", "doing", "doubt",
            "dozen", "draft", "drama", "drank", "drawn", "dream", "dress", "drill", "drink", "drive",
            "drove", "dying", "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy",
            "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra", "faith",
            "false", "fault", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
            "flash", "fleet", "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found",
            "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny", "giant", "given",
            "glass", "globe", "going", "grace", "grade", "grand", "grant", "grass", "great", "green",
            "gross", "group", "grown", "guard", "guess", "guest", "guide", "happy", "harry", "heart",
            "heavy", "hence", "henry", "horse", "hotel", "house", "human", "ideal", "image", "index",
            "inner", "input", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label",
            "large", "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal",
            "lemon", "level", "lewis", "light", "limit", "links", "lives", "local", "logic", "loose",
            "lower", "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria", "match",
            "maybe", "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed", "model",
            "money", "month", "moral", "motor", "mount", "mouse", "mouth", "movie", "music", "needs",
            "never", "newly", "night", "noise", "north", "noted", "novel", "nurse", "occur", "ocean",
            "offer", "often", "order", "other", "ought", "paint", "panel", "paper", "party", "peace",
            "peter", "phase", "phone", "photo", "piece", "pilot", "pitch", "place", "plain", "plane",
            "plant", "plate", "point", "pound", "power", "press", "price", "pride", "prime", "print",
            "prior", "prize", "proof", "proud", "prove", "queen", "quick", "quiet", "quite", "radio",
            "raise", "range", "rapid", "ratio", "reach", "ready", "refer", "right", "rival", "river",
            "robin", "roger", "roman", "rough", "round", "route", "royal", "rural", "scale", "scene",
            "scope", "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet",
            "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "short", "shown", "sight",
            "since", "sixth", "sixty", "sized", "skill", "sleep", "slide", "small", "smart", "smile",
            "smith", "smoke", "solid", "solve", "sorry", "sound", "south", "space", "spare", "speak",
            "speed", "spend", "spent", "split", "spoke", "sport", "staff", "stage", "stake", "stand",
            "start", "state", "steam", "steel", "stick", "still", "stock", "stone", "stood", "store",
            "storm", "story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite", "super",
            "sweet", "table", "taken", "taste", "taxes", "teach", "terry", "texas", "thank", "theft",
            "their", "theme", "there", "these", "thick", "thing", "think", "third", "those", "three",
            "threw", "throw", "tight", "times", "title", "today", "topic", "total", "touch", "tough",
            "tower", "track", "trade", "train", "trait", "trend", "trial", "tribe", "trick", "tried",
            "tries", "troop", "truck", "truly", "trust", "truth", "twice", "under", "undue", "union",
            "unity", "until", "upper", "urban", "usage", "usual", "valid", "value", "video", "virus",
            "visit", "vital", "vocal", "voice", "waste", "watch", "water", "wheel", "where", "which",
            "while", "white", "whole", "whose", "woman", "women", "world", "worry", "worse", "worst",
            "worth", "would", "wound", "write", "wrong", "wrote", "young", "youth", "crane"
        ]

        self.words = set(w for w in common_words if len(w) == self.word_length)

    def load_default_french(self) -> None:
        """Load default French word list."""
        # Common 5-letter French words
        french_words = [
            "alors", "autre", "avant", "avoir", "blanc", "bonne", "carte", "cause", "cette", "celui",
            "chose", "comme", "corps", "cours", "droit", "effet", "enfin", "entre", "faire", "femme",
            "forme", "force", "grand", "groupe", "homme", "heure", "jamais", "jardin", "jeune", "jours",
            "livre", "leurs", "ligne", "leur", "mieux", "monde", "moins", "morte", "place", "plus",
            "point", "porte", "pour", "peuvent", "quand", "reste", "route", "sans", "seul", "sinon",
            "sous", "temps", "terre", "toute", "train", "trois", "trouve", "ville", "voici", "voila",
            "venir", "vivre", "vraie", "agent", "allez", "arbre", "avait", "belle", "boire", "brave",
            "calme", "champ", "chaud", "coeur", "crois", "debut", "demain", "deux", "doigt", "droit",
            "ecole", "eglise", "etait", "etant", "fille", "froid", "jaune", "juste", "aller", "lutte",
            "madame", "maison", "matin", "merci", "monte", "noire", "notre", "ocean", "oncle", "ordre",
            "parle", "parti", "passe", "pauvre", "pense", "peste", "petite", "piece", "poche", "porte",
            "poste", "prise", "puits", "quart", "reine", "riche", "rouge", "russe", "saint", "salle",
            "Seine", "serve", "seule", "signe", "sucre", "suite", "table", "tache", "tante", "tente",
            "tombe", "total", "trous", "vague", "valse", "vaste", "venir", "verre", "verte", "vieux",
            "vigne", "voire", "voisin", "votre", "wagon","fleur"
        ]

        self.words = set(w for w in french_words if len(w) == self.word_length)

    def add_words(self, words: List[str]) -> None:
        """
        Add words to the dictionary.

        Args:
            words: List of words to add
        """
        for word in words:
            word = word.lower().strip()
            if len(word) == self.word_length and word.isalpha():
                self.words.add(word)

    def get_words(self) -> List[str]:
        """
        Get all words in dictionary.

        Returns:
            Sorted list of words
        """
        return sorted(list(self.words))

    def contains(self, word: str) -> bool:
        """
        Check if a word is in the dictionary.

        Args:
            word: Word to check

        Returns:
            True if word is in dictionary
        """
        return word.lower() in self.words

    def size(self) -> int:
        """
        Get dictionary size.

        Returns:
            Number of words in dictionary
        """
        return len(self.words)
