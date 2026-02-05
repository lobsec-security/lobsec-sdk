"""
LobSec Python SDK

A unified SDK for interacting with the LobSec Agent Insurance Protocol.

Basic usage:
    >>> from lobsec import Agent
    >>> agent = Agent(address="0x...", private_key="...")
    >>> agent.immunize()  # Register on LobSec Registry
    >>> agent.stake(usd=500)  # Stake for insurance
    >>> agent.is_covered(amount=1000)  # Check coverage

Advanced usage:
    >>> from lobsec import InsurancePool, LobSecRegistry
    >>> from web3 import Web3
    >>> w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
    >>> pool = InsurancePool(w3)
    >>> info = pool.get_pool_info()
    >>> print(f"Pool TVL: ${info['total_reserves_usd']}")
"""

__version__ = "0.1.0"
__author__ = "LobSec"
__email__ = "security@lobsec.org"

from .agent import Agent
from .insurance import InsurancePool
from .registry import LobSecRegistry
from .contracts import (
    AGENT_INSURANCE_POOL,
    AGENT_STAKING,
    CLAIM_ORACLE,
    LOBSEC_REGISTRY,
    USDC,
    get_contracts,
)

__all__ = [
    "Agent",
    "InsurancePool",
    "LobSecRegistry",
    "AGENT_INSURANCE_POOL",
    "AGENT_STAKING",
    "CLAIM_ORACLE",
    "LOBSEC_REGISTRY",
    "USDC",
    "get_contracts",
]
