import logging

import gym

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.agent import AgentSpec, Agent
from smarts.core.sensors import Observation

from examples import default_argument_parser


logging.basicConfig(level=logging.INFO)

AGENT_ID = "Agent-007"


class KeepLaneAgent(Agent):
    def act(self, obs: Observation):
        return "keep_lane"


def main(scenarios, max_episode_steps=None):
    agent_spec = AgentSpec(
        interface=AgentInterface.from_type(
            AgentType.Laner, max_episode_steps=max_episode_steps
        ),
        agent_builder=KeepLaneAgent,
    )

    env = gym.make(
        "smarts.env:hiway-v0",
        scenarios=scenarios,
        agent_specs={AGENT_ID: agent_spec},
        headless=False,
        visdom=False,
    )

    agent = agent_spec.build_agent()

    # done occurs here under the hood
    observations = env.reset()
    agent_obs = observations[AGENT_ID]
    agent_action = agent.act(agent_obs)
    # This works but should probably warn or assert because the agent no longer exists
    observations, rewards, dones, infos = env.step({AGENT_ID: agent_action})

    # use logger.warning() for giving warnings

    # This passes because done happened in `reset()` and the `env.step()` is no longer concerned with the agent.
    assert not dones["__all__"]

    # This crashes because the agent is done
    agent_obs = observations[AGENT_ID]

    env.close()


if __name__ == "__main__":
    parser = default_argument_parser("single-agent-example")
    args = parser.parse_args()

    main(
        scenarios=args.scenarios, max_episode_steps=0,
    )
