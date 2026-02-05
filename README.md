# LobSec Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/lobsec-security/lobsec-sdk/releases)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/lobsec-security/lobsec-sdk/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Base](https://img.shields.io/badge/Base-L2-0052FF.svg)](https://base.org/)
[![Web3.py](https://img.shields.io/badge/Web3.py-6.x-green.svg)](https://web3py.readthedocs.io/)

A unified Python SDK for interacting with the LobSec Agent Insurance Protocol on Base.

**Live on Base Mainnet** - Contracts verified on BaseScan.

## Features

- 🛡️ **Agent Insurance** - Stake collateral and get coverage for AI agents
- 🔒 **LobSec Registry** - Check immunization status and threat levels
- 💰 **Premium Quotes** - Calculate coverage costs with immunization discounts
- ⚡ **Base Native** - Optimized for Base L2 low fees

## Installation

```bash
pip install lobsec
```

Or install from source:

```bash
git clone https://github.com/lobsec-security/lobsec-sdk.git
cd lobsec-sdk
pip install -e .
```

## Quick Start

```python
from lobsec import Agent

# Initialize agent
agent = Agent(
    address="0xYourAgentAddress",
    private_key="0xYourPrivateKey",
    rpc_url="https://mainnet.base.org"  # Optional, default is Base mainnet
)

# Register on LobSec Registry (one-time)
tx_hash = agent.immunize()
print(f"Immunized! Tx: {tx_hash}")

# Stake USDC to unlock coverage (minimum $100)
tx_hash = agent.stake(usd=500)
print(f"Staked! Tx: {tx_hash}")

# Check if covered for a specific amount
is_covered = agent.is_covered(amount=1000)
print(f"Covered for $1K: {is_covered}")

# Get coverage details
info = agent.coverage_info()
print(f"Staked: ${info['staked_amount_usd']}")
print(f"Available coverage: ${info['available_coverage_usd']}")
```

## Usage Examples

### Get Premium Quote

```python
# Get quote for $10K coverage for 30 days
quote = agent.get_premium_quote(
    coverage_amount=10000,
    duration_days=30
)
print(f"Premium: ${quote['final_premium_usd']}")
print(f"Immunized discount: {quote['discount_percent']}%")
```

### Purchase Coverage

```python
# A protocol purchases coverage for this agent
tx_hash = agent.purchase_coverage(
    protocol_address="0xProtocolAddress",
    amount=5000,  # $5K coverage
    duration_days=90
)
```

### Check Registry Status

```python
status = agent.registry_status()
print(f"Immunized: {status['immunized']}")
print(f"Threat level: {status['threat_level']}")
print(f"Safe to interact: {status['safe']}")
```

### Unstaking

```python
# Request unstake (7-day delay required)
tx_hash = agent.unstake_request()

# After 7 days, execute unstake
tx_hash = agent.unstake_execute()
```

## Advanced Usage

### Direct Pool Access

```python
from lobsec import InsurancePool
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
pool = InsurancePool(w3)

# Get pool statistics
info = pool.get_pool_info()
print(f"Total reserves: ${info['total_reserves_usd']}")
print(f"Utilization: {info['utilization_percent']}%")

# Calculate premium
premium = pool.calculate_premium(
    amount=10000,  # $10K coverage
    duration_days=30,
    risk_score=1000
)
```

### Direct Registry Access

```python
from lobsec import LobSecRegistry

registry = LobSecRegistry(w3)

# Check any agent
is_safe = registry.is_immunized("0xAgentAddress")
threat = registry.get_threat_level("0xAgentAddress")
```

## Contract Addresses

### Base Mainnet (v2 - Feb 2026)

| Contract | Address | BaseScan |
|----------|---------|----------|
| AgentInsurancePool | `0x206E260A07b9389E1Cb6f2a42BAEAc6E1374f6F1` | [View](https://basescan.org/address/0x206E260A07b9389E1Cb6f2a42BAEAc6E1374f6F1) |
| AgentStaking | `0x585aaF900b573a1408fbEB8b02EAf343BdAaae62` | [View](https://basescan.org/address/0x585aaF900b573a1408fbEB8b02EAf343BdAaae62) |
| ClaimOracle | `0x70948e18A166Fa34807C2B5bf4D4b94c8Df79c54` | [View](https://basescan.org/address/0x70948e18A166Fa34807C2B5bf4D4b94c8Df79c54) |
| LobSec Registry | `0x0BDb4d48860520B60C0EF96c2B225aF0c36240c3` | [View](https://basescan.org/address/0x0BDb4d48860520B60C0EF96c2B225aF0c36240c3) |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | [View](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) |

## Privilege Levels

Staking unlocks coverage capacity based on privilege level:

| Level | Min Stake | Max Coverage | Leverage |
|-------|-----------|--------------|----------|
| Basic | $100 | $1,000 | 10x |
| Standard | $1,000 | $10,000 | 10x |
| Premium | $10,000 | $100,000 | 10x |
| Enterprise | $100,000 | $1,000,000 | 10x |

## Immunization Benefits

Agents registered on the LobSec Registry receive:
- **50% premium discount** on insurance
- **Reduced threat scores** in risk calculations
- **Trust signals** for protocols evaluating agents

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black lobsec/

# Type check
mypy lobsec/
```

## Security

- Never hardcode private keys in production
- Use environment variables or secure key management
- The SDK validates all addresses and amounts

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://docs.lobsec.org
- Twitter: [@lobsec](https://twitter.com/lobsec)
- Email: security@lobsec.org
