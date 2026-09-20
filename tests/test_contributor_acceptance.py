import base64
import copy
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from tools.contributor_acceptance import (
    AGREEMENT, END, START, RECORDS_BRANCH, MAX_FILES, Acceptance, ApiError, Blocked, GitHub, Ledger,
    accepted_event, agreement_from, block, canonical, digest,
    extract_block, make_context, replace_block, sole_author,
)


REPO = {"id": 10, "full_name": "owner/localization", "owner": {"id": 1}, "default_branch": "main"}
TEXT = "# Contributor Agreement\n\nVersion 1.0\n\nExclusive worldwide rights.\n"
AGREE = agreement_from(TEXT, "a" * 40, REPO["full_name"])


def pull():
    return {"number": 7, "state": "open", "body": "My translation\n", "user": {"id": 2},
            "head": {"sha": "b" * 40}, "base": {"sha": "c" * 40, "ref": "main"},
            "changed_files": 1, "commits": 1, "updated_at": "2026-09-17T12:00:00Z"}


def comparison():
    return {"merge_base_commit": {"sha": "d" * 40}, "files": [
        {"filename": "translations/de/ui_de.arb", "status": "added", "sha": "e" * 40}]}


def commit(author=2, message="Translate settings"):
    return {"author": {"id": author}, "commit": {"message": message}}


class MemoryLedger:
    def __init__(self):
        self.states = {}
        self.records = {}
        self.fail = False

    def state(self, number):
        return copy.deepcopy(self.states.get(number))

    def read(self, path):
        return copy.deepcopy(self.records.get(path))

    def save(self, number, state, record=None):
        if self.fail:
            raise ApiError(503, "/records")
        self.states[number] = copy.deepcopy(state)
        if record:
            path, value = record
            if path in self.records and self.records[path] != value:
                raise AssertionError("Attempted evidence overwrite")
            self.records[path] = copy.deepcopy(value)


