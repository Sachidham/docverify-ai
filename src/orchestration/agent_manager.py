from typing import Dict, Type, Any, Optional
from src.orchestration.agents.base_agent import BaseAgent
from structlog import get_logger

logger = get_logger()

class AgentManager:
    """
    Central orchestrator for managing agent lifecycles.
    Responsible for registering types, spawning instances, and health checks.
    """

    def __init__(self):
        self._registry: Dict[str, Type[BaseAgent]] = {}
        self._active_agents: Dict[str, BaseAgent] = {}
        self.logger = logger.bind(component="AgentManager")

    def register_agent_type(self, type_name: str, agent_class: Type[BaseAgent]):
        """Register a new class of agent."""
        self._registry[type_name] = agent_class
        self.logger.info("Registered agent type", type_name=type_name)

    async def spawn_agent(self, type_name: str, config: Dict[str, Any] = None) -> str:
        """
        Create and initialize a new agent instance.
        Returns the agent_id.
        """
        if type_name not in self._registry:
            raise ValueError(f"Unknown agent type: {type_name}")

        agent_class = self._registry[type_name]
        agent = agent_class() # ID is auto-generated
        
        self.logger.info("Spawning agent", type=type_name, agent_id=agent.agent_id)
        
        await agent.initialize(config or {})
        self._active_agents[agent.agent_id] = agent
        
        return agent.agent_id

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self._active_agents.get(agent_id)

    async def terminate_agent(self, agent_id: str):
        if agent_id in self._active_agents:
            agent = self._active_agents[agent_id]
            await agent.shutdown()
            del self._active_agents[agent_id]
            self.logger.info("Agent terminated", agent_id=agent_id)

    async def shutdown_all(self):
        """Terminate all active agents."""
        self.logger.info("Shutting down all agents", count=len(self._active_agents))
        for agent_id in list(self._active_agents.keys()):
            await self.terminate_agent(agent_id)

    def list_active_agents(self) -> Dict[str, Dict[str, Any]]:
        return {
            aid: agent.get_status() 
            for aid, agent in self._active_agents.items()
        }
