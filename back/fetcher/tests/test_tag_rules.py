from django.test import SimpleTestCase

from fetcher.tag_rules import ALIASES, DISPLAY_OVERRIDES, display_name_for, normalize_tag


class NormalizeTagTest(SimpleTestCase):
    """Pure-function tests for the tag normalization pipeline."""

    def _check(self, cases):
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(normalize_tag(raw), expected)

    def test_empty_and_whitespace_returns_none(self):
        self._check(
            [
                ("", None),
                ("   ", None),
                ("\t\n", None),
            ]
        )

    def test_case_and_whitespace_normalization(self):
        self._check(
            [
                ("PvP", "pvp"),
                ("  Survival  ", "survival"),
                ("Bed Wars", "bedwars"),
            ]
        )

    def test_separator_collapse(self):
        """Aggressive collapse: hyphens, underscores, spaces all stripped."""
        self._check(
            [
                ("bed-wars", "bedwars"),
                ("bed wars", "bedwars"),
                ("bed_wars", "bedwars"),
                ("box-pvp", "boxpvp"),
                ("classic-prison", "classicprison"),
                ("capture-the-flag", "ctf"),  # alias resolves after collapse
            ]
        )

    def test_unicode_stripping(self):
        self._check(
            [
                ("créatif", "creative"),
                ("sobrevivência", "survival"),
                ("Crack\ufffd", "cracked"),
            ]
        )

    def test_bare_numeric_dropped(self):
        """Version-number-like tags have a dedicated column; drop them."""
        self._check(
            [
                ("1710", None),
                ("12160", None),
                ("118", None),
                ("247", None),
            ]
        )

    def test_plural_singularization(self):
        self._check(
            [
                ("auctions", "auction"),
                ("clans", "clan"),
                ("bosses", "boss"),
                ("cities", "city"),
                ("mods", "mod"),
            ]
        )

    def test_safe_singularization_does_not_strip_ss_or_us(self):
        """inflect mis-singularizes short -ss/-us words; guard catches them."""
        self._check(
            [
                ("boss", "boss"),
                ("glass", "glass"),
                ("class", "class"),
                ("mass", "mass"),
                ("cactus", "cactus"),
                ("bus", "bus"),
            ]
        )

    def test_stopword_drop(self):
        self._check(
            [
                ("amazing", None),
                ("awesome", None),
                ("any", None),
                ("all", None),
                ("and-higher", None),
                ("more coming soon", None),
            ]
        )

    def test_alias_rewrite(self):
        self._check(
            [
                ("bedw", "bedwars"),
                ("capturetheflag", "ctf"),  # canonical is the abbreviation
                ("aventura", "adventure"),
                ("anarquia", "anarchy"),
                ("vanila", "vanilla"),
            ]
        )

    def test_alias_applied_after_separator_collapse(self):
        """Aliases are keyed on post-normalization strings."""
        self._check(
            [
                ("Bed-Wars", "bedwars"),
                ("Capture The Flag", "ctf"),
            ]
        )

    def test_second_pass_alias_after_singularization(self):
        """Singularization can produce an aliasable form (step 10)."""
        # "eggwars" (plural) → inflect → "eggwar" → no alias → stays "eggwar"
        # But we want it canonical as "eggwars". Alias pins it.
        self._check(
            [
                ("eggwar", "eggwars"),  # alias after singularization attempt
            ]
        )


class AliasMapInvariantsTest(SimpleTestCase):
    """Structural invariants on the ALIASES and STOPWORDS tables."""

    def test_aliases_are_single_step_not_transitive(self):
        """An alias value must not also be an alias key."""
        collisions = set(ALIASES.keys()) & set(ALIASES.values())
        self.assertEqual(collisions, set(), f"Aliases form a chain: {collisions}")

    def test_alias_keys_are_normalized_form(self):
        """Every alias key must be lowercase alphanumeric only."""
        for key in ALIASES:
            self.assertTrue(key.isalnum(), f"Alias key {key!r} is not alphanumeric")
            self.assertEqual(key, key.lower(), f"Alias key {key!r} is not lowercase")

    def test_alias_values_are_normalized_form(self):
        for value in ALIASES.values():
            self.assertTrue(value.isalnum(), f"Alias value {value!r} is not alphanumeric")
            self.assertEqual(value, value.lower(), f"Alias value {value!r} is not lowercase")


class DisplayNameTest(SimpleTestCase):
    def test_override_returns_custom_form(self):
        # This test assumes the seed includes these entries.
        self.assertEqual(display_name_for("pvp"), DISPLAY_OVERRIDES["pvp"])

    def test_unknown_slug_falls_back_to_title_case(self):
        self.assertEqual(display_name_for("random"), "Random")

    def test_empty_returns_empty(self):
        self.assertEqual(display_name_for(""), "")
