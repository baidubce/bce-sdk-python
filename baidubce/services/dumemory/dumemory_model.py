# !/usr/bin/env python
# coding=UTF-8
#
# Copyright 2026 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
"""
DuMemory request-side model helpers.

This module provides thin, ergonomic factory functions over the pydantic models
shipped with the upstream ``hindsight_client_api`` package. The DuMemory SDK
itself accepts:

* ``hindsight_client_api`` pydantic model instances (preferred), or
* plain ``dict`` payloads (validated by hindsight pydantic models internally).

Re-exports here exist so callers do not have to import ``hindsight_client_api``
directly. If the upstream package is not installed, ``ImportError`` is raised
on first use.
"""

# All upstream models live under hindsight_client_api.models.*
# We re-export the most common request bodies and option helpers that match the
# DuMemory.md interface tables.

try:
    from hindsight_client_api.models.create_bank_request import CreateBankRequest
    from hindsight_client_api.models.bank_config_update import BankConfigUpdate
    from hindsight_client_api.models.consolidation_request import ConsolidationRequest
    from hindsight_client_api.models.memory_item import MemoryItem
    from hindsight_client_api.models.retain_request import RetainRequest
    from hindsight_client_api.models.recall_request import RecallRequest
    from hindsight_client_api.models.reflect_request import ReflectRequest
    from hindsight_client_api.models.update_document_request import UpdateDocumentRequest
    from hindsight_client_api.models.create_mental_model_request import CreateMentalModelRequest
    from hindsight_client_api.models.update_mental_model_request import UpdateMentalModelRequest
    from hindsight_client_api.models.create_directive_request import CreateDirectiveRequest
    from hindsight_client_api.models.update_directive_request import UpdateDirectiveRequest
except ImportError as _imp_err:  # pragma: no cover - surfaced only at runtime
    _IMPORT_ERROR = _imp_err

    def _missing(*_args, **_kwargs):
        raise ImportError(
            "hindsight_client_api is not installed. Install the upstream "
            "package via `pip install hindsight-client` (provides both "
            "`hindsight_client` and `hindsight_client_api`) before using "
            "the DuMemory SDK."
        ) from _IMPORT_ERROR

    CreateBankRequest = BankConfigUpdate = ConsolidationRequest = _missing
    MemoryItem = RetainRequest = RecallRequest = ReflectRequest = _missing
    UpdateDocumentRequest = _missing
    CreateMentalModelRequest = UpdateMentalModelRequest = _missing
    CreateDirectiveRequest = UpdateDirectiveRequest = _missing


# ----------------------------- factory helpers ----------------------------- #

def new_memory_item(content, **kwargs):
    """Build a hindsight ``MemoryItem`` from a plain string ``content``."""
    return MemoryItem(content=content, **kwargs)


def new_retain_request(items, **kwargs):
    """Build a hindsight ``RetainRequest`` from a list of items.

    ``items`` accepts either ``MemoryItem`` instances or dicts; dicts are
    validated by pydantic at the call site of the API.
    """
    return RetainRequest(items=list(items), **kwargs)


def new_recall_request(query, **kwargs):
    """Build a hindsight ``RecallRequest``."""
    return RecallRequest(query=query, **kwargs)


def new_reflect_request(query, **kwargs):
    """Build a hindsight ``ReflectRequest``."""
    return ReflectRequest(query=query, **kwargs)


def new_create_bank_request(**kwargs):
    """Build a hindsight ``CreateBankRequest``."""
    return CreateBankRequest(**kwargs)


def new_bank_config_update(updates):
    """Build a hindsight ``BankConfigUpdate`` from a flat dict of overrides."""
    return BankConfigUpdate(updates=updates)


def new_update_document_request(**kwargs):
    """Build a hindsight ``UpdateDocumentRequest``."""
    return UpdateDocumentRequest(**kwargs)


def new_create_mental_model_request(name, source_query, **kwargs):
    """Build a hindsight ``CreateMentalModelRequest``."""
    return CreateMentalModelRequest(
        name=name, source_query=source_query, **kwargs)


def new_update_mental_model_request(**kwargs):
    """Build a hindsight ``UpdateMentalModelRequest``."""
    return UpdateMentalModelRequest(**kwargs)


def new_create_directive_request(name, content, **kwargs):
    """Build a hindsight ``CreateDirectiveRequest``."""
    return CreateDirectiveRequest(name=name, content=content, **kwargs)


def new_update_directive_request(**kwargs):
    """Build a hindsight ``UpdateDirectiveRequest``."""
    return UpdateDirectiveRequest(**kwargs)


# -------------------- query options for list_* endpoints ------------------- #
# These are not pydantic models on the wire; they are simple containers that
# the client unpacks into the upstream API call's keyword arguments.

