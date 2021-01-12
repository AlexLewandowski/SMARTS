from smarts.zoo.registry import register
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.agent import Agent, AgentSpec


class SimpleAgent(Agent):
    def act(self, obs):
        return "keep_lane"


# You can register a callable that will build your AgentSpec
def demo_agent_callable(target_prefix=None, interface=None):
    if interface is None:
        interface = AgentInterface.from_type(AgentType.Laner)
    return AgentSpec(interface=interface, agent_builder=SimpleAgent)


register(
    locator="zoo-agent1-v0",
    entrypoint="smarts.core.agent:AgentSpec",
    # Also works:
    # entrypoint=smarts.core.agent.AgentSpec
    interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=20000),
)

register(
    locator="zoo-agent2-v0",
    entrypoint=demo_agent_callable,
    # Also works:
    # entrypoint="scenarios.zoo_intersection:demo_agent_callable",
)
