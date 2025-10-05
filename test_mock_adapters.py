import pytest
import asyncio
from src.adapters.mock_note_maker import MockNoteMaker
from src.adapters.mock_flashcard import MockFlashcard
from src.adapters.mock_concept_explainer import MockConceptExplainer

@pytest.mark.asyncio
async def test_note_maker_valid():
    adapter = MockNoteMaker()
    payload = {"topic": "photosynthesis"}
    result = await adapter.call(payload)
    assert "title" in result
    assert "summary" in result
    assert "note_sections" in result
    assert result["topic"] == "photosynthesis"
    assert result["tool"] == "note_maker"


@pytest.mark.asyncio
async def test_note_maker_missing_topic():
    adapter = MockNoteMaker()
    payload = {}
    result = await adapter.call(payload)
    assert "error" in result
    assert "Missing fields" in result["error"]


@pytest.mark.asyncio
async def test_flashcard_valid():
    adapter = MockFlashcard()
    payload = {"topic": "calculus", "count": 3}
    result = await adapter.call(payload)
    assert "flashcards" in result
    assert len(result["flashcards"]) == 3
    assert result["topic"] == "calculus"
    assert result["tool"] == "flashcard_generator"


@pytest.mark.asyncio
async def test_flashcard_default_count():
    adapter = MockFlashcard()
    payload = {"topic": "biology"}
    result = await adapter.call(payload)
    assert len(result["flashcards"]) == 5  
    assert result["tool"] == "flashcard_generator"


@pytest.mark.asyncio
async def test_concept_explainer_with_concept():
    adapter = MockConceptExplainer()
    payload = {"concept_to_explain": "Newton's laws", "desired_depth": "intermediate"}
    result = await adapter.call(payload)
    assert result["concept"] == "Newton's laws"
    assert "explanation" in result
    assert result["tool"] == "concept_explainer"


@pytest.mark.asyncio
async def test_concept_explainer_with_topic_fallback():
    adapter = MockConceptExplainer()
    payload = {"topic": "osmosis"}
    result = await adapter.call(payload)
    assert result["concept"] == "osmosis"
    assert "explanation" in result
    assert result["tool"] == "concept_explainer"
