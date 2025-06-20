from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройки расписания", callback_data="admin_schedule")],
            [InlineKeyboardButton(text="🔄 Сменить дежурного", callback_data="admin_change_duty")],
        ])