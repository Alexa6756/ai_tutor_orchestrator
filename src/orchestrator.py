from typing import List, Dict, Any
from src.context_analysis import analyze_context
from src.parameter_extraction import generate_payload_for_tool
from src.tool_orchestrator import ToolOrchestrator
from src.state_postgres import PostgresStateManager
from src.agents import TutorAgent
from src.personalization import adjust_for_mastery, adjust_for_emotion, adjust_for_learning_style

class Orchestrator:
    def __init__(self):
        self.tool_orch = ToolOrchestrator()
        self.state = PostgresStateManager()  
        self.agent = TutorAgent()  

    async def handle_chat(
        self,
        user_info: Dict[str, Any],
        chat_history: List[Dict[str, str]],
        latest_message: str,
    ) -> Dict[str, Any]:
        """
        Orchestrator workflow:
        1. Update user state in DB
        2. Select tools via agent or context analysis
        3. Generate payloads with validation and personalization
        4. Call tool adapters
        5. Handle low-confidence via clarifying questions
        """
        user_id = user_info.get("user_id")
        previous_info = self.state.get_user(user_id) or {}
        merged_user_info = {**previous_info, **user_info}
        self.state.upsert_user(merged_user_info)

        
        selected_tools = self.agent.choose_tools(chat_history, latest_message)
        if not selected_tools:
            context_analysis = analyze_context(chat_history, latest_message)
            selected_tools = context_analysis.get("tools", [])

        outputs = {
            "selected_tools": selected_tools,
            "analysis": {"agent_tools": selected_tools},
            "payloads": {},
            "tool_responses": {},
            "clarify_question": None,
        }

        
        for tool in selected_tools:
            schema = self.tool_orch.load_schema(tool)

            
            payload, confidence = await generate_payload_for_tool(
                tool_name=tool,
                schema=schema,
                chat_history=chat_history,
                latest_message=latest_message,
                user_info=merged_user_info,
                state=self.state,
            )

            
            if tool == "concept_explainer":
                payload.setdefault("user_info", merged_user_info)
                payload.setdefault("chat_history", chat_history)
                payload.setdefault("concept_to_explain", latest_message)
                payload.setdefault("current_topic", payload.get("topic", ""))
                
                allowed_depths = ["basic", "intermediate", "advanced", "comprehensive"]
                user_depth = payload.get("desired_depth")
                
                if user_depth and str(user_depth).strip().lower() in allowed_depths:
                    payload["desired_depth"] = str(user_depth).strip().lower()
                else:
                    payload["desired_depth"] = "intermediate"  

           
            payload = adjust_for_mastery(tool, payload, merged_user_info.get("mastery_level", 1))
            payload = adjust_for_emotion(tool, payload, merged_user_info.get("emotional_state", "neutral"))
            payload = adjust_for_learning_style(tool, payload, merged_user_info.get("learning_style", "visual"))

            
            missing_fields = self.tool_orch.check_missing_fields(tool, payload)
            for f in list(missing_fields.keys()):
                if f in previous_info:
                    payload[f] = previous_info[f]
                    del missing_fields[f]

            outputs["payloads"][tool] = {"payload": payload, "confidence": confidence}

            
            if missing_fields:
                outputs["clarify_question"] = self.tool_orch.make_clarifying_question(
                    tool, payload, schema
                )
                self.state.upsert_user(payload.get("user_info", {}))
                return outputs

            
            resp = await self.tool_orch.call_tool(tool, payload)
            outputs["tool_responses"][tool] = resp

        return outputs
