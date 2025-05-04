"""
Token account closing functionality.
"""
from solders.pubkey import Pubkey
from spl.token.instructions import close_account

from core.client import SolanaClient
from core.wallet import Wallet
from utils.logger import get_logger

logger = get_logger(__name__)

async def close_token_account(
    client: SolanaClient,
    wallet: Wallet,
    mint: Pubkey,
    priority_fee: int = None,
) -> bool:
    """
    Close an associated token account for a specific mint.
    
    Args:
        client: Solana client
        wallet: Wallet
        mint: Mint address
        priority_fee: Optional priority fee
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        associated_token_account = wallet.get_associated_token_address(mint)
        
        # Create close account instruction
        close_ix = close_account(
            associated_token_account,
            wallet.pubkey,
            wallet.pubkey
        )
        
        # Send and confirm transaction
        tx_signature = await client.build_and_send_transaction(
            [close_ix],
            wallet.keypair,
            skip_preflight=False,
            priority_fee=priority_fee
        )
        
        success = await client.confirm_transaction(tx_signature)
        
        if success:
            logger.info(f"Successfully closed token account: {tx_signature}")
            return True
        else:
            logger.error(f"Failed to close token account: {tx_signature}")
            return False
            
    except Exception as e:
        logger.error(f"Error closing token account: {e}")
        return False 