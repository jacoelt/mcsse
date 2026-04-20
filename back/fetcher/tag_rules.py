"""Tag normalization rules.

Raw tag strings from 9 different listing sources arrive with wildly varying
conventions: `Bed Wars`, `bed-wars`, `bedwars`, `bedw`, `bed_wars`, `BEDWARS`,
`Bed-Wars`. Plus typos, translations, junk superlatives, bare version numbers.

`normalize_tag(raw)` is the single entry point: it maps any raw tag string to
a canonical slug, or returns None if the tag should be dropped.
"""

import re
import unicodedata

import inflect

_inflect = inflect.engine()
_non_alnum = re.compile(r"[^a-z0-9]")


STOPWORDS: frozenset[str] = frozenset(
    {
        # Pure superlatives / meta noise
        "amazing",
        "awesome",
        "cool",
        "epic",
        "best",
        "good",
        "great",
        "nice",
        "new",
        "newest",
        "popular",
        "viral",
        "original",
        "normal",
        "normale",
        "simple",
        "mature",
        "friendly",
        "active",
        # Quantifier / vacuous words
        "any",
        "all",
        "andhigher",
        "andmore",
        "more",
        "morecomingsoon",
        "somanygamemodes",
        "somanygameplay",
        "soon",
        # Short single-syllable garbage / fragments
        "ect",
        "etc",
        "f",
        "fu",
        "bis",
        "bs",
        "ind",
        "pea",
        "spa",
        "van",
        "ve",
        "to",
        # Tautological (every server is a Minecraft server)
        "server",
        "minecraft",
        "minecraftserver",
        # Version-meta (server already has a game_version field)
        "anyversion",
        "allversions",
        "allversionsupport",
        "allversionsupported",
        "bedrocklatest",
        "allversion",
        # Platform duplicates (Server has an `edition` enum already)
        "pc",
        "pe",
        # Vague fragments that aren't recoverable without guessing
        "mund",  # appeared as standalone; means "world" in German but too short to alias
    }
)


ALIASES: dict[str, str] = {
    # Spelling mistakes / variants → canonical form
    "beadrock": "bedrock",
    "bulding": "building",
    "dangeon": "dungeon",
    "vanila": "vanilla",
    "vannilla": "vanilla",
    "semivanila": "semivanilla",
    "economi": "economy",
    "economoy": "economy",
    "econ": "economy",
    "eco": "economy",
    "servival": "survival",
    "suvival": "survival",
    "sur": "survival",
    "surv": "survival",
    "survia": "survival",
    "survie": "survival",  # French
    "sobrevivencia": "survival",  # Portuguese
    "sobrevivncia": "survival",  # Portuguese (encoding-truncated)
    "hayattakalma": "survival",  # Turkish
    "suevivalop": "survivalop",
    "skyb": "skyblock",
    "skybloc": "skyblock",
    "skywa": "skywars",
    "boxp": "boxpvp",
    "bedw": "bedwars",
    "bedwar": "bedwars",
    "eggwar": "eggwars",
    "skywar": "skywars",  # inflect singularizes; these modes are always plural
    "hungergame": "hungergames",
    "squidgame": "squidgames",
    "faction": "factions",
    "minigame": "minigames",
    "bedrockcompatibility": "crossplay",
    # Typo/truncation of real words
    "crac": "cracked",
    "cracke": "cracked",
    "crack": "cracked",
    "abili": "ability",
    # Abbreviations — keep the short form as canonical (tighter facet)
    "capturetheflag": "ctf",
    "playervsplayer": "pvp",
    "playerversusplayer": "pvp",
    "playervsenvironment": "pve",
    "playerversusenvironment": "pve",
    "hardcorefactions": "hcf",
    "minecraftmmo": "mcmmo",
    # Translations → English
    "aventura": "adventure",
    "macera": "adventure",  # Turkish
    "anarquia": "anarchy",
    "anarquico": "anarchy",
    "semianarquia": "semianarchy",
    "semianarquico": "semianarchy",
    "creatif": "creative",  # French
    "creativo": "creative",  # Spanish/Portuguese
    "construccion": "construction",
    "eventos": "events",
    "guerra": "war",
    "gladiador": "gladiator",
    "razas": "races",
    "reinos": "kingdoms",
    "protecciones": "protection",
    "komunita": "community",
    "parkur": "parkour",
    "nogomet": "soccer",  # Croatian for soccer
    "fudbal": "soccer",  # Serbian
    "zindan": "dungeon",  # Turkish
    "sohbet": "chat",  # Turkish
    "urbain": "urban",  # French
    "minijeux": "minigames",
    "rangosgratis": "freeranks",
    # Copycat servers → parent brand
    "hermitcraftlike": "hermitcraft",
    "factionslike": "factions",
    "2b2tcopy": "2b2t",
    # Client names — map aliases to canonical form
    "eagler": "eaglercraft",
    "tlauncher": "cracked",  # tlauncher is associated with cracked clients
}


