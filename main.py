
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# ============================================
# CONFIGURATION
# ============================================
TOKEN = "8661867566:A4HVg04yXsYI2tb0ZEW0cK5G3vzYH44hmvY"

if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found! Set it in Railway variables.")

# ============================================
# SETUP LOGGING
# ============================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# ARBITRAGE CALCULATION
# ============================================

def calculate_arbitrage(odds_a, odds_b, total_stake=10000):
    """Check for arbitrage in a 2-way market."""
    arb_pct = (1/odds_a) + (1/odds_b)
    
    if arb_pct < 1:
        profit_pct = (1 - arb_pct) * 100
        stake_a = (1/odds_a) / arb_pct * total_stake
        stake_b = total_stake - stake_a
        profit = stake_a * odds_a - total_stake
        
        return {
            'found': True,
            'profit_pct': round(profit_pct, 2),
            'profit_amount': round(profit, 2),
            'stake_a': round(stake_a, 2),
            'stake_b': round(stake_b, 2),
            'odds_a': odds_a,
            'odds_b': odds_b
        }
    return {'found': False}

# ============================================
# SAMPLE SCAN FUNCTION
# ============================================

def scan_for_arbitrage():
    """Scans for arbitrage using sample odds data."""
    
    # Sample odds (will be replaced with real data later)
    sample_matches = [
        {'match': 'Real Madrid vs Barcelona', 'market': 'GG/NG',
         'betpawa_gg': 2.15, 'betking_ng': 2.05},
        {'match': 'Man United vs Liverpool', 'market': 'Over/Under 2.5',
         'betpawa_over': 1.95, 'betking_under': 2.10},
    ]
    
    opportunities = []
    
    for match in sample_matches:
        if 'betpawa_gg' in match and 'betking_ng' in match:
            result = calculate_arbitrage(match['betpawa_gg'], match['betking_ng'])
            if result['found']:
                opportunities.append({
                    'match': match['match'],
                    'market': match['market'],
                    'outcome_a': 'Betpawa GG',
                    'outcome_b': 'Betking NG',
                    'odds_a': result['odds_a'],
                    'odds_b': result['odds_b'],
                    'stake_a': result['stake_a'],
                    'stake_b': result['stake_b'],
                    'profit_pct': result['profit_pct'],
                    'profit_amount': result['profit_amount']
                })
        
        if 'betpawa_over' in match and 'betking_under' in match:
            result = calculate_arbitrage(match['betpawa_over'], match['betking_under'])
            if result['found']:
                opportunities.append({
                    'match': match['match'],
                    'market': match['market'],
                    'outcome_a': 'Betpawa Over',
                    'outcome_b': 'Betking Under',
                    'odds_a': result['odds_a'],
                    'odds_b': result['odds_b'],
                    'stake_a': result['stake_a'],
                    'stake_b': result['stake_b'],
                    'profit_pct': result['profit_pct'],
                    'profit_amount': result['profit_amount']
                })
    
    return opportunities

# ============================================
# TELEGRAM COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Pre-Match Arbitrage Scanner**\n\n"
        "I scan Nigerian bookmakers for arbitrage opportunities.\n\n"
        "📌 **Commands:**\n"
        "/check - Scan for opportunities\n"
        "/status - Check bot status\n"
        "/help - Show help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **How to use:**\n\n"
        "1. Send /check to scan for arbitrage\n"
        "2. If found, I'll show you stakes and profit\n"
        "3. You manually place bets on both sites\n"
        "4. Profit is guaranteed!\n\n"
        "💰 With ₦10,000 stake, you can make ₦100-₦500 per bet!"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ **Bot is running!**\n\n"
        "🔄 Monitoring pre-match odds\n"
        "📊 Bookmakers: Betpawa, Betking\n"
        "💰 Use /check to scan!"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Scanning for arbitrage opportunities...")
    
    opportunities = scan_for_arbitrage()
    
    if opportunities:
        for opp in opportunities:
            message = (
                f"💰 **ARBITRAGE FOUND!**\n\n"
                f"⚽ {opp['match']}\n"
                f"📊 {opp['market']}\n"
                f"📈 Profit: **{opp['profit_pct']}%** (₦{opp['profit_amount']:,.2f})\n\n"
                f"📱 **Place these bets:**\n"
                f"• ₦{opp['stake_a']:,.2f} on **{opp['outcome_a']}** @ {opp['odds_a']}\n"
                f"• ₦{opp['stake_b']:,.2f} on **{opp['outcome_b']}** @ {opp['odds_b']}\n\n"
                f"⚡ Act fast!"
            )
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("ℹ️ No arbitrage found at the moment.")

# ============================================
# MAIN
# ============================================

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("check", check))
    
    print("🤖 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
