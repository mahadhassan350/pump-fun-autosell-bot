# Auto-Sell Bot for Pump.fun

This is a modified version of the pump-fun-bot that automatically sells tokens after a 3-second delay when it detects your token creation or purchase on PumpFun.

## How It Works

1. The bot monitors the Solana blockchain for transactions related to the PumpFun program.
2. When it detects a token creation or purchase from your wallet, it waits for 3 seconds.
3. After the delay, it automatically sells the token.

## Setup Instructions

### 1. Install Dependencies

Make sure you have Python 3.9+ and all required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SOLANA_NODE_RPC_ENDPOINT=https://your-rpc-endpoint.com
SOLANA_NODE_WSS_ENDPOINT=wss://your-wss-endpoint.com
SOLANA_PRIVATE_KEY=your_private_key_here
YOUR_WALLET_ADDRESS=your_public_wallet_address_here
```

- Get RPC endpoints from providers like [QuickNode](https://www.quicknode.com/) or [Triton](https://triton.one/).
- Use the same wallet for both the bot and your manual PumpFun transactions.

### 3. Configure the Bot

Open `bots/auto-sell-bot.yaml` and make these adjustments:

1. Set your preferred slippage values for buys and sells.
2. Make sure `bro_address` is set to `${YOUR_WALLET_ADDRESS}`.
3. Verify that `wait_after_buy` is set to `3` (this is the delay in seconds).
4. Make sure `yolo_mode` is `true` for continuous monitoring.

### 4. Run the Bot

```bash
python -m src.bot_runner
```

Keep the bot running while you create or buy tokens on PumpFun. The bot will detect your transactions and automatically sell after the specified delay.

## Important Notes

- **Test with small amounts first!** Always verify the bot is working as expected before using larger amounts.
- The bot monitors for YOUR transactions, specified by the wallet address in `bro_address`.
- If the token price drops rapidly, the slippage setting becomes important - adjust it based on market conditions.
- The bot runs continuously in `yolo_mode`, watching for new transactions.

## Troubleshooting

- If the bot is not detecting your transactions, check that `YOUR_WALLET_ADDRESS` is correctly set.
- If sales are failing, try increasing the `sell_slippage` value.
- For better transaction confirmation speed, consider using a fast RPC provider and adjusting priority fees.

## Disclaimer

This bot is provided for educational purposes only. Trading crypto tokens involves significant risk. Use at your own risk. 