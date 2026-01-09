from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import uuid
from enum import Enum
from structlog import get_logger

logger = get_logger()

class AgentStatus(str, Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    PROCESSING = "processing"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class BaseAgent(ABC):
    """
    Abstract base class for all DocVerify AI agents.
    Enforces a standard lifecycle and interface.
    """

    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.status = AgentStatus.IDLE
        self.context: Dict[str, Any] = {}
        self.logger = logger.bind(agent_id=self.agent_id, agent_type=self.__class__.__name__)
        
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the agent with configuration.
        """
        self.status = AgentStatus.INITIALIZING
        self.logger.info("Initializing agent...")
        try:
            await self._initialize_impl(config)
            self.status = AgentStatus.IDLE
            self.logger.info("Agent initialized successfully")
            return True
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.logger.error("Agent initialization failed", error=str(e))
            raise e

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method.
        """
        if self.status == AgentStatus.ERROR:
             raise RuntimeError(f"Agent {self.agent_id} is in ERROR state")
        
        self.status = AgentStatus.PROCESSING
        self.logger.info("Processing task", input_keys=list(input_data.keys()))
        
        try:
            result = await self._process_impl(input_data)
            self.status = AgentStatus.IDLE
            return result
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.logger.error("Processing failed", error=str(e))
            raise e

    async def shutdown(self):
        """
        Cleanup resources.
        """
        self.logger.info("Shutting down agent...")
        await self._shutdown_impl()
        self.status = AgentStatus.SHUTDOWN

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "type": self.__class__.__name__,
            "status": self.status,
            "context_size": len(self.context)
        }

    # --- Abstract Methods to be implemented by subclasses ---

    @abstractmethod
    async def _initialize_impl(self, config: Dict[str, Any]):
        pass

    @abstractmethod
    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def _shutdown_impl(self):
        """Optional override for cleanup"""
        pass
