"""
Insurance Pool Functions
"""
from typing import Optional, Dict, Any, Tuple
from decimal import Decimal
from web3 import Web3

from .contracts import (
    AGENT_INSURANCE_POOL,
    AGENT_STAKING,
    USDC,
    AGENT_INSURANCE_POOL_ABI,
    AGENT_STAKING_ABI,
    USDC_ABI
)


class InsurancePool:
    """Interface for the Agent Insurance Pool"""
    
    USDC_DECIMALS = 6
    
    def __init__(
        self,
        w3: Web3,
        pool_address: Optional[str] = None,
        staking_address: Optional[str] = None
    ):
        """
        Initialize Insurance Pool interface
        
        Args:
            w3: Web3 instance connected to Base
            pool_address: Optional custom pool address
            staking_address: Optional custom staking address
        """
        self.w3 = w3
        
        self.pool_address = Web3.to_checksum_address(pool_address or AGENT_INSURANCE_POOL)
        self.pool = self.w3.eth.contract(
            address=self.pool_address,
            abi=AGENT_INSURANCE_POOL_ABI
        )
        
        self.staking_address = Web3.to_checksum_address(staking_address or AGENT_STAKING)
        self.staking = self.w3.eth.contract(
            address=self.staking_address,
            abi=AGENT_STAKING_ABI
        )
        
        self.usdc = self.w3.eth.contract(
            address=Web3.to_checksum_address(USDC),
            abi=USDC_ABI
        )
    
    def _to_usdc_units(self, amount: float) -> int:
        """Convert USDC amount to contract units (6 decimals)"""
        return int(Decimal(str(amount)) * Decimal(10 ** self.USDC_DECIMALS))
    
    def _from_usdc_units(self, amount: int) -> float:
        """Convert contract units to USDC amount"""
        return float(Decimal(amount) / Decimal(10 ** self.USDC_DECIMALS))
    
    def get_pool_info(self) -> Dict[str, Any]:
        """Get current pool statistics"""
        total_reserves = self.pool.functions.totalReserves().call()
        total_coverage = self.pool.functions.totalCoverageProvided().call()
        available = self.pool.functions.getAvailableCapacity().call()
        
        utilization = 0
        if total_reserves > 0:
            utilization = (total_coverage / total_reserves) * 100
        
        return {
            "total_reserves_usd": self._from_usdc_units(total_reserves),
            "total_coverage_usd": self._from_usdc_units(total_coverage),
            "available_capacity_usd": self._from_usdc_units(available),
            "utilization_percent": round(utilization, 2)
        }
    
    def calculate_premium(
        self,
        amount: float,
        duration_days: int,
        risk_score: int = 1000
    ) -> float:
        """
        Calculate premium for coverage
        
        Args:
            amount: Coverage amount in USD
            duration_days: Coverage duration in days
            risk_score: Risk score 0-10000 (default 1000 = 10%)
            
        Returns:
            Premium amount in USD
        """
        amount_units = self._to_usdc_units(amount)
        duration_seconds = duration_days * 24 * 60 * 60
        
        premium = self.pool.functions.calculatePremium(
            amount_units,
            duration_seconds,
            risk_score
        ).call()
        
        return self._from_usdc_units(premium)
    
    def get_agent_coverage_info(self, agent_address: str) -> Dict[str, Any]:
        """
        Get coverage information for an agent
        
        Args:
            agent_address: Address of the agent
            
        Returns:
            Dictionary with coverage details
        """
        agent = Web3.to_checksum_address(agent_address)
        info = self.staking.functions.getAgentInfo(agent).call()
        
        return {
            "staked_amount_usd": self._from_usdc_units(info[0]),
            "privilege_level": info[1],
            "active_coverage_usd": self._from_usdc_units(info[2]),
            "available_coverage_usd": self._from_usdc_units(info[3]),
            "can_request_coverage": info[4]
        }
    
    def is_covered(
        self,
        agent_address: str,
        amount: Optional[float] = None
    ) -> bool:
        """
        Check if an agent has sufficient coverage
        
        Args:
            agent_address: Address of the agent
            amount: Optional specific amount to check against
            
        Returns:
            True if agent has adequate coverage
        """
        agent = Web3.to_checksum_address(agent_address)
        info = self.get_agent_coverage_info(agent)
        
        if not info["can_request_coverage"]:
            return False
        
        if amount is not None:
            return info["available_coverage_usd"] >= amount
        
        return info["available_coverage_usd"] > 0
    
    def purchase_coverage(
        self,
        agent_address: str,
        protocol_address: str,
        amount: float,
        duration_days: int,
        private_key: str,
        risk_score: int = 1000
    ) -> str:
        """
        Purchase coverage for an agent
        
        Args:
            agent_address: Address of agent to cover
            protocol_address: Address of protocol purchasing coverage
            amount: Coverage amount in USD
            duration_days: Coverage duration in days
            private_key: Private key for transaction signing
            risk_score: Risk score 0-10000
            
        Returns:
            Transaction hash
        """
        agent = Web3.to_checksum_address(agent_address)
        protocol = Web3.to_checksum_address(protocol_address)
        amount_units = self._to_usdc_units(amount)
        duration_seconds = duration_days * 24 * 60 * 60
        
        account = self.w3.eth.account.from_key(private_key)
        
        # Calculate premium
        premium_units = self.pool.functions.calculatePremium(
            amount_units,
            duration_seconds,
            risk_score
        ).call()
        
        # Approve USDC spending
        approve_tx = self.usdc.functions.approve(
            self.pool_address,
            premium_units
        ).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed_approve = self.w3.eth.account.sign_transaction(approve_tx, private_key)
        approve_hash = self.w3.eth.send_raw_transaction(signed_approve.rawTransaction)
        
        # Wait for approval confirmation (simplified)
        self.w3.eth.wait_for_transaction_receipt(approve_hash)
        
        # Create coverage
        tx = self.pool.functions.createCoverage(
            agent,
            protocol,
            amount_units,
            duration_seconds,
            risk_score
        ).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    
    def stake_for_insurance(
        self,
        amount: float,
        private_key: str
    ) -> str:
        """
        Stake USDC to become an insurable agent
        
        Args:
            amount: Amount to stake in USD (minimum $100)
            private_key: Private key for transaction signing
            
        Returns:
            Transaction hash
        """
        amount_units = self._to_usdc_units(amount)
        account = self.w3.eth.account.from_key(private_key)
        
        # Approve USDC spending
        approve_tx = self.usdc.functions.approve(
            self.staking_address,
            amount_units
        ).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed_approve = self.w3.eth.account.sign_transaction(approve_tx, private_key)
        approve_hash = self.w3.eth.send_raw_transaction(signed_approve.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(approve_hash)
        
        # Stake as agent
        tx = self.staking.functions.stakeAsAgent(amount_units).build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
