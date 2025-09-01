import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'multi_agent_deploy'))

if __name__ == "__main__":
    from multi_agent_deploy import deploy
