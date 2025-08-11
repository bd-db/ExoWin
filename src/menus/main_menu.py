from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from src.database import get_user
from src.utils.formatting import format_money

async def main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the main menu"""
    user_id = update.effective_user.id
    user = await get_user(user_id)
    
    message = (
        f"🎰 **ExoWin 👑** 🎰\n\n"
        f"💰 Balance: {format_money(user['balance'])}\n"
        f"🎮 Welcome back, {update.effective_user.first_name}!\n\n"
        f"Choose an option below:"
    )
    
    # Create the main menu keyboard matching Image 3
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play", callback_data="menu_games")
        ],
        [
            InlineKeyboardButton("💰 Deposit", callback_data="menu_deposit"),
            InlineKeyboardButton("💸 Withdraw", callback_data="menu_withdraw")
        ],
        [
            InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
            InlineKeyboardButton("🎁 Bonuses", callback_data="menu_bonuses")
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu callback queries"""
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    
    if len(data) < 2:
        return
    
    action = data[1]
    
    if action == "games":
        from .games_menu import show_games_menu
        await show_games_menu(update, context)
    
    elif action == "deposit":
        from .deposit_menu import show_deposit_menu
        await show_deposit_menu(update, context)
    
    elif action == "withdraw":
        from src.wallet.withdrawal_system import withdrawal_system
        await withdrawal_system.show_withdrawal_menu(update, context)
    
    elif action == "profile":
        from .profile_menu import show_profile_menu
        await show_profile_menu(update, context)
    
    elif action == "bonuses":
        from .bonuses_menu import show_bonuses_menu
        await show_bonuses_menu(update, context)
    
    elif action == "settings":
        from .settings_menu import show_settings_menu
        await show_settings_menu(update, context)
    
    elif action == "main":
        # Return to main menu
        await main_menu_command(update, context)

async def show_withdraw_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show withdrawal menu"""
    from src.database import can_withdraw
    
    user_id = update.callback_query.from_user.id
    user = await get_user(user_id)
    can_withdraw_funds = await can_withdraw(user_id)
    
    if not can_withdraw_funds:
        message = (
            "❌ **Withdrawal Not Available** ❌\n\n"
            f"💰 Current balance: {format_money(user['balance'])}\n\n"
            "You need at least **$50** to withdraw funds.\n"
            "Keep playing to increase your balance! 🎮"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("🔙 Back", callback_data="menu_main")
            ]
        ]
    else:
        message = (
            "💸 **Withdraw Funds** 💸\n\n"
            f"💰 Available balance: {format_money(user['balance'])}\n\n"
            "Select withdrawal method:"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("₿ Cryptocurrency", callback_data="withdraw_crypto")
            ],
            [
                InlineKeyboardButton("💳 Bank Transfer", callback_data="withdraw_bank"),
                InlineKeyboardButton("🏦 PayPal", callback_data="withdraw_paypal")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="menu_main")
            ]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')