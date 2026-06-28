# -*- coding: utf-8 -*-
"""Examples for the DuMemory entity-scope (tag isolation) APIs.

Each example mirrors a function in the Go SDK's
``examples/dumemory/example_tag_scoped.go``. The entity scope is materialised
as ``user_id:<id>``, ``agent_id:<id>``, ``app_id:<id>`` and ``run_id:<id>``
tags that the SDK appends to every relevant request automatically.
"""

from baidubce.services.dumemory import dumemory_client
from baidubce.services.dumemory import dumemory_model
from sample.dumemory import dumemory_sample_conf as conf


def retain_with_scope():
    """POST memories within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")

    item = dumemory_model.new_memory_item(
        content="User likes concise technical explanations.",
        tags=["topic:preference"])
    request = dumemory_model.new_retain_request(
        items=[item], document_tags=["source:example"])

    return client.retain_with_scope(conf.BANK_ID, scope, request)


def recall_with_scope():
    """POST recall within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")

    request = dumemory_model.new_recall_request(
        query="What response style does the user prefer?",
        tags=["topic:preference"])
    return client.recall_with_scope(conf.BANK_ID, scope, request)


def reflect_with_scope():
    """POST reflect within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", agent_id="your-agent-id")

    request = dumemory_model.new_reflect_request(
        query="Summarize the user's current working preferences.",
        tags=["topic:preference"])
    return client.reflect_with_scope(conf.BANK_ID, scope, request)


def list_tags_with_scope():
    """GET tags within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(user_id="your-user-id")
    return client.list_tags_with_scope(
        conf.BANK_ID, scope,
        dumemory_model.ListTagsOptions(source="memories", limit=20))


def list_documents_with_scope():
    """GET documents filtered by entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", run_id="your-run-id")
    return client.list_documents_with_scope(
        conf.BANK_ID, scope,
        dumemory_model.ListDocumentsOptions(
            tags=["source:example"], limit=20))


def update_document_tags_with_scope():
    """PATCH document tags within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")
    request = dumemory_model.new_update_document_request(
        tags=["source:example", "topic:preference"])
    return client.update_document_tags_with_scope(
        conf.BANK_ID, "your-document-id", scope, request)


def create_directive_with_scope():
    """POST a directive within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", agent_id="your-agent-id")
    request = dumemory_model.new_create_directive_request(
        name="scoped-tone",
        content="Use a concise and practical tone.",
        tags=["topic:style"])
    return client.create_directive_with_scope(
        conf.BANK_ID, scope, request)


def list_directives_with_scope():
    """GET directives filtered by entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", agent_id="your-agent-id")
    return client.list_directives_with_scope(
        conf.BANK_ID, scope,
        dumemory_model.ListDirectivesOptions(
            tags=["topic:style"], active_only=True, limit=20))


def update_directive_with_scope():
    """PATCH a directive within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", agent_id="your-agent-id")
    request = dumemory_model.new_update_directive_request(
        tags=["topic:style", "state:active"])
    return client.update_directive_with_scope(
        conf.BANK_ID, "your-directive-id", scope, request)


def create_mental_model_with_scope():
    """POST a mental model within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")
    request = dumemory_model.new_create_mental_model_request(
        name="User Preference Model",
        source_query="What does this user prefer while working?",
        tags=["topic:preference"])
    return client.create_mental_model_with_scope(
        conf.BANK_ID, scope, request)


def list_mental_models_with_scope():
    """GET mental models filtered by entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")
    return client.list_mental_models_with_scope(
        conf.BANK_ID, scope,
        dumemory_model.ListMentalModelsOptions(
            tags=["topic:preference"], limit=20))


def update_mental_model_with_scope():
    """PATCH a mental model within an entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(
        user_id="your-user-id", app_id="your-app-id")
    request = dumemory_model.new_update_mental_model_request(
        tags=["topic:preference", "state:active"])
    return client.update_mental_model_with_scope(
        conf.BANK_ID, "your-model-id", scope, request)


def get_memory_with_scope():
    """GET a memory after validating the entity scope."""
    client = dumemory_client.new_client(conf.BASE_URL, conf.API_KEY)
    scope = dumemory_model.EntityScope(user_id="your-user-id")
    return client.get_memory_with_scope(
        conf.BANK_ID, "your-memory-id", scope)


if __name__ == "__main__":
    try:
        print(retain_with_scope())
    except Exception as exc:  # noqa: BLE001
        print("Exception when calling api: %s" % exc)