class _Options(object):
    """Base helper that exposes ``to_kwargs`` skipping ``None`` fields."""

    def to_kwargs(self):
        """Return non-None attributes as a kwargs-friendly dict."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class ListMemoriesOptions(_Options):
    """Query options for ``list_memories``."""

    def __init__(self, type=None, q=None, consolidation_state=None,
                 limit=None, offset=None):
        self.type = type
        self.q = q
        self.consolidation_state = consolidation_state
        self.limit = limit
        self.offset = offset


class ListDocumentsOptions(_Options):
    """Query options for ``list_documents``."""

    def __init__(self, q=None, tags=None, tags_match=None,
                 limit=None, offset=None):
        self.q = q
        self.tags = tags
        self.tags_match = tags_match
        self.limit = limit
        self.offset = offset


class ListMentalModelsOptions(_Options):
    """Query options for ``list_mental_models``."""

    def __init__(self, tags=None, tags_match=None, detail=None,
                 limit=None, offset=None):
        self.tags = tags
        self.tags_match = tags_match
        self.detail = detail
        self.limit = limit
        self.offset = offset


class ListDirectivesOptions(_Options):
    """Query options for ``list_directives``."""

    def __init__(self, tags=None, tags_match=None, active_only=None,
                 limit=None, offset=None):
        self.tags = tags
        self.tags_match = tags_match
        self.active_only = active_only
        self.limit = limit
        self.offset = offset


class ListOperationsOptions(_Options):
    """Query options for ``list_operations``."""

    def __init__(self, status=None, type=None, limit=None, offset=None,
                 exclude_parents=None):
        self.status = status
        self.type = type
        self.limit = limit
        self.offset = offset
        self.exclude_parents = exclude_parents


class ListTagsOptions(_Options):
    """Query options for ``list_tags_with_scope``."""

    def __init__(self, q=None, source=None, limit=None, offset=None):
        self.q = q
        self.source = source
        self.limit = limit
        self.offset = offset


# -------------------- entity scope for tag-scoped memory APIs ------------- #

MISSING_ENTITY_SCOPE_MESSAGE = (
    "At least one entity ID (user_id, agent_id, app_id, or run_id) is "
    "required."
)


class MissingEntityScopeError(ValueError):
    """Raised when an :class:`EntityScope` has no entity id set.

    Mirrors the Go SDK's ``ErrMissingEntityScope``. Subclassing
    :class:`ValueError` keeps backwards-compatible behavior for callers that
    only catch ``ValueError`` from bad inputs.
    """

    def __init__(self, message=None):
        """Initialize with the standard scope-missing message."""
        super(MissingEntityScopeError, self).__init__(
            message or MISSING_ENTITY_SCOPE_MESSAGE)


# Convenience alias that matches the Go SDK identifier ``ErrMissingEntityScope``.
ErrMissingEntityScope = MissingEntityScopeError


_DEFAULT_SCOPED_TAGS_MATCH = "all_strict"


class EntityScope(object):
    """Identifies the entity boundary used by the scoped memory APIs.

    At least one of ``user_id``, ``agent_id``, ``app_id`` or ``run_id`` must
    be set. Non-empty fields are converted into tag strings of the form
    ``user_id:<id>``, ``agent_id:<id>``, ``app_id:<id>`` and ``run_id:<id>``.
    The order of the resulting tags is stable and matches the Go SDK.
    """

    __slots__ = ("user_id", "agent_id", "app_id", "run_id")

    def __init__(self, user_id="", agent_id="", app_id="", run_id=""):
        """Store the four scope ids, defaulting any unset value to ``""``."""
        self.user_id = user_id or ""
        self.agent_id = agent_id or ""
        self.app_id = app_id or ""
        self.run_id = run_id or ""

    def validate(self):
        """Raise :class:`MissingEntityScopeError` if no entity id is set."""
        if not (self.user_id or self.agent_id
                or self.app_id or self.run_id):
            raise MissingEntityScopeError()

    def tags(self):
        """Return the ordered list of scope tags after validation."""
        self.validate()
        out = []
        if self.user_id:
            out.append("user_id:" + self.user_id)
        if self.agent_id:
            out.append("agent_id:" + self.agent_id)
        if self.app_id:
            out.append("app_id:" + self.app_id)
        if self.run_id:
            out.append("run_id:" + self.run_id)
        return out


def new_entity_scope(user_id="", agent_id="", app_id="", run_id=""):
    """Build an :class:`EntityScope`. Kept for parity with other ``new_*``."""
    return EntityScope(user_id=user_id, agent_id=agent_id,
                       app_id=app_id, run_id=run_id)


def merge_tags(base, extra):
    """Return ``base`` followed by ``extra`` with empty tags and dups removed.

    Preserves first-seen order. ``None`` is treated as an empty list. Returns
    ``None`` when the combined list is empty so the upstream API call omits
    the field entirely.
    """
    base = list(base) if base else []
    extra = list(extra) if extra else []
    if not base and not extra:
        return None
    seen = set()
    out = []
    for tag in base + extra:
        if not tag or tag in seen:
            continue
        seen.add(tag)
        out.append(tag)
    return out or None


def scoped_tags_match(tags_match):
    """Return ``tags_match`` unless it is unset or the upstream default.

    When ``tags_match`` is empty / ``None`` / ``"any"`` the scoped APIs must
    use ``"all_strict"`` so all scope tags match and untagged global rows
    are excluded.
    """
    if tags_match and tags_match != "any":
        return tags_match
    return _DEFAULT_SCOPED_TAGS_MATCH
