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
Unit tests for ``baidubce.services.dumemory.dumemory_client``.

The upstream ``hindsight_client_api`` package is replaced by lightweight stub
modules at import time, so the tests do not require the real dependency and do
not perform any network IO. Each test asserts that:

1. ``DuMemoryClient`` constructs the expected upstream ``ApiClient`` /
   ``Configuration`` and installs the bearer token header.
2. Each public SDK method dispatches to the correct upstream ``*Api`` async
   method with the correct keyword arguments, including request-body type
   coercion and ``ListXxxOptions`` unpacking.

Run with::

    python3 -m unittest baidubce.services.dumemory.test_dumemory_client

or::

    python3 -m pytest baidubce/services/dumemory/test_dumemory_client.py
"""

import sys
import types
import unittest


# --------------------------------------------------------------------------- #
# Stub out hindsight_client_api before the SUT is imported.                   #
# The stubs record every constructor call and every coroutine method call so  #
# the tests can introspect the dispatch.                                      #
# --------------------------------------------------------------------------- #

CALLS = []  # list of (api_name, method_name, kwargs)


def _install_hindsight_stubs():
    """Install fake hindsight_client_api package into sys.modules."""

    pkg = types.ModuleType("hindsight_client_api")

    class Configuration(object):
        """Stub configuration object used by the fake API client."""

        def __init__(self, host=None, access_token=None, **kwargs):
            """Store configuration values passed by the SDK client."""
            self.host = host
            self.access_token = access_token
            self.kwargs = kwargs

    class ApiClient(object):
        """Stub API client that records default headers."""

        def __init__(self, configuration=None):
            """Initialize the stub with an optional configuration."""
            self.configuration = configuration
            self.default_headers = {}

        def set_default_header(self, name, value):
            """Record a default header on the stub client."""
            self.default_headers[name] = value

    pkg.Configuration = Configuration
    pkg.ApiClient = ApiClient
    sys.modules["hindsight_client_api"] = pkg

    # Sub-package: hindsight_client_api.api with one stub class per *Api.
    api_pkg = types.ModuleType("hindsight_client_api.api")
    sys.modules["hindsight_client_api.api"] = api_pkg

    # Each upstream API exposes a set of async methods; we don't need full
    # fidelity, just an awaitable that records the call.
    def _make_api_class(name, methods):
        """Build a stub upstream API class for the requested methods."""

        class _StubApi(object):
            """Stub upstream API class bound to one API name."""

            API_NAME = name

            def __init__(self, api_client=None):
                """Store the API client passed by the SDK client."""
                self.api_client = api_client

        async def _record(self, _method=None, **kwargs):
            """Record an awaited upstream API method call."""
            CALLS.append((self.API_NAME, _method, kwargs))
            return {"api": self.API_NAME, "method": _method, "kwargs": kwargs}

        for m in methods:
            # bind a closure capturing the method name
            def _bind(method_name):
                """Bind a coroutine to a specific upstream method name."""

                async def _coro(self, **kwargs):
                    """Record the coroutine invocation for assertions."""
                    return await _record(self, _method=method_name, **kwargs)
                _coro.__name__ = method_name
                return _coro
            setattr(_StubApi, m, _bind(m))
        _StubApi.__name__ = name
        return _StubApi

    api_specs = {
        "banks_api": ("BanksApi", [
            "list_banks", "create_or_update_bank", "get_bank_profile",
            "delete_bank", "get_bank_config", "update_bank_config",
            "get_agent_stats", "trigger_consolidation",
        ]),
        "memory_api": ("MemoryApi", [
            "retain_memories", "recall_memories", "reflect", "list_memories",
        ]),
        "documents_api": ("DocumentsApi", [
            "list_documents", "get_document", "update_document",
            "delete_document", "list_document_chunks",
        ]),
        "mental_models_api": ("MentalModelsApi", [
            "list_mental_models", "create_mental_model", "get_mental_model",
            "update_mental_model", "delete_mental_model",
            "refresh_mental_model",
        ]),
        "directives_api": ("DirectivesApi", [
            "list_directives", "create_directive", "get_directive",
            "update_directive", "delete_directive",
        ]),
        "operations_api": ("OperationsApi", [
            "list_operations", "cancel_operation",
        ]),
        "entities_api": ("EntitiesApi", [
            "list_entities", "get_entity_graph",
        ]),
        "monitoring_api": ("MonitoringApi", [
            "health_endpoint_health_get", "get_version",
        ]),
        "files_api": ("FilesApi", ["file_retain"]),
    }

    for mod_name, (class_name, methods) in api_specs.items():
        sub = types.ModuleType("hindsight_client_api.api." + mod_name)
        cls = _make_api_class(class_name, methods)
        setattr(sub, class_name, cls)
        sys.modules["hindsight_client_api.api." + mod_name] = sub

    # Sub-package: hindsight_client_api.models with stub request classes.
    models_pkg = types.ModuleType("hindsight_client_api.models")
    sys.modules["hindsight_client_api.models"] = models_pkg

    def _make_model_class(name):
        """Build a stub model class accepting arbitrary keyword fields."""

        class _Model(object):
            """Stub model object that stores keyword fields as attributes."""

            __MODEL_NAME__ = name

            def __init__(self, **kwargs):
                """Copy keyword fields onto the model instance."""
                self.__dict__.update(kwargs)

            def to_json(self):
                """Serialize public model fields to JSON."""
                import json as _j
                return _j.dumps({k: v for k, v in self.__dict__.items()
                                 if not k.startswith("_")})

        _Model.__name__ = name
        return _Model

    model_files = {
        "create_bank_request": "CreateBankRequest",
        "bank_config_update": "BankConfigUpdate",
        "consolidation_request": "ConsolidationRequest",
        "memory_item": "MemoryItem",
        "retain_request": "RetainRequest",
        "recall_request": "RecallRequest",
        "reflect_request": "ReflectRequest",
        "update_document_request": "UpdateDocumentRequest",
        "create_mental_model_request": "CreateMentalModelRequest",
        "update_mental_model_request": "UpdateMentalModelRequest",
        "create_directive_request": "CreateDirectiveRequest",
        "update_directive_request": "UpdateDirectiveRequest",
    }
    for mod_name, class_name in model_files.items():
        sub = types.ModuleType("hindsight_client_api.models." + mod_name)
        setattr(sub, class_name, _make_model_class(class_name))
        sys.modules["hindsight_client_api.models." + mod_name] = sub


_install_hindsight_stubs()

# Now safe to import the SUT.
from baidubce.services.dumemory import dumemory_client  # noqa: E402
from baidubce.services.dumemory import dumemory_model  # noqa: E402


BASE_URL = "https://cloud.memory.bj.baidubce.com/api"
API_KEY = "bce-v3/ALTAK-test/secret"


def _new_client(timeout=None):
    """Construct a client and reset the per-test call recorder."""
    del CALLS[:]
    if timeout is None:
        return dumemory_client.new_client(BASE_URL, API_KEY)
    return dumemory_client.new_client_with_timeout(BASE_URL, API_KEY, timeout)


def _last_call():
    """Return the last recorded upstream API call."""
    assert CALLS, "no upstream call was recorded"
    return CALLS[-1]


class ConstructionTest(unittest.TestCase):
    """Cover the constructor + factory helpers."""

    def test_new_client_sets_bearer_header_and_host(self):
        """Verify new client sets bearer header and host behavior."""
        cli = _new_client()
        self.assertEqual(cli._base_url, BASE_URL)
        self.assertEqual(cli._api_key, API_KEY)
        self.assertIsNone(cli._timeout)
        self.assertEqual(cli._api_client.configuration.host, BASE_URL)
        self.assertEqual(cli._api_client.configuration.access_token, API_KEY)
        self.assertEqual(
            cli._api_client.default_headers["Authorization"],
            "Bearer " + API_KEY,
        )

    def test_new_client_with_timeout(self):
        """Verify new client with timeout behavior."""
        cli = _new_client(timeout=30)
        self.assertEqual(cli._timeout, 30)
        cli.list_banks()
        _, _, kwargs = _last_call()
        self.assertEqual(kwargs.get("_request_timeout"), 30)

    def test_missing_base_url(self):
        """Verify missing base url behavior."""
        self.assertRaises(ValueError, dumemory_client.new_client, "", API_KEY)

    def test_missing_api_key(self):
        """Verify missing api key behavior."""
        self.assertRaises(ValueError, dumemory_client.new_client, BASE_URL, "")


class MonitoringTest(unittest.TestCase):
    """Cover MonitoringTest behavior."""
    def test_health(self):
        """Verify health behavior."""
        cli = _new_client()
        cli.health()
        api, method, _ = _last_call()
        self.assertEqual((api, method),
                         ("MonitoringApi", "health_endpoint_health_get"))

    def test_version(self):
        """Verify version behavior."""
        cli = _new_client()
        cli.version()
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("MonitoringApi", "get_version"))


class BanksTest(unittest.TestCase):
    """Cover BanksTest behavior."""
    def test_list_banks(self):
        """Verify list banks behavior."""
        cli = _new_client()
        cli.list_banks()
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("BanksApi", "list_banks"))

    def test_create_bank_with_dict(self):
        """Verify create bank with dict behavior."""
        cli = _new_client()
        cli.create_bank("bank-1", {"name": "x"})
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("BanksApi", "create_or_update_bank"))
        self.assertEqual(kw["bank_id"], "bank-1")
        self.assertIsInstance(kw["create_bank_request"],
                              dumemory_model.CreateBankRequest)
        self.assertEqual(kw["create_bank_request"].name, "x")

    def test_create_bank_default_body(self):
        """Verify create bank default body behavior."""
        cli = _new_client()
        cli.create_bank("bank-1")
        _, _, kw = _last_call()
        self.assertIsInstance(kw["create_bank_request"],
                              dumemory_model.CreateBankRequest)

    def test_get_bank(self):
        """Verify get bank behavior."""
        cli = _new_client()
        cli.get_bank("b")
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("BanksApi", "get_bank_profile"))
        self.assertEqual(kw["bank_id"], "b")

    def test_delete_bank(self):
        """Verify delete bank behavior."""
        cli = _new_client()
        cli.delete_bank("b")
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("BanksApi", "delete_bank"))

    def test_get_bank_config(self):
        """Verify get bank config behavior."""
        cli = _new_client()
        cli.get_bank_config("b")
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("BanksApi", "get_bank_config"))

    def test_update_bank_config(self):
        """Verify update bank config behavior."""
        cli = _new_client()
        cli.update_bank_config("b", {"updates": {"k": "v"}})
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("BanksApi", "update_bank_config"))
        self.assertIsInstance(kw["bank_config_update"],
                              dumemory_model.BankConfigUpdate)

    def test_get_bank_stats(self):
        """Verify get bank stats behavior."""
        cli = _new_client()
        cli.get_bank_stats("b")
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("BanksApi", "get_agent_stats"))

    def test_consolidate_bank_default(self):
        """Verify consolidate bank default behavior."""
        cli = _new_client()
        cli.consolidate_bank("b")
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("BanksApi", "trigger_consolidation"))
        self.assertIsInstance(kw["consolidation_request"],
                              dumemory_model.ConsolidationRequest)


class MemoryTest(unittest.TestCase):
    """Cover MemoryTest behavior."""
    def test_retain_sets_async_false(self):
        """Verify retain sets async false behavior."""
        cli = _new_client()
        req = dumemory_model.RetainRequest(items=[], var_async=True)
        cli.retain("b", req)
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("MemoryApi", "retain_memories"))
        self.assertFalse(kw["retain_request"].var_async)

    def test_retain_async_sets_async_true(self):
        """Verify retain async sets async true behavior."""
        cli = _new_client()
        req = dumemory_model.RetainRequest(items=[], var_async=False)
        cli.retain_async("b", req)
        _, method, kw = _last_call()
        self.assertEqual(method, "retain_memories")
        self.assertTrue(kw["retain_request"].var_async)

    def test_retain_accepts_dict(self):
        """Verify retain accepts dict behavior."""
        cli = _new_client()
        cli.retain("b", {"items": []})
        _, _, kw = _last_call()
        self.assertIsInstance(kw["retain_request"],
                              dumemory_model.RetainRequest)

    def test_recall(self):
        """Verify recall behavior."""
        cli = _new_client()
        cli.recall("b", {"query": "hi"})
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("MemoryApi", "recall_memories"))
        self.assertEqual(kw["recall_request"].query, "hi")

    def test_reflect(self):
        """Verify reflect behavior."""
        cli = _new_client()
        cli.reflect("b", {"query": "why"})
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("MemoryApi", "reflect"))
        self.assertEqual(kw["reflect_request"].query, "why")

    def test_list_memories_with_options(self):
        """Verify list memories with options behavior."""
        cli = _new_client()
        opts = dumemory_model.ListMemoriesOptions(
            type="world", limit=10, offset=0)
        cli.list_memories("b", opts)
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("MemoryApi", "list_memories"))
        self.assertEqual(kw["bank_id"], "b")
        self.assertEqual(kw["type"], "world")
        self.assertEqual(kw["limit"], 10)
        self.assertEqual(kw["offset"], 0)
        self.assertNotIn("q", kw)  # None values are dropped

    def test_list_memories_no_options(self):
        """Verify list memories no options behavior."""
        cli = _new_client()
        cli.list_memories("b")
        _, _, kw = _last_call()
        self.assertEqual(set(kw.keys()), {"bank_id"})


class EntitiesTest(unittest.TestCase):
    """Cover EntitiesTest behavior."""
    def test_list_entities(self):
        """Verify list entities behavior."""
        cli = _new_client()
        cli.list_entities("b", limit=5, offset=0)
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("EntitiesApi", "list_entities"))
        self.assertEqual(kw["limit"], 5)
        self.assertEqual(kw["offset"], 0)

    def test_entity_graph(self):
        """Verify entity graph behavior."""
        cli = _new_client()
        cli.entity_graph("b", limit=20, min_count=2)
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("EntitiesApi", "get_entity_graph"))
        self.assertEqual(kw["min_count"], 2)


class DocumentsTest(unittest.TestCase):
    """Cover DocumentsTest behavior."""
    def test_list_documents_with_options(self):
        """Verify list documents with options behavior."""
        cli = _new_client()
        opts = dumemory_model.ListDocumentsOptions(q="x", limit=3)
        cli.list_documents("b", opts)
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("DocumentsApi", "list_documents"))
        self.assertEqual(kw["q"], "x")
        self.assertEqual(kw["limit"], 3)

    def test_get_document(self):
        """Verify get document behavior."""
        cli = _new_client()
        cli.get_document("b", "d")
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("DocumentsApi", "get_document"))
        self.assertEqual(kw["document_id"], "d")

    def test_update_document(self):
        """Verify update document behavior."""
        cli = _new_client()
        cli.update_document("b", "d", {"tags": ["a"]})
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("DocumentsApi", "update_document"))
        self.assertIsInstance(kw["update_document_request"],
                              dumemory_model.UpdateDocumentRequest)

    def test_delete_document(self):
        """Verify delete document behavior."""
        cli = _new_client()
        cli.delete_document("b", "d")
        api, method, _ = _last_call()
        self.assertEqual((api, method), ("DocumentsApi", "delete_document"))

    def test_list_document_chunks(self):
        """Verify list document chunks behavior."""
        cli = _new_client()
        cli.list_document_chunks("b", "d", limit=10, offset=20)
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("DocumentsApi", "list_document_chunks"))
        self.assertEqual(kw["limit"], 10)
        self.assertEqual(kw["offset"], 20)


class MentalModelsTest(unittest.TestCase):
    """Cover MentalModelsTest behavior."""
    def test_list_mental_models(self):
        """Verify list mental models behavior."""
        cli = _new_client()
        opts = dumemory_model.ListMentalModelsOptions(detail="full")
        cli.list_mental_models("b", opts)
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "list_mental_models"))
        self.assertEqual(kw["detail"], "full")

    def test_create_mental_model(self):
        """Verify create mental model behavior."""
        cli = _new_client()
        cli.create_mental_model("b", {"name": "n", "source_query": "q"})
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "create_mental_model"))
        self.assertIsInstance(kw["create_mental_model_request"],
                              dumemory_model.CreateMentalModelRequest)

    def test_get_mental_model(self):
        """Verify get mental model behavior."""
        cli = _new_client()
        cli.get_mental_model("b", "m", detail="content")
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "get_mental_model"))
        self.assertEqual(kw["mental_model_id"], "m")
        self.assertEqual(kw["detail"], "content")

    def test_update_mental_model(self):
        """Verify update mental model behavior."""
        cli = _new_client()
        cli.update_mental_model("b", "m", {"name": "n2"})
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "update_mental_model"))
        self.assertIsInstance(kw["update_mental_model_request"],
                              dumemory_model.UpdateMentalModelRequest)

    def test_delete_mental_model(self):
        """Verify delete mental model behavior."""
        cli = _new_client()
        cli.delete_mental_model("b", "m")
        api, method, _ = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "delete_mental_model"))

    def test_refresh_mental_model(self):
        """Verify refresh mental model behavior."""
        cli = _new_client()
        cli.refresh_mental_model("b", "m")
        api, method, _ = _last_call()
        self.assertEqual((api, method),
                         ("MentalModelsApi", "refresh_mental_model"))


class DirectivesTest(unittest.TestCase):
    """Cover DirectivesTest behavior."""
    def test_list_directives(self):
        """Verify list directives behavior."""
        cli = _new_client()
        opts = dumemory_model.ListDirectivesOptions(active_only=True)
        cli.list_directives("b", opts)
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("DirectivesApi", "list_directives"))
        self.assertTrue(kw["active_only"])

    def test_create_directive(self):
        """Verify create directive behavior."""
        cli = _new_client()
        cli.create_directive("b", {"name": "n", "content": "c"})
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("DirectivesApi", "create_directive"))
        self.assertIsInstance(kw["create_directive_request"],
                              dumemory_model.CreateDirectiveRequest)

    def test_get_directive(self):
        """Verify get directive behavior."""
        cli = _new_client()
        cli.get_directive("b", "d")
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("DirectivesApi", "get_directive"))
        self.assertEqual(kw["directive_id"], "d")

    def test_update_directive(self):
        """Verify update directive behavior."""
        cli = _new_client()
        cli.update_directive("b", "d", {"content": "c2"})
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("DirectivesApi", "update_directive"))
        self.assertIsInstance(kw["update_directive_request"],
                              dumemory_model.UpdateDirectiveRequest)

    def test_delete_directive(self):
        """Verify delete directive behavior."""
        cli = _new_client()
        cli.delete_directive("b", "d")
        api, method, _ = _last_call()
        self.assertEqual((api, method),
                         ("DirectivesApi", "delete_directive"))


class OperationsTest(unittest.TestCase):
    """Cover OperationsTest behavior."""
    def test_list_operations(self):
        """Verify list operations behavior."""
        cli = _new_client()
        opts = dumemory_model.ListOperationsOptions(status="pending", limit=5)
        cli.list_operations("b", opts)
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("OperationsApi", "list_operations"))
        self.assertEqual(kw["status"], "pending")
        self.assertEqual(kw["limit"], 5)

    def test_cancel_operation(self):
        """Verify cancel operation behavior."""
        cli = _new_client()
        cli.cancel_operation("b", "op")
        api, method, kw = _last_call()
        self.assertEqual((api, method),
                         ("OperationsApi", "cancel_operation"))
        self.assertEqual(kw["operation_id"], "op")


class FilesTest(unittest.TestCase):
    """Cover FilesTest behavior."""
    def test_files_retain_with_dict_request(self):
        """Verify files retain with dict request behavior."""
        cli = _new_client()
        cli.files_retain("b", [b"\x00data"], {"tags": ["x"]})
        api, method, kw = _last_call()
        self.assertEqual((api, method), ("FilesApi", "file_retain"))
        # dict requests are JSON-serialised
        self.assertIsInstance(kw["request"], str)
        self.assertIn("tags", kw["request"])
        self.assertEqual(kw["files"], [b"\x00data"])

    def test_files_retain_with_string_request(self):
        """Verify files retain with string request behavior."""
        cli = _new_client()
        payload = '{"tags":["x"]}'
        cli.files_retain("b", [], payload)
        _, _, kw = _last_call()
        self.assertEqual(kw["request"], payload)


class CoverageTest(unittest.TestCase):
    """Sanity check that the test-suite covers every public SDK method."""

    def test_every_public_method_exercised(self):
        """Verify every public method exercised behavior."""
        public_methods = {
            name for name in vars(dumemory_client.DuMemoryClient)
            if (not name.startswith("_")
                and callable(getattr(dumemory_client.DuMemoryClient, name)))
        }
        # Expected = the method names tested above.
        tested = {
            "health", "version",
            "list_banks", "create_bank", "get_bank", "delete_bank",
            "get_bank_config", "update_bank_config", "get_bank_stats",
            "consolidate_bank",
            "retain", "retain_async", "recall", "reflect", "list_memories",
            "list_entities", "entity_graph",
            "list_documents", "get_document", "update_document",
            "delete_document", "list_document_chunks",
            "list_mental_models", "create_mental_model", "get_mental_model",
            "update_mental_model", "delete_mental_model",
            "refresh_mental_model",
            "list_directives", "create_directive", "get_directive",
            "update_directive", "delete_directive",
            "list_operations", "cancel_operation",
            "files_retain",
        }
        missing = public_methods - tested
        self.assertFalse(
            missing,
            "DuMemoryClient methods without a unit test: %s" % sorted(missing))


if __name__ == "__main__":
    unittest.main()
