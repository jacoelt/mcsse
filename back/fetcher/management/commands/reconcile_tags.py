"""One-shot (but idempotent, re-runnable) cleanup of the Tag table.

Applies the current fetcher.tag_rules to every existing Tag row and the Server
M2M relations pointing at them. Safe to re-run whenever tag_rules changes.

Usage:
    python manage.py reconcile_tags             # execute
    python manage.py reconcile_tags --dry-run   # show plan, no writes
    python manage.py reconcile_tags -v 2        # per-tag action log
"""

from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Server, Tag
from fetcher.tag_rules import display_name_for, normalize_tag


class Command(BaseCommand):
    help = "Reconcile existing Tag rows against fetcher.tag_rules (merge/rename/delete)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show the plan without writing to the database.",
        )

    def handle(self, *args, dry_run=False, verbosity=1, **options):
        plan = self._build_plan()

        self._print_summary(plan, dry_run=dry_run)

        if verbosity >= 2:
            self._print_detail(plan)

        if dry_run:
            return

        with transaction.atomic():
            self._execute(plan)

        final_count = Tag.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Done. {final_count} tags remain."))

    def _build_plan(self):
        """Classify every existing Tag into keep / rename / merge / delete.

        Returns a dict with these buckets:
            keeps:     list[Tag]                         - canonical, untouched
            renames:   list[tuple[Tag, str]]             - (source, new_canonical_slug)
            merges:    list[tuple[Tag, Tag]]             - (source, target) both Tag objects
            deletes:   list[Tag]                         - to remove entirely
        """
        all_tags = list(Tag.objects.all())
        by_name: dict[str, Tag] = {t.name: t for t in all_tags}

        # First pass: classify each tag
        classified: list[tuple[Tag, str | None]] = []  # (tag, canonical)
        for tag in all_tags:
            canonical = normalize_tag(tag.name)
            classified.append((tag, canonical))

        # Group non-canonical tags by their target canonical slug, so we know
        # whether we can rename in place vs. must merge (multiple sources).
        sources_by_target: dict[str, list[Tag]] = defaultdict(list)
        for tag, canonical in classified:
            if canonical is not None and canonical != tag.name:
                sources_by_target[canonical].append(tag)

        keeps: list[Tag] = []
        renames: list[tuple[Tag, str]] = []
        merges: list[tuple[Tag, Tag]] = []
        deletes: list[Tag] = []

        for tag, canonical in classified:
            if canonical is None:
                deletes.append(tag)
                continue

            if canonical == tag.name:
                keeps.append(tag)
                continue

            # tag.name != canonical
            target_exists = canonical in by_name
            sources_for_target = sources_by_target[canonical]

            if not target_exists and len(sources_for_target) == 1:
                # Safe to rename in place: no one else is competing for this slug.
                renames.append((tag, canonical))
            else:
                # Target exists already, or multiple tags map to same canonical.
                # Create target Tag if it doesn't yet exist.
                if not target_exists:
                    # Promote the first source in the list to be the target.
                    promoted = sources_for_target[0]
                    if tag.id == promoted.id:
                        renames.append((tag, canonical))
                        # Update our view so subsequent siblings see the target.
                        by_name[canonical] = tag
                        continue
                    # else: wait until the promoted one is renamed; we merge into it
                    target = promoted
                else:
                    target = by_name[canonical]

                merges.append((tag, target))

        return {
            "keeps": keeps,
            "renames": renames,
            "merges": merges,
            "deletes": deletes,
        }

    def _print_summary(self, plan, *, dry_run: bool):
        total = sum(len(plan[k]) for k in ("keeps", "renames", "merges", "deletes"))
        self.stdout.write(f"{total} tags analyzed:")
        self.stdout.write(f"  {len(plan['keeps'])} keep as-is")
        self.stdout.write(f"  {len(plan['renames'])} rename")
        self.stdout.write(f"  {len(plan['merges'])} merge")
        self.stdout.write(f"  {len(plan['deletes'])} delete")
        final = len(plan["keeps"]) + len(plan["renames"])
        # +1 per unique merge target that had to be created fresh
        merge_targets_created = len(
            {t.id for _, t in plan["merges"] if t.id is None}
        )
        final += merge_targets_created
        self.stdout.write(
            f"After: ~{final} canonical tags"
            + (" (dry-run, no writes)" if dry_run else "")
        )

    def _print_detail(self, plan):
        for tag, new_name in plan["renames"]:
            self.stdout.write(f"  RENAME {tag.name!r} -> {new_name!r}")
        # Pending renames change what merge targets will be called post-execute.
        rename_map = {tag.id: new_name for tag, new_name in plan["renames"]}
        for source, target in plan["merges"]:
            resolved_target = rename_map.get(target.id, target.name)
            self.stdout.write(f"  MERGE  {source.name!r} -> {resolved_target!r}")
        for tag in plan["deletes"]:
            self.stdout.write(f"  DELETE {tag.name!r}")

    def _execute(self, plan):
        through = Server.tags.through

        # 1. Renames — no M2M work needed
        for tag, new_name in plan["renames"]:
            tag.name = new_name
            tag.display_name = display_name_for(new_name)
            tag.save(update_fields=["name", "display_name"])

        # 2. Merges — move M2M rows, avoiding unique-constraint collisions
        for source, target in plan["merges"]:
            # If the target is itself a tag that was just renamed in pass 1,
            # refresh it from the DB so we have the current id.
            target.refresh_from_db()

            # Rows where target tag is NOT already linked to the same server:
            # reassign tag_id.
            through.objects.filter(tag_id=source.id).exclude(
                server_id__in=through.objects.filter(tag_id=target.id).values("server_id")
            ).update(tag_id=target.id)

            # Remaining rows are duplicates (server already linked to target);
            # delete them outright.
            through.objects.filter(tag_id=source.id).delete()

            source.delete()

        # 3. Deletes — stopwords and bare numerics
        delete_ids = [t.id for t in plan["deletes"]]
        if delete_ids:
            through.objects.filter(tag_id__in=delete_ids).delete()
            Tag.objects.filter(id__in=delete_ids).delete()
