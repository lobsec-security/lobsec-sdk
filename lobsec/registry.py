"""
LobSec Registry Integration
"""
from typing import Optional, Dict, Any
from web3 import Web3
from web3.contract import Contract
from eth_account.datastructures import SignedTransaction

from .contracts import LOBSEC_REGISTRY, LOBSEC_REGISTRY_ABI


class LobSecRegistry:
    """Interface for the LobSec Registry contract"""
    
    def __init__(self, w3: Web3, contract_address: Optional[str] = None):
        """
        Initialize LobSec Registry interface
        
        Args:
            w3: Web3 instance connected to Base
            contract_address: Optional custom registry address
        """
        self.w3 = w3
        self.address = Web3.to_checksum_address(contract_address or LOBSEC_REGISTRY)
        self.contract = self.w3.eth.contract(
            address=self.address,
            abi=LOBSEC_REGISTRY_ABI
        )
    
    def is_immunized(self, agent_address: str) -> bool:
        """
        Check if an agent is immunized (verified by LobSec)
        
        Args:
            agent_address: Address of the agent to check
            
        Returns:
            True if agent is immunized
        """
        agent = Web3.to_checksum_address(agent_address)
        return self.contract.functions.isImmunized(agent).call()
    
    def get_threat_level(self, agent_address: str) -> int:
        """
        Get the threat level of an agent (0-255)
        
        Args:
            agent_address: Address of the agent to check
            
        Returns:
            Threat level (lower is better)
        """
        agent = Web3.to_checksum_address(agent_address)
        return self.contract.functions.getThreatLevel(agent).call()
    
    def get_agent_status(self, agent_address: str) -> Dict[str, Any]:
        """
        Get full status of an agent from registry
        
        Args:
            agent_address: Address of the agent
            
        Returns:
            Dictionary with immunization and threat info
        """
        agent = Web3.to_checksum_address(agent_address)
        return {
            "address": agent,
            "immunized": self.is_immunized(agent),
            "threat_level": self.get_threat_level(agent),
            "safe": self.get_threat_level(agent) < 50 and self.is_immunized(agent)
        }
    
    def register_agent(self, agent_address: str, private_key: str) -> str:
        """
        Register an agent on the LobSec Registry
        
        Args:
            agent_address: Address of the agent to register
            private_key: Private key for transaction signing
            
        Returns:
            Transaction hash
        """
        agent = Web3.to_checksum_address(agent_address)
        account = self.w3.eth.account.from_key(private_key)
        
        tx = self.contract.functions.registerAgent(agent).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    
    def immunize_agent(self, agent_address: str, private_key: str) -> str:
        """
        Immunize an agent (requires registry authorization)
        
        Args:
            agent_address: Address of the agent to immunize
            private_key: Private key for transaction signing
            
        Returns:
            Transaction hash
        """
        agent = Web3.to_checksum_address(agent_address)
        account = self.w3.eth.account.from_key(private_key)
        
        tx = self.contract.functions.immunize(agent).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
