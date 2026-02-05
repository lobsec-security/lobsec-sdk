"""
LobSec Agent - Main interface for AI agent security and insurance
"""
from typing import Optional, Dict, Any
from web3 import Web3

from .contracts import BASE_MAINNET_RPC
from .registry import LobSecRegistry
from .insurance import InsurancePool


class Agent:
    """
    Main interface for LobSec Agent operations
    
    Example:
        >>> from lobsec import Agent
        >>> agent = Agent(
        ...     address="0x...",
        ...     private_key="0x...",
        ...     rpc_url="https://mainnet.base.org"
        ... )
        >>> agent.immunize()  # Register on LobSec
        >>> agent.stake(usd=500)  # Stake for insurance
        >>> agent.is_covered(amount=1000)  # Check coverage
    """
    
    def __init__(
        self,
        address: str,
        private_key: str,
        rpc_url: str = BASE_MAINNET_RPC,
        pool_address: Optional[str] = None,
        registry_address: Optional[str] = None
    ):
        """
        Initialize LobSec Agent
        
        Args:
            address: Agent's Ethereum address
            private_key: Agent's private key for signing transactions
            rpc_url: Base network RPC URL
            pool_address: Optional custom insurance pool address
            registry_address: Optional custom registry address
        """
        self.address = Web3.to_checksum_address(address)
        self._private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {rpc_url}")
        
        # Initialize components
        self.registry = LobSecRegistry(self.w3, registry_address)
        self.insurance = InsurancePool(
            self.w3,
            pool_address=pool_address
        )
    
    @property
    def balance_eth(self) -> float:
        """Get agent's ETH balance"""
        balance = self.w3.eth.get_balance(self.address)
        return float(self.w3.from_wei(balance, 'ether'))
    
    @property
    def balance_usdc(self) -> float:
        """Get agent's USDC balance"""
        return self.insurance._from_usdc_units(
            self.insurance.usdc.functions.balanceOf(self.address).call()
        )
    
    def immunize(self) -> str:
        """
        Register and immunize agent on LobSec Registry
        
        Returns:
            Transaction hash
        """
        # First register
        tx_hash = self.registry.register_agent(self.address, self._private_key)
        return tx_hash
    
    def stake(self, usd: float) -> str:
        """
        Stake USDC to unlock insurance coverage
        
        Args:
            usd: Amount of USDC to stake (minimum $100)
            
        Returns:
            Transaction hash
        """
        if usd < 100:
            raise ValueError("Minimum stake is $100 USDC")
        
        return self.insurance.stake_for_insurance(usd, self._private_key)
    
    def unstake_request(self) -> str:
        """
        Request to unstake (7-day delay required)
        
        Returns:
            Transaction hash
        """
        account = self.w3.eth.account.from_key(self._private_key)
        
        tx = self.insurance.staking.functions.requestUnstake().build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 150000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, self._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    
    def unstake_execute(self) -> str:
        """
        Execute unstake after 7-day delay
        
        Returns:
            Transaction hash
        """
        account = self.w3.eth.account.from_key(self._private_key)
        
        tx = self.insurance.staking.functions.executeUnstake().build_transaction({
            'from': account.address,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': 150000,
            'maxFeePerGas': self.w3.to_wei('0.1', 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei('0.001', 'gwei'),
        })
        
        signed = self.w3.eth.account.sign_transaction(tx, self._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    
    def is_covered(self, amount: Optional[float] = None) -> bool:
        """
        Check if agent has sufficient insurance coverage
        
        Args:
            amount: Optional specific amount to check against
            
        Returns:
            True if agent has adequate coverage
        """
        return self.insurance.is_covered(self.address, amount)
    
    def coverage_info(self) -> Dict[str, Any]:
        """
        Get detailed coverage information
        
        Returns:
            Dictionary with coverage details
        """
        return self.insurance.get_agent_coverage_info(self.address)
    
    def registry_status(self) -> Dict[str, Any]:
        """
        Get agent's status in LobSec Registry
        
        Returns:
            Dictionary with registry status
        """
        return self.registry.get_agent_status(self.address)
    
    def get_premium_quote(
        self,
        coverage_amount: float,
        duration_days: int
    ) -> Dict[str, Any]:
        """
        Get a premium quote for coverage
        
        Args:
            coverage_amount: Desired coverage amount in USD
            duration_days: Coverage duration in days
            
        Returns:
            Dictionary with quote details
        """
        base_premium = self.insurance.calculate_premium(
            coverage_amount,
            duration_days,
            risk_score=1000
        )
        
        # Check for immunization discount
        registry_status = self.registry_status()
        discount = 0.5 if registry_status.get("immunized") else 0.0
        final_premium = base_premium * (1 - discount)
        
        return {
            "coverage_amount_usd": coverage_amount,
            "duration_days": duration_days,
            "base_premium_usd": round(base_premium, 2),
            "discount_percent": discount * 100,
            "final_premium_usd": round(final_premium, 2),
            "immunized": registry_status.get("immunized", False)
        }
    
    def purchase_coverage(
        self,
        protocol_address: str,
        amount: float,
        duration_days: int
    ) -> str:
        """
        Purchase coverage for this agent
        
        Args:
            protocol_address: Address of protocol purchasing coverage
            amount: Coverage amount in USD
            duration_days: Duration in days
            
        Returns:
            Transaction hash
        """
        # Calculate risk score based on registry status
        registry_status = self.registry_status()
        risk_score = 500 if registry_status.get("immunized") else 1000
        
        return self.insurance.purchase_coverage(
            agent_address=self.address,
            protocol_address=protocol_address,
            amount=amount,
            duration_days=duration_days,
            private_key=self._private_key,
            risk_score=risk_score
        )
    
    def __repr__(self) -> str:
        return f"<LobSecAgent address={self.address}>"
