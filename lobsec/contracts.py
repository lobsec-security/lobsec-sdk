"""
LobSec Protocol Contract ABIs and Addresses
"""
from typing import Dict, Any

# Base Mainnet Addresses (v2 - deployed Feb 5, 2026)
AGENT_INSURANCE_POOL = "0x206E260A07b9389E1Cb6f2a42BAEAc6E1374f6F1"
AGENT_STAKING = "0x585aaF900b573a1408fbEB8b02EAf343BdAaae62"
CLAIM_ORACLE = "0x70948e18A166Fa34807C2B5bf4D4b94c8Df79c54"
LOBSEC_REGISTRY = "0x0BDb4d48860520B60C0EF96c2B225aF0c36240c3"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"

# RPC Configuration
BASE_MAINNET_RPC = "https://mainnet.base.org"
BASE_SEPOLIA_RPC = "https://sepolia.base.org"

# Contract ABIs
AGENT_INSURANCE_POOL_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_usdc", "type": "address"},
            {"internalType": "address", "name": "_oracle", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "agent", "type": "address"},
            {"internalType": "address", "name": "protocol", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
            {"internalType": "uint256", "name": "riskScore", "type": "uint256"}
        ],
        "name": "createCoverage",
        "outputs": [{"internalType": "bytes32", "name": "coverageId", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "coverageId", "type": "bytes32"}],
        "name": "coverages",
        "outputs": [
            {"internalType": "address", "name": "agent", "type": "address"},
            {"internalType": "address", "name": "protocol", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "premium", "type": "uint256"},
            {"internalType": "uint256", "name": "startTime", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAvailableCapacity",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"},
            {"internalType": "uint256", "name": "riskScore", "type": "uint256"}
        ],
        "name": "calculatePremium",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "provideLiquidity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "lpTokens", "type": "uint256"}],
        "name": "withdrawLiquidity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "lpBalances",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalReserves",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalCoverageProvided",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "coverageId", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "protocol", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "CoverageCreated",
        "type": "event"
    }
]

AGENT_STAKING_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_usdc", "type": "address"},
            {"internalType": "address", "name": "_lobSecRegistry", "type": "address"},
            {"internalType": "address", "name": "_oracle", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "stakeAsAgent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "protocol", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "duration", "type": "uint256"}
        ],
        "name": "requestCoverage",
        "outputs": [{"internalType": "bytes32", "name": "coverageId", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "getStakedAmount",
        "outputs": [{"internalType": "uint256", "name": "stakedAmount", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "getAgentInfo",
        "outputs": [
            {"internalType": "uint256", "name": "stakedAmount", "type": "uint256"},
            {"internalType": "uint8", "name": "privilegeLevel", "type": "uint8"},
            {"internalType": "uint256", "name": "activeCoverage", "type": "uint256"},
            {"internalType": "uint256", "name": "availableCoverage", "type": "uint256"},
            {"internalType": "bool", "name": "canRequestCoverage", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "requestUnstake",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "executeUnstake",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "agentStakes",
        "outputs": [
            {"internalType": "uint256", "name": "stakedAmount", "type": "uint256"},
            {"internalType": "uint256", "name": "lockedUntil", "type": "uint256"},
            {"internalType": "uint8", "name": "privilegeLevel", "type": "uint8"},
            {"internalType": "uint256", "name": "activeCoverage", "type": "uint256"},
            {"internalType": "uint256", "name": "lastSlashTime", "type": "uint256"},
            {"internalType": "bool", "name": "exists", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "uint8", "name": "privilege", "type": "uint8"}
        ],
        "name": "AgentStaked",
        "type": "event"
    }
]

LOBSEC_REGISTRY_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "isImmunized",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "getThreatLevel",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "registerAgent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "immunize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

USDC_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def get_contracts() -> Dict[str, Dict[str, Any]]:
    """Get all contract configurations"""
    return {
        "AgentInsurancePool": {
            "address": AGENT_INSURANCE_POOL,
            "abi": AGENT_INSURANCE_POOL_ABI
        },
        "AgentStaking": {
            "address": AGENT_STAKING,
            "abi": AGENT_STAKING_ABI
        },
        "ClaimOracle": {
            "address": CLAIM_ORACLE,
            "abi": []
        },
        "LobSecRegistry": {
            "address": LOBSEC_REGISTRY,
            "abi": LOBSEC_REGISTRY_ABI
        },
        "USDC": {
            "address": USDC,
            "abi": USDC_ABI
        }
    }