DISPLAY_OVERRIDES: dict[str, str] = {
    # Acronyms — preserve casing
    "pvp": "PvP",
    "pve": "PvE",
    "ctf": "CTF",
    "smp": "SMP",
    "rpg": "RPG",
    "ffa": "FFA",
    "uhc": "UHC",
    "mmo": "MMO",
    "mmorpg": "MMORPG",
    "mcmmo": "mcMMO",
    "hcf": "HCF",
    "koth": "KoTH",
    "mlg": "MLG",
    "kitpvp": "KitPvP",
    "boxpvp": "BoxPvP",
    "skypvp": "SkyPvP",
    "2b2t": "2b2t",
    # Multi-word slugs that got collapsed — restore readable form
    "bedwars": "Bed Wars",
    "skywars": "Sky Wars",
    "eggwars": "Egg Wars",
    "hungergames": "Hunger Games",
    "squidgames": "Squid Games",
    "skyblock": "SkyBlock",
    "buildbattle": "Build Battle",
    "capturetheflag": "Capture the Flag",
    "battleroyale": "Battle Royale",
    "hideandseek": "Hide and Seek",
    "minigames": "Minigames",
    "survivalgames": "Survival Games",
    "factions": "Factions",
    "prison": "Prison",
    "survival": "Survival",
    "creative": "Creative",
    "hardcore": "Hardcore",
    "vanilla": "Vanilla",
    "anarchy": "Anarchy",
    "roleplay": "Roleplay",
    "adventure": "Adventure",
    "economy": "Economy",
    "parkour": "Parkour",
    "pixelmon": "Pixelmon",
    "towny": "Towny",
    "hermitcraft": "Hermitcraft",
    "crossplay": "Cross-Play",
    "eaglercraft": "EaglerCraft",
    "cracked": "Cracked",
}


def _safe_singularize(word: str) -> str:
    """inflect.singular_noun is over-eager on -ss and -us endings.

    `inflect.engine().singular_noun("boss")` returns "bos", `singular_noun("cactus")`
    returns "cactu". Guard those endings. Also reject any output shorter than 3
    chars (catches `bis` -> `bi`, `ads` -> `ad`).
    """
    if not word or word.endswith("ss") or word.endswith("us"):
        return word
    singular = _inflect.singular_noun(word)
    if not singular or len(singular) < 3:
        return word
    return singular


def normalize_tag(raw: str) -> str | None:
    """Map a raw tag string to a canonical slug, or None to drop it."""
    if not raw:
        return None

    x = raw.strip().lower()
    x = unicodedata.normalize("NFKD", x)
    x = x.encode("ascii", "ignore").decode("ascii")
    x = _non_alnum.sub("", x)

    if not x:
        return None
    if x.isdigit():
        return None
    if x in STOPWORDS:
        return None

    x = ALIASES.get(x, x)
    x = _safe_singularize(x)

    if x in STOPWORDS:
        return None

    x = ALIASES.get(x, x)

    return x or None


def display_name_for(canonical: str) -> str:
    if not canonical:
        return ""
    if canonical in DISPLAY_OVERRIDES:
        return DISPLAY_OVERRIDES[canonical]
    return canonical.title()
