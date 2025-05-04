"""
Cleanup modes implementations for pump.fun token accounts management.
"""
from cleanup.account_closer import close_token_account
from cleanup.manager import AccountCleanupManager
from core.client import SolanaClient
from core.priority_fee.manager import PriorityFeeManager
from core.wallet import Wallet
from trading.base import TokenInfo
from utils.logger import get_logger

logger = get_logger(__name__)


def should_cleanup_after_failure(cleanup_mode) -> bool:
    return cleanup_mode == "on_fail"


def should_cleanup_after_sell(cleanup_mode) -> bool:
    return cleanup_mode == "after_sell"


def should_cleanup_post_session(cleanup_mode) -> bool:
    return cleanup_mode == "post_session"


async def handle_cleanup_after_failure(
        client, wallet, mint, priority_fee_manager, cleanup_mode, cleanup_with_prior_fee, force_burn
    ):
    if should_cleanup_after_failure(cleanup_mode):
        logger.info("[Cleanup] Triggered by failed buy transaction.")
        manager = AccountCleanupManager(client, wallet, priority_fee_manager, cleanup_with_prior_fee, force_burn)
        await manager.cleanup_ata(mint)

async def handle_cleanup_after_sell(
    client: SolanaClient, 
    wallet: Wallet, 
    token_info: TokenInfo,
    priority_fee_enabled: bool = False,
    priority_fee_manager: PriorityFeeManager = None,
) -> None:
    """Handle cleanup after a successful sell operation.
    
    Args:
        client: Solana client
        wallet: Wallet
        token_info: Token information
        priority_fee_enabled: Whether to use priority fee
        priority_fee_manager: Priority fee manager
    """
    
    mint = token_info.mint
    logger.info(f"Performing post-sell cleanup for mint: {mint}")
    
    # Close the token account
    try:
        associated_token_account = wallet.get_associated_token_address(mint)
        token_balance = await client.get_token_account_balance(associated_token_account)
        
        if token_balance == 0:
            logger.info(f"Closing empty token account for {mint}")
            priority_fee = None
            if priority_fee_enabled and priority_fee_manager is not None:
                priority_fee = await priority_fee_manager.calculate_priority_fee()
                
            close_result = await close_token_account(
                client, 
                wallet,
                mint,
                priority_fee=priority_fee
            )
            
            if close_result:
                logger.info(f"Successfully closed token account for {mint}")
            else:
                logger.error(f"Failed to close token account for {mint}")
        else:
            logger.warning(f"Token account still has balance: {token_balance}. Skipping close.")
    except Exception as e:
        logger.error(f"Error during post-sell cleanup: {e}")

async def handle_cleanup_post_session(
        client, wallet, mints, priority_fee_manager, cleanup_mode, cleanup_with_prior_fee, force_burn
    ):
    if should_cleanup_post_session(cleanup_mode):
        logger.info("[Cleanup] Triggered post trading session.")
        manager = AccountCleanupManager(client, wallet, priority_fee_manager, cleanup_with_prior_fee, force_burn)
        for mint in mints:
            await manager.cleanup_ata(mint)