class FakeAPI:
    def __init__(self):
        self.pr = pull()
        self.compare = comparison()
        self.files = self.compare["files"]
        self.commits = [commit()]
        self.calls = []
        self.checks = []
        self.statuses = []
        self.agreement = AGREE
        self.before_read = None
        self.file_mode = "100644"
        self.merge_sha = "e" * 40

    def get(self, path):
        self.calls.append(("GET", path))
        if path.endswith("/pulls/7"):
            if self.before_read:
                callback, self.before_read = self.before_read, None
                callback()
            return copy.deepcopy(self.pr)
        if "/check-runs?" in path:
            return {"check_runs": []}
        if "/compare/" in path:
            return copy.deepcopy(self.compare)
        if "/pulls/7/files?" in path:
            query = parse_qs(urlsplit(path).query)
            size, page = int(query["per_page"][0]), int(query["page"][0])
            return copy.deepcopy(self.files[(page - 1) * size:page * size])
        if "/commits?" in path:
            return [{"sha": self.agreement["commit"]}]
        if "/contents/" + AGREEMENT in path:
            return {"encoding": "base64", "content": base64.b64encode(self.agreement["text"].encode()).decode()}
        if "/git/trees/" in path:
            sha = self.merge_sha if "7" * 40 in path else "e" * 40
            return {"tree": [{"path": file["filename"], "mode": self.file_mode,
                              "type": "blob", "sha": sha} for file in self.files], "truncated": False}
        if "/git/blobs/" in path:
            return {"encoding": "base64", "sha": "e" * 40,
                    "content": base64.b64encode(b'{"hello":"Hallo"}').decode()}
        raise AssertionError(path)

    def pages(self, path):
        self.calls.append(("GET", path))
        if path.endswith("/files"):
            return GitHub.pages(self, path)
        return copy.deepcopy(self.commits)

    def request(self, method, path, data):
        self.calls.append((method, path))
        if "/statuses/" in path:
            self.statuses.append(copy.deepcopy(data))
            return {"id": len(self.statuses)}
        if path.endswith("/check-runs"):
            self.checks.append(copy.deepcopy(data))
            return {"id": len(self.checks)}
        if path.endswith("/pulls/7"):
            self.pr["body"] = data["body"]
            return copy.deepcopy(self.pr)
        raise AssertionError((method, path))


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeAPI()
        self.ledger = MemoryLedger()
        self.run_id = 100

    def service(self, event=None, name="pull_request_target"):
        self.run_id += 1
        return Acceptance(self.api, self.ledger, REPO, name, event or {"action": "opened"},
                          {"id": str(self.run_id), "attempt": "1", "workflow_sha": "f" * 40})

    def prepare(self):
        self.service().process(7)
        return self.ledger.state(7)["context"]

    def tick(self, actor=2):
        before = self.api.pr["body"]
        context = self.ledger.state(7)["context"]
        self.api.pr["body"] = replace_block(before, block(context, True))
        return {"action": "edited", "sender": {"id": actor, "login": "translator", "type": "User"},
                "pull_request": copy.deepcopy(self.api.pr), "changes": {"body": {"from": before}}}

    def accept(self):
        self.prepare()
        self.service(self.tick()).process(7)

    def test_open_prepares_unchecked_pinned_declaration(self):
        context = self.prepare()
        self.assertEqual(extract_block(self.api.pr["body"]), block(context))
        self.assertIn("/blob/" + "a" * 40, self.api.pr["body"])
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")
        self.assertFalse(self.ledger.records)

    def test_author_acceptance_retains_text_actor_and_complete_snapshot(self):
        self.accept()
        self.assertEqual(self.api.checks[-1]["conclusion"], "success")
        record = next(iter(self.ledger.records.values()))
        self.assertEqual(record["actor"]["id"], 2)
        self.assertEqual(record["agreement_text"], TEXT)
        self.assertEqual(record["pr_description"], self.api.pr["body"])
        self.assertEqual(base64.b64decode(record["snapshot"][0]["after"]["base64"]), b'{"hello":"Hallo"}')

    def test_required_status_passes_only_after_acceptance_is_retained(self):
        self.prepare()
        self.assertEqual(self.api.statuses[-1]["context"], "contributor-acceptance")
        self.assertEqual(self.api.statuses[-1]["state"], "failure")
        self.assertNotIn("success", [status["state"] for status in self.api.statuses])
        self.service(self.tick()).process(7)
        self.assertEqual(self.api.statuses[-1]["state"], "success")
        self.assertEqual(self.api.checks[-1]["name"], "contributor-acceptance-record")
        self.assertEqual(self.api.calls[-1], ("POST", "/repos/owner/localization/statuses/" + "b" * 40))
        self.assertLessEqual(len(self.api.statuses[-1]["description"]), 140)
        self.assertTrue(self.ledger.records)

    def test_recheck_invalidates_status_before_reading_evidence(self):
        self.accept()
        self.ledger.records.clear()
        with self.assertRaises(Blocked):
            self.service(name="schedule").process(7)
        self.assertEqual(self.api.statuses[-1]["state"], "failure")

    def test_changed_head_needs_new_acceptance_status(self):
        self.accept()
        self.api.pr["head"]["sha"] = "9" * 40
        self.service({"action": "synchronize"}).process(7)
        self.assertEqual(self.api.statuses[-1]["state"], "failure")
        self.assertIn(("POST", "/repos/owner/localization/statuses/" + "9" * 40), self.api.calls)
        self.assertIsNone(self.ledger.state(7)["acceptance"])

    def test_legacy_check_is_renamed_before_success_status(self):
        original_get, original_request = self.api.get, self.api.request
        patches = []

        def get(path):
            if "check_name=contributor-acceptance&" in path:
                return {"check_runs": [{"id": 42, "external_id": "ks-acceptance:10:7",
                                        "app": {"slug": "github-actions"}}]}
            return original_get(path)

        def request(method, path, data):
            if path.endswith("/check-runs/42"):
                patches.append(copy.deepcopy(data))
                self.assertFalse(self.api.statuses)
                return {}
            return original_request(method, path, data)

        self.api.get, self.api.request = get, request
        self.service().check(self.api.pr, "success", "Verified retained acceptance")
        self.assertEqual(patches[0], {"name": "contributor-acceptance-record"})
        self.assertEqual(patches[-1]["conclusion"], "success")
        self.assertEqual(self.api.statuses[-1]["state"], "success")

    def test_failed_check_publication_does_not_publish_success_status(self):
        original_request = self.api.request

        def request(method, path, data):
            if path.endswith("/check-runs"):
                raise ApiError(503, path)
            return original_request(method, path, data)

        self.api.request = request
        with self.assertRaises(ApiError):
            self.service().check(self.api.pr, "success", "Verified retained acceptance")
        self.assertFalse(self.api.statuses)

    def test_maintainer_cannot_accept_for_author(self):
        context = self.prepare()
        self.service(self.tick(actor=1)).process(7)
        self.assertFalse(self.ledger.records)
        self.assertEqual(extract_block(self.api.pr["body"]), block(context))

    def test_changed_disclosure_requires_fresh_acceptance(self):
        self.accept()
        self.api.pr["body"] = "Updated AI rights disclosure\n" + self.api.pr["body"]
        self.service({"action": "edited"}).process(7)
        self.assertIsNone(self.ledger.state(7)["acceptance"])
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")
        self.assertIn("- [ ]", extract_block(self.api.pr["body"]))

    def test_bot_cannot_accept(self):
        self.prepare()
        event = self.tick()
        event["sender"]["type"] = "Bot"
        self.service(event).process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")

    def test_title_edit_with_old_checked_box_cannot_accept(self):
        self.prepare()
        event = self.tick()
        event["changes"] = {"title": {"from": "Old title"}}
        self.service(event).process(7)
        self.assertFalse(self.ledger.records)

    def test_manually_fabricated_checked_declaration_cannot_accept_on_open(self):
        context = make_context(self.api.pr, AGREE, self.api.compare, self.api.files)
        self.api.pr["body"] = block(context, True)
        self.service({"action": "opened"}).process(7)
        self.assertFalse(self.ledger.records)

    def test_declared_terms_cannot_be_shortened(self):
        self.prepare()
        event = self.tick()
        self.api.pr["body"] = self.api.pr["body"].replace("exclusive worldwide", "nonexclusive")
        event["pull_request"] = copy.deepcopy(self.api.pr)
        self.service(event).process(7)
        self.assertFalse(self.ledger.records)

    def test_event_cannot_apply_to_new_head(self):
        self.prepare()
        event = self.tick()
        self.api.pr["head"]["sha"] = "9" * 40
        self.service(event).process(7)
        self.assertFalse(self.ledger.records)
        self.assertIn("9" * 40, self.api.pr["body"])

    def test_event_cannot_apply_after_a_later_body_edit(self):
        self.prepare()
        event = self.tick()
        self.api.pr["body"] += "\nA later edit"
        self.service(event).process(7)
        self.assertFalse(self.ledger.records)

    def test_old_event_with_identical_body_but_later_edit_is_not_accepted(self):
        self.prepare()
        event = self.tick()
        self.api.pr["updated_at"] = "2026-09-17T12:01:00Z"
        self.service(event).process(7)
        self.assertFalse(self.ledger.records)

    def test_new_commit_invalidates_previously_successful_acceptance(self):
        self.accept()
        old_records = copy.deepcopy(self.ledger.records)
        self.api.pr["head"]["sha"] = "9" * 40
        self.service({"action": "synchronize"}).process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")
        self.assertEqual(self.ledger.records, old_records)
        self.assertIsNone(self.ledger.state(7)["acceptance"])

    def test_changed_agreement_invalidates_even_without_version_bump(self):
        self.accept()
        self.api.agreement = agreement_from(TEXT + "New terms.\n", "8" * 40, REPO["full_name"])
        self.service(name="push").process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")
        self.assertIn("8" * 40, self.api.pr["body"])

    def test_schedule_preserves_only_verified_record(self):
        self.accept()
        self.service(name="schedule").process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "success")

    def test_checked_box_without_record_is_reset_by_schedule(self):
        self.prepare()
        self.tick()
        self.service(name="schedule").process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")
        self.assertNotIn("- [x]", self.api.pr["body"])

    def test_uncheck_before_merge_revokes_pending_acceptance(self):
        self.accept()
        context = self.ledger.state(7)["context"]
        self.api.pr["body"] = replace_block(self.api.pr["body"], block(context))
        self.service({"action": "edited"}).process(7)
        self.assertIsNone(self.ledger.state(7)["acceptance"])

    def test_corrupted_evidence_never_passes(self):
        self.accept()
        path = self.ledger.state(7)["acceptance"]["path"]
        self.ledger.records[path]["actor"]["id"] = 99
        with self.assertRaises(Blocked):
            self.service(name="schedule").process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")

    def test_storage_failure_never_publishes_success(self):
        self.prepare()
        self.ledger.fail = True
        with self.assertRaises(ApiError):
            self.service(self.tick()).process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "failure")

    def test_owner_only_change_is_exempt(self):
        self.api.pr["user"]["id"] = 1
        self.api.commits = [commit(1)]
        self.service().process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "success")
        self.assertFalse(self.ledger.records)

    def test_owner_cannot_bypass_another_commit_author(self):
        self.api.pr["user"]["id"] = 1
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_coauthor_trailer_requires_separate_review(self):
        self.api.commits = [commit(message="Translate\n\nCo-authored-by: Other <other@example.test>")]
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_unlinked_author_requires_review(self):
        self.api.commits[0]["author"] = None
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_community_cannot_change_workflows(self):
        self.api.compare["files"][0]["filename"] = ".github/workflows/injected.yml"
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_renaming_protected_file_into_translation_does_not_pass(self):
        self.api.compare["files"][0]["previous_filename"] = "LICENSE"
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_incomplete_paginated_file_list_fails(self):
        self.api.pr["changed_files"] = 2
        with self.assertRaisesRegex(Blocked, "complete contribution file list"):
            self.service().process(7)

    def test_complete_language_retains_every_file_across_pages(self):
        for count in (180, 325):
            with self.subTest(files=count):
                self.setUp()
                self.api.files = [
                    {"filename": f"translations/de/section_{i}_de.arb", "status": "added", "sha": "e" * 40}
                    for i in range(count)
                ]
                self.api.compare["files"] = self.api.files[:300]
                self.api.pr["changed_files"] = count
                self.accept()
                record = next(iter(self.ledger.records.values()))
                self.assertEqual(self.api.checks[-1]["conclusion"], "success")
                self.assertEqual(len(record["context"]["files"]), count)
                self.assertEqual(
                    [item["file"]["filename"] for item in record["snapshot"]],
                    [item["filename"] for item in self.api.files],
                )
                self.assertTrue(all(base64.b64decode(item["after"]["base64"]) == b'{"hello":"Hallo"}'
                                    for item in record["snapshot"]))
                self.assertIn(("GET", f"/repos/owner/localization/pulls/7/files?per_page=100&page={(count + 99) // 100}"),
                              self.api.calls)

    def test_duplicate_files_cannot_hide_an_incomplete_list(self):
        self.api.pr["changed_files"] = 2
        self.api.files *= 2
        with self.assertRaisesRegex(Blocked, "complete contribution file list"):
            self.service().process(7)
        self.assertFalse(self.ledger.states)

    def test_github_file_limit_is_checked_before_fetching_files(self):
        self.api.pr["changed_files"] = MAX_FILES + 1
        with self.assertRaisesRegex(Blocked, "3,000 changed files"):
            self.service().process(7)
        self.assertFalse(any("/files" in path for _, path in self.api.calls))

    def test_head_or_base_change_during_pagination_cannot_issue_declaration(self):
        for ref in ("head", "base"):
            with self.subTest(ref=ref):
                self.setUp()
                original_get = self.api.get

                def get(path):
                    result = original_get(path)
                    if "/pulls/7/files?" in path:
                        self.api.pr[ref]["sha"] = "9" * 40
                    return result

                self.api.get = get
                with self.assertRaisesRegex(Blocked, "PR changed while"):
                    self.service().process(7)
                self.assertFalse(self.ledger.states)
                self.assertFalse(any(method == "PATCH" for method, _ in self.api.calls))

    def test_snapshot_size_limits_still_block_acceptance(self):
        for limit in ("MAX_BLOB_BYTES", "MAX_SNAPSHOT_BYTES"):
            with self.subTest(limit=limit):
                self.setUp()
                self.prepare()
                with patch("tools.contributor_acceptance." + limit, 1):
                    with self.assertRaisesRegex(Blocked, "evidence size limit"):
                        self.service(self.tick()).process(7)
                self.assertFalse(self.ledger.records)

    def test_pr_body_is_never_evaluated(self):
        self.api.pr["body"] = "$(touch /tmp/never-run) `arbitrary code`"
        self.prepare()
        self.assertTrue(self.api.pr["body"].startswith("$(touch /tmp/never-run)"))

    def test_duplicate_markers_fail_instead_of_rewriting_other_text(self):
        self.api.pr["body"] = START + "\n" + END + "\n" + START + END
        with self.assertRaises(Blocked):
            self.service().process(7)

    def test_merge_records_owner_acceptance(self):
        self.accept()
        self.api.pr.update(state="closed", merged=True, merge_commit_sha="7" * 40,
                           merged_at="2026-09-17T13:00:00Z", merged_by={"id": 1})
        self.service({"action": "closed", "sender": {"id": 1}}).process(7)
        outcome = list(self.ledger.records.values())[-1]
        self.assertTrue(outcome["covered"])
        self.assertTrue(outcome["matches_merge"])
        self.assertEqual(outcome["merge_commit"], "7" * 40)

    def test_merge_by_other_account_is_flagged(self):
        self.accept()
        self.api.pr.update(state="closed", merged=True, merge_commit_sha="7" * 40, merged_by={"id": 3})
        with self.assertRaises(Blocked):
            self.service({"action": "closed", "sender": {"id": 3}}).process(7)

    def test_merge_with_different_content_is_flagged(self):
        self.accept()
        self.api.merge_sha = "8" * 40
        self.api.pr.update(state="closed", merged=True, merge_commit_sha="7" * 40, merged_by={"id": 1})
        with self.assertRaises(Blocked):
            self.service({"action": "closed", "sender": {"id": 1}}).process(7)
        self.assertFalse(list(self.ledger.records.values())[-1]["matches_merge"])

    def test_unchecked_declaration_at_merge_is_flagged(self):
        self.accept()
        self.api.pr["body"] = self.api.pr["body"].replace("- [x]", "- [ ]")
        self.api.pr.update(state="closed", merged=True, merge_commit_sha="7" * 40, merged_by={"id": 1})
        with self.assertRaises(Blocked):
            self.service({"action": "closed", "sender": {"id": 1}}).process(7)
        self.assertFalse(list(self.ledger.records.values())[-1]["covered"])

    def test_crlf_checkbox_is_accepted_and_original_declaration_retained(self):
        self.prepare()
        self.api.pr["body"] = self.api.pr["body"].replace("\n", "\r\n")
        before = self.api.pr["body"]
        self.api.pr["body"] = before.replace("- [ ]", "- [x]")
        event = {"action": "edited", "sender": {"id": 2, "login": "translator", "type": "User"},
                 "pull_request": copy.deepcopy(self.api.pr), "changes": {"body": {"from": before}}}
        self.service(event).process(7)
        self.assertEqual(self.api.checks[-1]["conclusion"], "success")
        self.assertIn("\r\n", next(iter(self.ledger.records.values()))["declaration"])

    def test_symlink_snapshot_is_rejected(self):
        self.prepare()
        self.api.file_mode = "120000"
        with self.assertRaises(Blocked):
            self.service(self.tick()).process(7)
        self.assertFalse(self.ledger.records)

    def test_body_write_does_not_overwrite_a_known_concurrent_edit(self):
        pr = copy.deepcopy(self.api.pr)
        self.api.pr["body"] = "New translator text"
        with self.assertRaises(Blocked):
            self.service().update_body(pr, "Bot replacement")
        self.assertEqual(self.api.pr["body"], "New translator text")


