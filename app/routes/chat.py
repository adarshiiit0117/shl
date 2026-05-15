from fastapi import APIRouter
from app.agent.comparer import compare_assessments
from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse
from app.agent.responder import generate_reply
from app.agent.extractor import extract_state
from app.agent.refinement import detect_refinement
from app.agent.conversation import (
    is_conversation_complete
)
from app.agent.clarifier import (
    needs_clarification,
    get_question
)
from app.agent.recommender import recommend
from app.agent.guardrails import blocked_query

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    messages = [m.dict() for m in req.messages]

    latest = messages[-1]["content"]

    comparison_response = compare_assessments(
        latest
    )

    if comparison_response:

        return {
            "reply": comparison_response,
            "recommendations": [],
            "end_of_conversation": False
        }

    if blocked_query(latest):

        return {
            "reply": "I can only discuss SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    state = extract_state(messages)

    if needs_clarification(state):

        return {
            "reply": get_question(state),
            "recommendations": [],
            "end_of_conversation": False
        }

    refinement = detect_refinement(
        latest
    )

    recs = recommend(state)

    if refinement:

        if refinement["type"] == "add_sjt":

            state["needs_sjt"] = True

            recs = recommend(state)

        elif refinement["type"] == "add_cognitive":

            state["needs_cognitive"] = True

            recs = recommend(state)

        elif refinement["type"] == "remove_personality":

            recs = [

                r for r in recs

                if "opq" not in r["name"].lower()
            ]

        elif refinement["type"] == "shorten":

            recs = recs[:3]

    conversation_done = (
    is_conversation_complete(latest)
)

    return {
    "reply": generate_reply(state, recs),
    "recommendations": recs,
    "end_of_conversation": conversation_done
}