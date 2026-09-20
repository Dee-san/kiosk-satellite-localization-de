#!/usr/bin/env python3
"""Record contributor acceptance without executing pull request code."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


CHECK = "contributor-acceptance"
RECORD_CHECK = "contributor-acceptance-record"
START = "<!-- ks-contributor-acceptance:start -->"
END = "<!-- ks-contributor-acceptance:end -->"
AGREEMENT = "docs/CONTRIBUTOR-AGREEMENT.md"
RECORDS_BRANCH = "contributor-records"
# GitHub's paginated PR files endpoint can return up to 3,000 files.
MAX_FILES = 3000
MAX_COMMITS = 100
MAX_SNAPSHOT_BYTES = 3_000_000
MAX_BLOB_BYTES = 500_000
TRANSLATION_PATH = re.compile(r"translations/[A-Za-z][A-Za-z0-9_-]*/[A-Za-z][A-Za-z0-9_]*\.arb\Z")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Blocked(Exception):
    """A contribution or configuration cannot pass automatically."""


class ApiError(Exception):
    def __init__(self, status, path):
        super().__init__(f"GitHub API returned HTTP {status} for {path.split('?')[0]}")
        self.status = status


class GitHub:
    def __init__(self, token):
        if not token:
            raise Blocked("A required workflow credential is missing.")
        self.token = token

    def request(self, method, path, data=None):
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("Only GitHub API paths are allowed.")
        request = Request(
            "https://api.github.com" + path,
            data=None if data is None else canonical(data).encode(),
            headers={
                "Authorization": "Bearer " + self.token,
                "Accept": ("application/vnd.github.object+json" if "/contents/" in path
                           else "application/vnd.github+json"),
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Kiosk-Satellite-Contributor-Acceptance",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=45) as response:
                body = response.read()
                return json.loads(body) if body else None
        except HTTPError as error:
            # Do not print response bodies or credentials.
            raise ApiError(error.code, path) from None

    def get(self, path):
        return self.request("GET", path)

    def pages(self, path):
        result = []
        for page in range(1, 101):
            separator = "&" if "?" in path else "?"
            batch = self.get(f"{path}{separator}per_page=100&page={page}")
            if not isinstance(batch, list):
                raise Blocked("Unexpected paginated GitHub response.")
            result.extend(batch)
            if len(batch) < 100:
                return result
        raise Blocked("Too many results. Split the contribution into smaller PRs.")


class Ledger:
    """Store evidence on a dedicated branch of the localization repository."""

    def __init__(self, api, source):
        self.api = api
        self.prefix = "/repos/" + source["full_name"]
        self.branch = RECORDS_BRANCH
        if source["default_branch"] == self.branch:
            raise Blocked("The records branch must not be the default branch.")
        self.source_id = source["id"]
        self.ensure_branch()

    def ensure_branch(self):
        ref_path = self.prefix + "/git/ref/heads/" + self.branch
        try:
            self.api.get(ref_path)
            return
        except ApiError as error:
            if error.status != 404:
                raise
        # An independent root keeps records out of translation and workflow history.
        tree = self.api.request("POST", self.prefix + "/git/trees", {
            "tree": [{"path": "README.md", "mode": "100644", "type": "blob",
                      "content": "# Contributor acceptance records\n\n"
                      "This branch contains automated acceptance records for localization PRs.\n"
                      "It has the same visibility as this repository. Do not add private information.\n"
                      "Do not merge this branch into the default branch or edit records manually.\n"}],
        })
        commit = self.api.request("POST", self.prefix + "/git/commits", {
            "message": "Initialize contributor acceptance records", "tree": tree["sha"], "parents": [],
        })
        try:
            self.api.request("POST", self.prefix + "/git/refs", {
                "ref": "refs/heads/" + self.branch, "sha": commit["sha"],
            })
        except ApiError as error:
            if error.status not in (409, 422):
                raise
            # A concurrent initializer may have created the branch. Never replace it.
            self.api.get(ref_path)

    def read(self, path):
        try:
            value = self.api.get(self.prefix + "/contents/" + quote(path, safe="/")
                                 + "?" + urlencode({"ref": self.branch}))
        except ApiError as error:
            if error.status == 404:
                return None
            raise
        if value.get("type") != "file":
            raise Blocked("Unexpected acceptance record format.")
        # The Contents API omits inline content for files larger than 1 MB.
        if value.get("encoding") == "none":
            value = self.api.get(self.prefix + "/git/blobs/" + value["sha"])
        if value.get("encoding") != "base64":
            raise Blocked("Unexpected acceptance record encoding.")
        return json.loads(base64.b64decode(value["content"]))

    def state_path(self, number):
        return f"state/{self.source_id}/{number}.json"

    def state(self, number):
        return self.read(self.state_path(number))

    def save(self, number, state, record=None):
        changes = {self.state_path(number): state}
        if record:
            path, content = record
            existing = self.read(path)
            if existing is not None and existing != content:
                raise Blocked("Refusing to overwrite an existing acceptance record.")
            if existing is None:
                changes[path] = content
        if all(self.read(path) == value for path, value in changes.items()):
            return
        for attempt in range(3):
            ref_path = self.prefix + "/git/ref/heads/" + quote(self.branch, safe="")
            parent = self.api.get(ref_path)["object"]["sha"]
            parent_commit = self.api.get(self.prefix + "/git/commits/" + parent)
            tree = self.api.request("POST", self.prefix + "/git/trees", {
                "base_tree": parent_commit["tree"]["sha"],
                "tree": [{"path": path, "mode": "100644", "type": "blob",
                          "content": canonical(value) + "\n"} for path, value in changes.items()],
            })
            commit = self.api.request("POST", self.prefix + "/git/commits", {
                "message": f"Record contributor acceptance state for PR #{number}",
                "tree": tree["sha"], "parents": [parent],
            })
            try:
                self.api.request("PATCH", self.prefix + "/git/refs/heads/" + quote(self.branch, safe=""),
                                 {"sha": commit["sha"], "force": False})
                return
            except ApiError as error:
                if error.status not in (409, 422) or attempt == 2:
                    raise


def agreement_from(text, commit, repository):
    versions = re.findall(r"^Version ([0-9]+(?:\.[0-9]+)*)\s*$", text, re.MULTILINE)
    if len(versions) != 1:
        raise Blocked("The contributor agreement must have one explicit version line.")
    return {"version": versions[0], "sha256": digest(text), "text": text,
            "commit": commit, "url": f"https://github.com/{repository}/blob/{commit}/{AGREEMENT}"}


def block(context, accepted=False):
    mark = "x" if accepted else " "
    agreement = context["agreement"]
    return (
        START + "\n"
        "### Contributor agreement acceptance\n\n"
        f"Read [Contributor Agreement version {agreement['version']}]({agreement['url']}). "
        "Use your own GitHub account to check the box below.\n\n"
        f"- [{mark}] I have read and accept the Contributor Agreement linked above for my "
        f"contribution in PR #{context['number']} at commit `{context['head']}`. "
        "I retain copyright ownership and grant Xavier Larrea exclusive worldwide usage rights "
        "as specified in that agreement. I confirm that I am the sole author of this contribution "
        "and have authority to grant those rights. I intend this action to be my electronic signature.\n\n"
        f"Acceptance reference: `{context['id']}`. Changes require renewed acceptance.\n"
        + END
    )


def extract_block(body):
    body = body or ""
    if body.count(START) != 1 or body.count(END) != 1:
        return None
    start, end = body.index(START), body.index(END) + len(END)
    return body[start:end] if start < end else None


def normalized_block(body):
    value = extract_block(body)
    return value.replace("\r\n", "\n").replace("- [X]", "- [x]") if value else value


def replace_block(body, replacement):
    body = body or ""
    existing = extract_block(body)
    if existing is not None:
        return body.replace(existing, replacement, 1)
    if START in body or END in body:
        raise Blocked("Restore the acceptance section markers or ask the maintainer to repair them.")
    return body.rstrip() + "\n\n" + replacement + "\n"


def accepted_event(event_name, event, pr, context, state):
    """Only an authenticated author changing the issued checkbox counts."""
    previous = event.get("changes", {}).get("body", {}).get("from")
    event_pr = event.get("pull_request", {})
    actor = event.get("sender", {})
    return all((
        event_name == "pull_request_target", event.get("action") == "edited",
        actor.get("type") == "User", actor.get("id") == pr["user"]["id"],
        event_pr.get("number") == pr["number"],
        event_pr.get("head", {}).get("sha") == context["head"],
        event_pr.get("body") == pr.get("body"),
        event_pr.get("updated_at") == pr.get("updated_at"),
        state is not None and state.get("context") == context,
        normalized_block(previous) == block(context, False),
        normalized_block(event_pr.get("body")) == block(context, True),
    ))


def sole_author(pr, commits):
    if not commits or len(commits) != pr["commits"]:
        raise Blocked("The complete commit authorship could not be verified.")
    author_id = pr["user"]["id"]
    for commit in commits:
        if (commit.get("author") or {}).get("id") != author_id:
            raise Blocked("Automatic acceptance supports one author per PR. Split work by author or arrange separate rights review.")
        if re.search(r"(?im)^\s*co-authored-by\s*:", commit["commit"]["message"]):
            raise Blocked("This PR declares another author and needs separate rights review.")


def make_context(pr, agreement, comparison, files):
    if pr["changed_files"] > MAX_FILES:
        raise Blocked(f"GitHub can list at most {MAX_FILES:,} changed files per PR. This contribution needs separate review.")
    if len(files) != pr["changed_files"] or len({file["filename"] for file in files}) != len(files):
        raise Blocked("The complete contribution file list could not be verified. Recheck the current PR revision.")
    manifest = [{key: file.get(key) for key in ("filename", "previous_filename", "status", "sha")}
                for file in files]
    context = {
        "schema": 1, "number": pr["number"], "author_id": pr["user"]["id"],
        "head": pr["head"]["sha"], "merge_base": comparison["merge_base_commit"]["sha"],
        "files": manifest,
        "disclosures_sha256": digest((pr.get("body") or "").replace(
            extract_block(pr.get("body")) or "\0", ""
        ).replace("\r\n", "\n").strip()),
        "agreement": {key: agreement[key] for key in ("version", "commit", "sha256", "url")},
    }
    context["id"] = digest(canonical(context))
    return context


class Acceptance:
    def __init__(self, api, ledger, repository, event_name, event, run):
        self.api, self.ledger = api, ledger
        self.repository, self.event_name, self.event, self.run = repository, event_name, event, run
        self.prefix = "/repos/" + repository["full_name"]
        self.agreement = None

    def load_agreement(self):
        if self.agreement is None:
            commits = self.api.get(self.prefix + "/commits?" + urlencode({
                "path": AGREEMENT, "sha": self.repository["default_branch"], "per_page": 1}))
            if not commits:
                raise Blocked("The default branch has no contributor agreement.")
            revision = commits[0]["sha"]
            file = self.api.get(self.prefix + "/contents/" + AGREEMENT + "?ref=" + revision)
            if file.get("encoding") != "base64":
                raise Blocked("The agreement could not be read in full.")
            text = base64.b64decode(file["content"]).decode("utf-8")
            self.agreement = agreement_from(text, revision, self.repository["full_name"])
        return self.agreement

    def check(self, pr, conclusion, summary):
        # Publish the merge requirement as a commit status. API-created checks
        # using GITHUB_TOKEN can appear green without satisfying the Actions
        # job requirement. Keep the detailed evidence check under its own name.
        status = {"context": CHECK, "state": conclusion, "description": summary[:140],
                  "target_url": f"https://github.com/{self.repository['full_name']}/actions/runs/{self.run['id']}"}
        status_path = self.prefix + "/statuses/" + pr["head"]["sha"]
        if conclusion != "success":
            self.api.request("POST", status_path, status)
        external_id = f"ks-acceptance:{self.repository['id']}:{pr['number']}"
        path = self.prefix + "/commits/" + pr["head"]["sha"] + "/check-runs?" + urlencode({
            "check_name": RECORD_CHECK, "filter": "latest", "per_page": 100})
        runs = self.api.get(path)["check_runs"]
        # Rename the legacy check so GitHub does not require both a check run
        # and a commit status with the same name on existing PR revisions.
        legacy_path = self.prefix + "/commits/" + pr["head"]["sha"] + "/check-runs?" + urlencode({
            "check_name": CHECK, "filter": "latest", "per_page": 100})
        legacy = self.api.get(legacy_path)["check_runs"]
        for item in legacy:
            if (item.get("external_id") == external_id
                    and item.get("app", {}).get("slug") == "github-actions"):
                self.api.request("PATCH", self.prefix + f"/check-runs/{item['id']}", {"name": RECORD_CHECK})
                runs.append(item)
        existing = next((item for item in runs if item.get("external_id") == external_id
                         and item.get("app", {}).get("slug") == "github-actions"), None)
        data = {"name": RECORD_CHECK, "external_id": external_id, "status": "completed",
                "conclusion": conclusion, "output": {"title": RECORD_CHECK, "summary": summary}}
        if existing:
            self.api.request("PATCH", self.prefix + f"/check-runs/{existing['id']}", data)
        else:
            data["head_sha"] = pr["head"]["sha"]
            self.api.request("POST", self.prefix + "/check-runs", data)
        if conclusion == "success":
            self.api.request("POST", status_path, status)

    def current(self, pr):
        latest = self.api.get(self.prefix + f"/pulls/{pr['number']}")
        if (latest["head"]["sha"] != pr["head"]["sha"]
                or latest["base"]["sha"] != pr["base"]["sha"]
                or latest.get("body") != pr.get("body") or latest["state"] != pr["state"]):
            raise Blocked("The PR changed while it was checked. Recheck acceptance for the current revision.")
        return latest

    def update_body(self, pr, body):
        if body != pr.get("body"):
            self.current(pr)
            self.api.request("PATCH", self.prefix + f"/pulls/{pr['number']}", {"body": body})
            pr["body"] = body

    def snapshot(self, pr, context):
        trees = {}
        for key, revision in (("before", context["merge_base"]), ("after", context["head"])):
            response = self.api.get(self.prefix + "/git/trees/" + revision + "?recursive=1")
            if response.get("truncated"):
                raise Blocked("The contribution tree could not be retained completely.")
            trees[key] = {item["path"]: item for item in response["tree"]}
        files, total = [], 0
        for item in context["files"]:
            versions = {}
            if item["status"] != "removed":
                versions["after"] = item["filename"]
            if item["status"] != "added":
                versions["before"] = item["previous_filename"] or item["filename"]
            captured = {"file": item}
            for name, path in versions.items():
                entry = trees[name].get(path)
                if not entry or entry["type"] != "blob" or entry["mode"] != "100644":
                    raise Blocked("Translations must be ordinary nonexecutable files. Symlinks are not accepted.")
                if entry.get("size", 0) > MAX_BLOB_BYTES:
                    raise Blocked("Contribution files exceed the evidence size limit. Submit a smaller PR.")
                if name == "after" and entry["sha"] != item["sha"]:
                    raise Blocked("The file manifest does not match the contribution tree.")
                value = self.api.get(self.prefix + "/git/blobs/" + entry["sha"])
                if value.get("encoding") != "base64":
                    raise Blocked("A contribution file could not be retained in full.")
                raw = base64.b64decode(value["content"])
                total += len(raw)
                if len(raw) > MAX_BLOB_BYTES or total > MAX_SNAPSHOT_BYTES:
                    raise Blocked("Contribution files exceed the evidence size limit. Submit a smaller PR.")
                captured[name] = {"sha": value["sha"], "sha256": hashlib.sha256(raw).hexdigest(),
                                  "base64": base64.b64encode(raw).decode()}
            files.append(captured)
        self.current(pr)
        return files

    def record_acceptance(self, pr, context, state):
        agreement = self.load_agreement()
        record = {
            "schema": 1, "kind": "contributor_acceptance", "repository": self.repository["full_name"],
            "repository_id": self.repository["id"], "context": context,
            "agreement_text": agreement["text"], "declaration": extract_block(pr["body"]),
            "pr_description": pr["body"],
            "actor": {key: self.event["sender"][key] for key in ("id", "login", "type")},
            "event_action": self.event["action"],
            "event_updated_at": self.event["pull_request"]["updated_at"],
            "previous_declaration": extract_block(self.event["changes"]["body"]["from"]),
            "run": self.run, "snapshot": self.snapshot(pr, context),
        }
        path = (f"records/{self.repository['id']}/{pr['number']}/{context['id']}/"
                f"{self.run['id']}-{self.run['attempt']}.json")
        state["acceptance"] = {"path": path, "sha256": digest(canonical(record))}
        self.ledger.save(pr["number"], state, (path, record))

    def verified_record(self, state):
        pointer = state.get("acceptance")
        if not pointer:
            return False
        record = self.ledger.read(pointer["path"])
        if (record is None or digest(canonical(record)) != pointer["sha256"]
                or record["context"] != state["context"]
                or record["actor"]["id"] != state["context"]["author_id"]):
            raise Blocked("The retained acceptance record could not be verified.")
        return True

    def closed(self, pr):
        state = self.ledger.state(pr["number"])
        if not state:
            return
        covered = (state["context"]["head"] == pr["head"]["sha"]
                   and normalized_block(pr.get("body")) == block(state["context"], True)
                   and self.verified_record(state))
        matches_merge = False
        if pr.get("merged") and covered:
            tree = self.api.get(self.prefix + "/git/trees/" + pr["merge_commit_sha"] + "?recursive=1")
            if tree.get("truncated"):
                raise Blocked("The merged files could not be verified completely.")
            paths = {item["path"]: item for item in tree["tree"]}
            evidence = self.ledger.read(state["acceptance"]["path"])
            matches_merge = True
            for file in evidence["snapshot"]:
                path = file["file"]["filename"]
                if "after" in file:
                    entry = paths.get(path, {})
                    matches_merge &= entry.get("sha") == file["after"]["sha"] and entry.get("mode") == "100644"
                else:
                    matches_merge &= path not in paths
                previous = file["file"]["previous_filename"]
                if previous and previous != path:
                    matches_merge &= previous not in paths
        record = {"kind": "pr_closed", "number": pr["number"], "head": pr["head"]["sha"],
                  "merged": bool(pr.get("merged")), "merge_commit": pr.get("merge_commit_sha"),
                  "closed_at": pr.get("closed_at"), "merged_at": pr.get("merged_at"),
                  "actor_id": self.event.get("sender", {}).get("id"),
                  "merged_by": (pr.get("merged_by") or {}).get("id"), "matches_merge": matches_merge,
                  "covered": covered, "acceptance": state.get("acceptance"), "run": self.run}
        path = f"outcomes/{self.repository['id']}/{pr['number']}/{self.run['id']}-{self.run['attempt']}.json"
        self.ledger.save(pr["number"], state, (path, record))
        if pr.get("merged") and (not covered or not matches_merge
                                 or record["merged_by"] != self.repository["owner"]["id"]):
            raise Blocked("A PR was merged without recorded contributor and owner acceptance. Review the outcome record on contributor-records.")

    def process(self, number):
        pr = self.api.get(self.prefix + f"/pulls/{number}")
        try:
            if pr["state"] != "open":
                self.closed(pr)
                return
            self.check(pr, "failure", "Acceptance is being verified. A retained record is required before merging.")
            if pr["base"]["ref"] != self.repository["default_branch"]:
                raise Blocked("Translation PRs must target the default branch.")
            if pr["commits"] > MAX_COMMITS:
                raise Blocked("Submit fewer than 101 commits per PR.")
            commits = self.api.pages(self.prefix + f"/pulls/{number}/commits")
            sole_author(pr, commits)
            if pr["user"]["id"] == self.repository["owner"]["id"]:
                self.current(pr)
                self.check(pr, "success", "This PR contains only the repository owner's commits. No contributor license is needed.")
                return
            agreement = self.load_agreement()
            if pr["changed_files"] > MAX_FILES:
                raise Blocked(f"GitHub can list at most {MAX_FILES:,} changed files per PR. This contribution needs separate review.")
            comparison = self.api.get(self.prefix + f"/compare/{pr['base']['sha']}...{pr['head']['sha']}")
            # The comparison supplies the pinned merge base, but its file list
            # stops at 300 entries. Retrieve every PR file page separately.
            files = self.api.pages(self.prefix + f"/pulls/{number}/files")
            self.current(pr)
            context = make_context(pr, agreement, comparison, files)
            if not context["files"] or any(not TRANSLATION_PATH.fullmatch(file["filename"])
                    or (file["previous_filename"] and not TRANSLATION_PATH.fullmatch(file["previous_filename"]))
                    for file in context["files"]):
                raise Blocked("Community translation PRs may change only ARB files under translations/<locale>/. Other changes need maintainer review.")
            self.current(pr)
            state = self.ledger.state(number)
            if state is None or state.get("context") != context:
                state = {"context": context, "acceptance": None}
                self.ledger.save(number, state)
                self.update_body(pr, replace_block(pr.get("body"), block(context)))
            elif accepted_event(self.event_name, self.event, pr, context, state):
                self.record_acceptance(pr, context, state)
            elif normalized_block(pr.get("body")) != block(context, True):
                state["acceptance"] = None
                self.ledger.save(number, state)
                self.update_body(pr, replace_block(pr.get("body"), block(context)))
            if self.verified_record(state) and normalized_block(pr.get("body")) == block(context, True):
                self.current(pr)
                self.check(pr, "success", f"The PR author accepted agreement {agreement['version']} for commit `{context['head']}`. Evidence is retained on the contributor-records branch. Linguistic and rights review remain the maintainer's responsibility.")
            else:
                self.update_body(pr, replace_block(pr.get("body"), block(context)))
                self.check(pr, "failure", "Read the pinned agreement and check the acceptance box in the PR description using your own account. This check supports one author per PR.")
        except Blocked as error:
            self.check(pr, "failure", str(error))
            raise


def main():
    repository_name = os.environ["GITHUB_REPOSITORY"]
    api = GitHub(os.environ.get("GITHUB_TOKEN"))
    repository = api.get("/repos/" + repository_name)
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    event_name = os.environ["GITHUB_EVENT_NAME"]
    if event_name not in {"pull_request_target", "push", "schedule", "workflow_dispatch"}:
        raise Blocked("Unsupported workflow event.")
    run = {"id": os.environ["GITHUB_RUN_ID"], "attempt": os.environ["GITHUB_RUN_ATTEMPT"],
           "workflow_sha": os.environ["GITHUB_SHA"]}
    service = Acceptance(api, None, repository, event_name, event, run)
    if event_name == "pull_request_target":
        numbers = [event["pull_request"]["number"]]
    elif event_name == "workflow_dispatch" and event.get("inputs", {}).get("pr_number"):
        numbers = [int(event["inputs"]["pr_number"])]
    else:
        numbers = [pr["number"] for pr in api.pages(service.prefix + "/pulls?state=open")]
    # Invalidate cached successes before checking the records branch.
    # A missing credential or unavailable ledger must not leave a green check.
    for number in numbers:
        pr = api.get(service.prefix + f"/pulls/{number}")
        if pr["state"] == "open":
            service.check(pr, "failure", "Acceptance verification is in progress. Evidence storage must be available.")
    service.ledger = Ledger(api, repository)
    failures = []
    for number in numbers:
        try:
            service.process(number)
        except (Blocked, ApiError) as error:
            failures.append(number)
            print(f"PR #{number}: {error}", file=sys.stderr)
    if failures:
        raise Blocked("Acceptance is incomplete for PRs: " + ", ".join(map(str, failures)))


if __name__ == "__main__":
    try:
        main()
    except (Blocked, ApiError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