class FormatTests(unittest.TestCase):
    def test_body_outside_managed_block_is_preserved(self):
        self.assertEqual(replace_block("Before\n" + START + "old" + END + "\nAfter", "new"),
                         "Before\nnew\nAfter")

    def test_missing_version_is_not_accepted(self):
        with self.assertRaises(Blocked):
            agreement_from("No version", "a" * 40, REPO["full_name"])

    def test_multiple_version_lines_are_rejected(self):
        with self.assertRaises(Blocked):
            agreement_from(TEXT + "Version 2.0\n", "a" * 40, REPO["full_name"])

    def test_ledger_rejects_default_records_branch(self):
        with self.assertRaises(Blocked):
            Ledger(None, {**REPO, "default_branch": RECORDS_BRANCH})


class GitStorageAPI:
    def __init__(self):
        self.head = "initial"
        self.trees = {"initial": {}}
        self.next_tree = 0
        self.commits = {}
        self.conflict_once = False
        self.ref_writes = 0
        self.calls = []
        self.create_conflict = False
        self.create_error = None

    def get(self, path):
        self.calls.append(("GET", path, None))
        assert path.startswith("/repos/owner/localization/")
        if "/contents/" in path:
            filename = path.split("/contents/")[1].split("?")[0]
            assert path.endswith("?ref=" + RECORDS_BRANCH)
            value = self.trees[self.head].get(filename)
            if value is None:
                raise ApiError(404, path)
            return {"encoding": "base64", "type": "file",
                    "content": base64.b64encode(value.encode()).decode()}
        if path.endswith("/git/ref/heads/" + RECORDS_BRANCH):
            if self.head is None:
                raise ApiError(404, path)
            return {"object": {"sha": self.head}}
        if "/git/commits/" in path:
            return {"tree": {"sha": path.rsplit("/", 1)[1]}}
        raise AssertionError(path)

    def request(self, method, path, data):
        self.calls.append((method, path, copy.deepcopy(data)))
        assert path.startswith("/repos/owner/localization/")
        if path.endswith("/git/refs"):
            assert data["ref"] == "refs/heads/" + RECORDS_BRANCH
            if self.create_error:
                raise ApiError(self.create_error, path)
            if self.create_conflict:
                self.head = "initial"
                raise ApiError(422, path)
            self.head = data["sha"]
            return {}
        if path.endswith("/git/trees"):
            self.next_tree += 1
            key = "tree" + str(self.next_tree)
            self.trees[key] = {**self.trees.get(data.get("base_tree"), {}),
                               **{item["path"]: item["content"] for item in data["tree"]}}
            return {"sha": key}
        if path.endswith("/git/commits"):
            key = "commit" + str(self.next_tree)
            self.trees[key] = copy.deepcopy(self.trees[data["tree"]])
            self.commits[key] = data["parents"][0] if data["parents"] else None
            return {"sha": key}
        if path.endswith("/git/refs/heads/" + RECORDS_BRANCH):
            self.ref_writes += 1
            self.assert_no_force(data)
            if self.conflict_once:
                self.conflict_once = False
                self.trees["external"] = {**self.trees[self.head], "unrelated.json": '{"retained":true}'}
                self.head = "external"
                raise ApiError(422, path)
            if self.commits[data["sha"]] != self.head:
                raise ApiError(422, path)
            self.head = data["sha"]
            return {}
        raise AssertionError((method, path))

    @staticmethod
    def assert_no_force(data):
        if data.get("force") is not False:
            raise AssertionError("Evidence history must not be force pushed")


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.api = GitStorageAPI()
        self.ledger = Ledger(self.api, REPO)

    def test_records_use_source_repository_for_either_visibility(self):
        for private in (True, False):
            with self.subTest(private=private):
                ledger = Ledger(self.api, {**REPO, "private": private})
                self.assertEqual(ledger.prefix, "/repos/owner/localization")
                self.assertEqual(ledger.branch, RECORDS_BRANCH)
        self.assertTrue(all(method == "GET" for method, _, _ in self.api.calls))

    def test_missing_records_branch_is_initialized_without_source_history(self):
        self.api.head = None
        ledger = Ledger(self.api, REPO)
        head = self.api.head
        self.assertIsNone(self.api.commits[head])
        self.assertEqual(set(self.api.trees[head]), {"README.md"})
        self.assertIn("same visibility", self.api.trees[head]["README.md"])
        ledger.save(7, {"accepted": False})
        self.assertEqual(ledger.state(7), {"accepted": False})

    def test_concurrent_branch_creation_preserves_existing_branch(self):
        self.api.head = None
        self.api.create_conflict = True
        Ledger(self.api, REPO)
        self.assertEqual(self.api.head, "initial")
        self.assertEqual(self.api.ref_writes, 0)

    def test_branch_creation_permission_failure_is_not_ignored(self):
        self.api.head = None
        self.api.create_error = 403
        with self.assertRaises(ApiError):
            Ledger(self.api, REPO)
        self.assertIsNone(self.api.head)

    def test_branch_creation_validation_failure_needs_existing_branch(self):
        self.api.head = None
        self.api.create_error = 422
        with self.assertRaises(ApiError):
            Ledger(self.api, REPO)
        self.assertIsNone(self.api.head)

    def test_state_and_evidence_are_published_in_one_commit(self):
        self.ledger.save(7, {"accepted": True}, ("records/test.json", {"declaration": "accepted"}))
        self.assertEqual(self.api.ref_writes, 1)
        self.assertEqual(self.ledger.state(7), {"accepted": True})
        self.assertEqual(self.ledger.read("records/test.json"), {"declaration": "accepted"})

    def test_large_record_is_read_through_blob_api(self):
        evidence = {"snapshot": "a" * 1_100_000}
        original_get = self.api.get

        def get(path):
            if "/contents/records/large.json" in path:
                return {"type": "file", "encoding": "none", "content": "", "sha": "f" * 40}
            if path.endswith("/git/blobs/" + "f" * 40):
                return {"encoding": "base64", "content": base64.b64encode(canonical(evidence).encode()).decode()}
            return original_get(path)

        self.api.get = get
        self.assertEqual(self.ledger.read("records/large.json"), evidence)

    def test_conflicting_write_preserves_other_repository_changes(self):
        self.api.conflict_once = True
        self.ledger.save(7, {"accepted": True}, ("records/test.json", {"declaration": "accepted"}))
        self.assertEqual(self.api.ref_writes, 2)
        self.assertEqual(self.ledger.read("unrelated.json"), {"retained": True})
        self.assertEqual(self.ledger.state(7), {"accepted": True})

    def test_old_evidence_cannot_be_overwritten(self):
        self.ledger.save(7, {}, ("records/test.json", {"declaration": "original"}))
        with self.assertRaises(Blocked):
            self.ledger.save(7, {}, ("records/test.json", {"declaration": "replacement"}))
        self.assertEqual(self.ledger.read("records/test.json"), {"declaration": "original"})

    def test_identical_retry_does_not_add_a_commit(self):
        self.ledger.save(7, {"accepted": True}, ("records/test.json", {"declaration": "accepted"}))
        self.ledger.save(7, {"accepted": True}, ("records/test.json", {"declaration": "accepted"}))
        self.assertEqual(self.api.ref_writes, 1)


if __name__ == "__main__":
    unittest.main()
