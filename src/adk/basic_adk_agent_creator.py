from typing import Tuple, List, Any, Dict

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import logging

logging.basicConfig(level=logging.ERROR)


class InitDatabaseAgent:
    def __init__(self, agent_configs: Dict[str, Any], session_configs: Dict[str, Any]):
        self.agent_config = agent_configs
        self.session_config = session_configs
        self.agent, self.session_service, self.session = (
            self._create_agent_and_session()
        )

        self.runner_configs = {
            "agent": self.agent,
            "app_name": session_configs["app_name"],
            "session_service": self.session_service,
        }

        self.runner = Runner(**self.runner_configs)

    def _create_agent_and_session(self) -> Tuple:
        try:
            database_agent = Agent(**self.agent_config)
            session_service = InMemorySessionService()
            session = session_service.create_session(**self.session_config)
        except Exception as error:
            logging.error("Error ocured: ", error)

        return database_agent, session_service, session

    async def call_agent_async(self, query: str):
        content = types.Content(role="user", parts=[types.Part(text=query)])

        final_response_text = "Agent did not produce a final response."  # Default

        async for event in self.runner.run_async(
            user_id=self.session_config["user_id"],
            session_id=self.session_config["session_id"],
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:

                    final_response_text = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"

                break

        print(f"<<< Agent Response: {final_response_text}")
