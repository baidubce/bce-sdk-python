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
DuMemory (Cloud Memory) SDK client.

This client is a thin synchronous wrapper around the upstream Hindsight Python
client (``hindsight_client_api``, https://github.com/vectorize-io/hindsight).
It mirrors the Go SDK method names defined in DuMemory.md one-for-one, with
snake_case Python naming.

Authentication uses an HTTP ``Authorization: Bearer <API_KEY>`` header. The
underlying generated client does not declare any auth settings, so this wrapper
explicitly installs the bearer header on the ``ApiClient`` after construction.

Each public method delegates to the matching ``*Api`` class in
``hindsight_client_api.api`` and bridges the upstream async coroutine to a
synchronous call via :func:`_run_async`. Return values are the upstream pydantic
response models verbatim; callers may invoke ``.model_dump()`` to obtain a
plain dict.
"""

import asyncio
import logging

from baidubce.services.dumemory import dumemory_model

try:
    from hindsight_client_api import ApiClient, Configuration
    from hindsight_client_api.api.banks_api import BanksApi
    from hindsight_client_api.api.directives_api import DirectivesApi
    from hindsight_client_api.api.documents_api import DocumentsApi
    from hindsight_client_api.api.entities_api import EntitiesApi
    from hindsight_client_api.api.files_api import FilesApi
    from hindsight_client_api.api.memory_api import MemoryApi
    from hindsight_client_api.api.mental_models_api import MentalModelsApi
    from hindsight_client_api.api.monitoring_api import MonitoringApi
    from hindsight_client_api.api.operations_api import OperationsApi
    _HINDSIGHT_IMPORT_ERROR = None
except ImportError as _imp_err:  # pragma: no cover - surfaced only at runtime
    ApiClient = Configuration = None
    BanksApi = DirectivesApi = DocumentsApi = EntitiesApi = None
    FilesApi = MemoryApi = MentalModelsApi = MonitoringApi = OperationsApi = None
    _HINDSIGHT_IMPORT_ERROR = _imp_err

_logger = logging.getLogger(__name__)


def _require_hindsight():
    """Raise a clear ImportError if hindsight_client_api is not installed."""
    if _HINDSIGHT_IMPORT_ERROR is not None:
        raise ImportError(
            "hindsight_client_api is not installed. Install the upstream "
            "package via `pip install hindsight-client` before using the "
            "DuMemory SDK."
        ) from _HINDSIGHT_IMPORT_ERROR


def _run_async(coro):
    """Run an asyncio coroutine to completion from synchronous code.

    Creates a fresh event loop when no loop is running in the current thread.
    Raises :class:`RuntimeError` if a loop is already running, since blocking
    inside a running loop would deadlock.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError(
                "DuMemoryClient sync methods cannot be called from inside a "
                "running asyncio event loop. Use the upstream "
                "hindsight_client_api async API directly instead."
            )
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


class DuMemoryClient(object):
    """Synchronous client for the DuMemory (Cloud Memory) service.

    See ``DuMemory.md`` for the full method list. Method names mirror the Go
    SDK, transliterated to snake_case.
    """

    def __init__(self, base_url, api_key, timeout=None):
        _require_hindsight()
        if not base_url:
            raise ValueError("base_url is required")
        if not api_key:
            raise ValueError("api_key is required")

        self._base_url = base_url
        self._api_key = api_key
        self._timeout = timeout

        config = Configuration(host=base_url, access_token=api_key)
        self._api_client = ApiClient(configuration=config)
        # The OpenAPI spec exposes no auth_settings, so the access_token would
        # otherwise not be wired into requests. Install the bearer header
        # explicitly.
        self._api_client.set_default_header(
            "Authorization", "Bearer {0}".format(api_key))

        self._banks = BanksApi(self._api_client)
        self._memory = MemoryApi(self._api_client)
        self._documents = DocumentsApi(self._api_client)
        self._mental_models = MentalModelsApi(self._api_client)
        self._directives = DirectivesApi(self._api_client)
        self._operations = OperationsApi(self._api_client)
        self._entities = EntitiesApi(self._api_client)
        self._monitoring = MonitoringApi(self._api_client)
        self._files = FilesApi(self._api_client)

    # ---------------------------- helpers ---------------------------- #

    def _kw(self, **extra):
        """Build kwargs dict, injecting per-client timeout when set."""
        kw = {}
        if self._timeout is not None:
            kw["_request_timeout"] = self._timeout
        for k, v in extra.items():
            if v is not None:
                kw[k] = v
        return kw

    @staticmethod
    def _options_kwargs(options):
        """Convert an Options container (or dict / None) to a kwargs dict."""
        if options is None:
            return {}
        if hasattr(options, "to_kwargs"):
            return options.to_kwargs()
        if isinstance(options, dict):
            return {k: v for k, v in options.items() if v is not None}
        raise TypeError(
            "options must be a dumemory_model.*Options, dict, or None")

    @staticmethod
    def _coerce(model_cls, payload):
        """Accept either a pydantic model instance or a plain dict."""
        if payload is None:
            return None
        if isinstance(payload, model_cls):
            return payload
        if isinstance(payload, dict):
            return model_cls(**payload)
        return payload

    # =============================== 监控 =============================== #

    def health(self):
        """GET /health — health check (no auth required upstream)."""
        return _run_async(
            self._monitoring.health_endpoint_health_get(**self._kw()))

    def version(self):
        """GET /version — return service version and feature flags."""
        return _run_async(self._monitoring.get_version(**self._kw()))

    # ============================= 记忆库 ============================= #

    def list_banks(self):
        """GET /v1/default/banks — list all memory banks."""
        return _run_async(self._banks.list_banks(**self._kw()))

    def create_bank(self, bank_id, request=None):
        """POST /v1/default/banks/{bankId} — create or update a bank."""
        body = self._coerce(dumemory_model.CreateBankRequest, request)
        if body is None:
            body = dumemory_model.CreateBankRequest()
        return _run_async(self._banks.create_or_update_bank(
            bank_id=bank_id, create_bank_request=body, **self._kw()))

    def get_bank(self, bank_id):
        """GET /v1/default/banks/{bankId}/profile."""
        return _run_async(self._banks.get_bank_profile(
            bank_id=bank_id, **self._kw()))

    def delete_bank(self, bank_id):
        """DELETE /v1/default/banks/{bankId}."""
        return _run_async(self._banks.delete_bank(
            bank_id=bank_id, **self._kw()))

    def get_bank_config(self, bank_id):
        """GET /v1/default/banks/{bankId}/config."""
        return _run_async(self._banks.get_bank_config(
            bank_id=bank_id, **self._kw()))

    def update_bank_config(self, bank_id, request):
        """PATCH /v1/default/banks/{bankId}/config."""
        body = self._coerce(dumemory_model.BankConfigUpdate, request)
        return _run_async(self._banks.update_bank_config(
            bank_id=bank_id, bank_config_update=body, **self._kw()))

    def get_bank_stats(self, bank_id):
        """GET /v1/default/banks/{bankId}/stats."""
        return _run_async(self._banks.get_agent_stats(
            bank_id=bank_id, **self._kw()))

    def consolidate_bank(self, bank_id, request=None):
        """POST /v1/default/banks/{bankId}/consolidate."""
        body = self._coerce(dumemory_model.ConsolidationRequest, request)
        if body is None:
            body = dumemory_model.ConsolidationRequest()
        return _run_async(self._banks.trigger_consolidation(
            bank_id=bank_id, consolidation_request=body, **self._kw()))

    # =============================== 记忆 =============================== #

    def retain(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/memories — synchronous retain."""
        body = self._coerce(dumemory_model.RetainRequest, request)
        # ensure async flag is False for the sync variant
        try:
            body.var_async = False
        except Exception:  # noqa: BLE001 - dict-like fallback
            pass
        return _run_async(self._memory.retain_memories(
            bank_id=bank_id, retain_request=body, **self._kw()))

    def retain_async(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/memories with async=true."""
        body = self._coerce(dumemory_model.RetainRequest, request)
        try:
            body.var_async = True
        except Exception:  # noqa: BLE001
            pass
        return _run_async(self._memory.retain_memories(
            bank_id=bank_id, retain_request=body, **self._kw()))

    def recall(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/memories/recall."""
        body = self._coerce(dumemory_model.RecallRequest, request)
        return _run_async(self._memory.recall_memories(
            bank_id=bank_id, recall_request=body, **self._kw()))

    def reflect(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/reflect."""
        body = self._coerce(dumemory_model.ReflectRequest, request)
        return _run_async(self._memory.reflect(
            bank_id=bank_id, reflect_request=body, **self._kw()))

    def list_memories(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/memories/list."""
        return _run_async(self._memory.list_memories(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    # =============================== 实体 =============================== #

    def list_entities(self, bank_id, limit=None, offset=None):
        """GET /v1/default/banks/{bankId}/entities."""
        return _run_async(self._entities.list_entities(
            bank_id=bank_id,
            **self._kw(limit=limit, offset=offset)))

    def entity_graph(self, bank_id, limit=None, min_count=None):
        """GET /v1/default/banks/{bankId}/entities/graph."""
        return _run_async(self._entities.get_entity_graph(
            bank_id=bank_id,
            **self._kw(limit=limit, min_count=min_count)))

    # =============================== 文档 =============================== #

    def list_documents(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/documents."""
        return _run_async(self._documents.list_documents(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    def get_document(self, bank_id, document_id):
        """GET /v1/default/banks/{bankId}/documents/{documentId}."""
        return _run_async(self._documents.get_document(
            bank_id=bank_id, document_id=document_id, **self._kw()))

    def update_document(self, bank_id, document_id, request):
        """PATCH /v1/default/banks/{bankId}/documents/{documentId}."""
        body = self._coerce(dumemory_model.UpdateDocumentRequest, request)
        return _run_async(self._documents.update_document(
            bank_id=bank_id, document_id=document_id,
            update_document_request=body, **self._kw()))

    def delete_document(self, bank_id, document_id):
        """DELETE /v1/default/banks/{bankId}/documents/{documentId}."""
        return _run_async(self._documents.delete_document(
            bank_id=bank_id, document_id=document_id, **self._kw()))

    def list_document_chunks(self, bank_id, document_id,
                             limit=None, offset=None):
        """GET /v1/default/banks/{bankId}/documents/{documentId}/chunks."""
        return _run_async(self._documents.list_document_chunks(
            bank_id=bank_id, document_id=document_id,
            **self._kw(limit=limit, offset=offset)))

    # ============================= 心智模型 ============================= #

    def list_mental_models(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/mental-models."""
        return _run_async(self._mental_models.list_mental_models(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    def create_mental_model(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/mental-models."""
        body = self._coerce(dumemory_model.CreateMentalModelRequest, request)
        return _run_async(self._mental_models.create_mental_model(
            bank_id=bank_id, create_mental_model_request=body, **self._kw()))

    def get_mental_model(self, bank_id, model_id, detail=None):
        """GET /v1/default/banks/{bankId}/mental-models/{modelId}."""
        return _run_async(self._mental_models.get_mental_model(
            bank_id=bank_id, mental_model_id=model_id,
            **self._kw(detail=detail)))

    def update_mental_model(self, bank_id, model_id, request):
        """PATCH /v1/default/banks/{bankId}/mental-models/{modelId}."""
        body = self._coerce(dumemory_model.UpdateMentalModelRequest, request)
        return _run_async(self._mental_models.update_mental_model(
            bank_id=bank_id, mental_model_id=model_id,
            update_mental_model_request=body, **self._kw()))

    def delete_mental_model(self, bank_id, model_id):
        """DELETE /v1/default/banks/{bankId}/mental-models/{modelId}."""
        return _run_async(self._mental_models.delete_mental_model(
            bank_id=bank_id, mental_model_id=model_id, **self._kw()))

    def refresh_mental_model(self, bank_id, model_id):
        """POST /v1/default/banks/{bankId}/mental-models/{modelId}/refresh."""
        return _run_async(self._mental_models.refresh_mental_model(
            bank_id=bank_id, mental_model_id=model_id, **self._kw()))

    # =============================== 指令 =============================== #

    def list_directives(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/directives."""
        return _run_async(self._directives.list_directives(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    def create_directive(self, bank_id, request):
        """POST /v1/default/banks/{bankId}/directives."""
        body = self._coerce(dumemory_model.CreateDirectiveRequest, request)
        return _run_async(self._directives.create_directive(
            bank_id=bank_id, create_directive_request=body, **self._kw()))

    def get_directive(self, bank_id, directive_id):
        """GET /v1/default/banks/{bankId}/directives/{directiveId}."""
        return _run_async(self._directives.get_directive(
            bank_id=bank_id, directive_id=directive_id, **self._kw()))

    def update_directive(self, bank_id, directive_id, request):
        """PATCH /v1/default/banks/{bankId}/directives/{directiveId}."""
        body = self._coerce(dumemory_model.UpdateDirectiveRequest, request)
        return _run_async(self._directives.update_directive(
            bank_id=bank_id, directive_id=directive_id,
            update_directive_request=body, **self._kw()))

    def delete_directive(self, bank_id, directive_id):
        """DELETE /v1/default/banks/{bankId}/directives/{directiveId}."""
        return _run_async(self._directives.delete_directive(
            bank_id=bank_id, directive_id=directive_id, **self._kw()))

    # =============================== 操作 =============================== #

    def list_operations(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/operations."""
        return _run_async(self._operations.list_operations(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    def get_operation_status(self, bank_id, operation_id):
        """GET /v1/default/banks/{bankId}/operations/{operationId}."""
        return _run_async(self._operations.get_operation_status(
            bank_id=bank_id, operation_id=operation_id, **self._kw()))

    def cancel_operation(self, bank_id, operation_id):
        """DELETE /v1/default/banks/{bankId}/operations/{operationId}."""
        return _run_async(self._operations.cancel_operation(
            bank_id=bank_id, operation_id=operation_id, **self._kw()))

    # ============================= 范围隔离 ============================= #
    # Tag-based entity scope APIs. Each method appends the scope tags onto
    # the underlying request/options before delegating to the matching
    # non-scoped method. See ``EntityScope`` for the tag layout.

    def get_memory(self, bank_id, memory_id):
        """GET /v1/default/banks/{bankId}/memories/{memoryId}."""
        return _run_async(self._memory.get_memory(
            bank_id=bank_id, memory_id=memory_id, **self._kw()))

    def list_tags(self, bank_id, options=None):
        """GET /v1/default/banks/{bankId}/tags."""
        return _run_async(self._memory.list_tags(
            bank_id=bank_id,
            **self._kw(**self._options_kwargs(options))))

    def retain_with_scope(self, bank_id, scope, request):
        """Retain memories after appending entity scope tags.

        Scope tags are merged into each ``items[i].tags`` and into
        ``document_tags`` so batch-level documents stay aligned with their
        memory units. Caller-supplied tags are preserved and de-duplicated.
        """
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.RetainRequest, request)
        items = getattr(body, "items", None) or []
        for item in items:
            base = getattr(item, "tags", None)
            merged = dumemory_model.merge_tags(base, scope_tags)
            try:
                item.tags = merged
            except Exception:  # noqa: BLE001 - dict-like fallback
                pass
        try:
            body.document_tags = dumemory_model.merge_tags(
                getattr(body, "document_tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.retain(bank_id, body)

    def recall_with_scope(self, bank_id, scope, request):
        """Recall memories within an entity scope.

        ``tags_match`` defaults to ``all_strict`` for scoped calls when the
        caller left it unset or at the upstream default ``any``.
        """
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.RecallRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
            body.tags_match = dumemory_model.scoped_tags_match(
                getattr(body, "tags_match", None))
        except Exception:  # noqa: BLE001
            pass
        return self.recall(bank_id, body)

    def reflect_with_scope(self, bank_id, scope, request):
        """Reflect (synthesize) within an entity scope.

        Same ``tags_match`` defaulting as :meth:`recall_with_scope`.
        """
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.ReflectRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
            body.tags_match = dumemory_model.scoped_tags_match(
                getattr(body, "tags_match", None))
        except Exception:  # noqa: BLE001
            pass
        return self.reflect(bank_id, body)

    def get_memory_with_scope(self, bank_id, memory_id, scope):
        """Fetch a memory after validating the scope.

        The upstream endpoint does not accept tag filters; callers can verify
        the returned ``tags`` field contains the expected scope.
        """
        scope.validate()
        return self.get_memory(bank_id, memory_id)

    def list_tags_with_scope(self, bank_id, scope, options=None):
        """List tags visible within an entity scope.

        When ``options.q`` is empty the query is scoped to the first scope
        tag plus a ``*`` wildcard (for example ``user_id:123*``).
        """
        scope_tags = scope.tags()
        if options is None:
            options = dumemory_model.ListTagsOptions()
        if not getattr(options, "q", None) and scope_tags:
            options.q = scope_tags[0] + "*"
        return self.list_tags(bank_id, options)

    def list_documents_with_scope(self, bank_id, scope, options=None):
        """List documents filtered by entity scope."""
        scope_tags = scope.tags()
        if options is None:
            options = dumemory_model.ListDocumentsOptions()
        options.tags = dumemory_model.merge_tags(options.tags, scope_tags)
        options.tags_match = dumemory_model.scoped_tags_match(
            options.tags_match)
        return self.list_documents(bank_id, options)

    def update_document_tags_with_scope(self, bank_id, document_id, scope,
                                        request):
        """Update document tags after appending entity scope tags."""
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.UpdateDocumentRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.update_document(bank_id, document_id, body)

    def list_directives_with_scope(self, bank_id, scope, options=None):
        """List directives filtered by entity scope."""
        scope_tags = scope.tags()
        if options is None:
            options = dumemory_model.ListDirectivesOptions()
        options.tags = dumemory_model.merge_tags(options.tags, scope_tags)
        options.tags_match = dumemory_model.scoped_tags_match(
            options.tags_match)
        return self.list_directives(bank_id, options)

    def create_directive_with_scope(self, bank_id, scope, request):
        """Create a directive after appending entity scope tags."""
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.CreateDirectiveRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.create_directive(bank_id, body)

    def update_directive_with_scope(self, bank_id, directive_id, scope,
                                    request):
        """Update a directive after appending entity scope tags."""
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.UpdateDirectiveRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.update_directive(bank_id, directive_id, body)

    def list_mental_models_with_scope(self, bank_id, scope, options=None):
        """List mental models filtered by entity scope."""
        scope_tags = scope.tags()
        if options is None:
            options = dumemory_model.ListMentalModelsOptions()
        options.tags = dumemory_model.merge_tags(options.tags, scope_tags)
        options.tags_match = dumemory_model.scoped_tags_match(
            options.tags_match)
        return self.list_mental_models(bank_id, options)

    def create_mental_model_with_scope(self, bank_id, scope, request):
        """Create a mental model after appending entity scope tags."""
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.CreateMentalModelRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.create_mental_model(bank_id, body)

    def update_mental_model_with_scope(self, bank_id, model_id, scope,
                                       request):
        """Update a mental model after appending entity scope tags."""
        scope_tags = scope.tags()
        body = self._coerce(dumemory_model.UpdateMentalModelRequest, request)
        try:
            body.tags = dumemory_model.merge_tags(
                getattr(body, "tags", None), scope_tags)
        except Exception:  # noqa: BLE001
            pass
        return self.update_mental_model(bank_id, model_id, body)

    # =============================== 文件 =============================== #

    def files_retain(self, bank_id, files, request):
        """POST /v1/default/banks/{bankId}/files/retain.

        :param files: list of file paths, raw ``bytes``, or
            ``(filename, bytes)`` tuples.
        :param request: JSON string containing the ``FileRetainRequest``
            payload (per the upstream multipart contract); a dict is
            JSON-serialised on your behalf.
        """
        import json as _json
        if isinstance(request, (dict, list)):
            request = _json.dumps(request)
        elif hasattr(request, "to_json"):
            request = request.to_json()
        return _run_async(self._files.file_retain(
            bank_id=bank_id, files=list(files), request=request,
            **self._kw()))


# ----------------------------- factories ----------------------------- #

def new_client(base_url, api_key):
    """Construct a :class:`DuMemoryClient` with no per-request timeout.

    Equivalent to ``DuMemory.New(baseURL, apiKey)`` in the Go SDK.
    """
    return DuMemoryClient(base_url, api_key)


def new_client_with_timeout(base_url, api_key, timeout):
    """Construct a :class:`DuMemoryClient` with a per-request timeout.

    ``timeout`` is forwarded as the upstream ``_request_timeout`` argument and
    accepts either a ``float`` (total seconds) or a ``(connect, read)`` tuple.
    Equivalent to ``DuMemory.NewWithTimeout(baseURL, apiKey, timeout)``.
    """
    return DuMemoryClient(base_url, api_key, timeout=timeout)
