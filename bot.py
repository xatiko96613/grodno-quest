import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8602916944:AAHunW7H7pqrhJxY8ce3G7LfPTVTG3Ou6Y8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==================== НАСТРОЙКИ ====================
FINAL_CODE = "КЛЮЧ-ГРОДНО"
SECRET_CODE = "СИГНАЛ-2026"
WINNER_LIMIT = 10
WAITING = set()
FINISHED = False
winner_id = None

# ==================== ОСНОВНЫЕ КОМАНДЫ ====================

@dp.message(Command("start"))
async def start_cmd(msg: Message):
    await msg.answer(
        "📡 <b>СИГНАЛ ИЗ ГРОДНО</b>\n\n"
        "Ты подключился к городскому квесту. В Гродно спрятана капсула с 30 BYN. "
        "Твоя задача — пройти цепочку загадок и найти её первым.\n\n"
        "🔐 <b>Первая подсказка:</b>\n"
        "<i>«Ищи начало там, где каменный лев охраняет вход в прошлое. "
        "Под его взглядом — знак, начертанный мелом».</i>\n\n"
        "Дальше — сам. Город подскажет.\n\n"
        "Когда дойдёшь до контрольной точки — найдёшь кодовое слово. Отправь его сюда.",
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_cmd(msg: Message):
    await msg.answer(
        "<b>СИГНАЛ ИЗ ГРОДНО</b> — городской квест с призом 30 BYN.\n\n"
        "Команды:\n"
        "/start — начало игры\n"
        "/help — это сообщение\n"
        "/map — обрывки сигнала\n"
        "/prize — что в капсуле\n"
        "/rules — правила\n\n"
        "Больше ничего не нужно. Город подскажет остальное.",
        parse_mode="HTML"
    )

# ==================== ИГРОВАЯ ЛОГИКА ====================

@dp.message(lambda m: m.text and m.text.strip().upper() == SECRET_CODE)
async def join_final(msg: Message):
    global FINISHED
    if FINISHED:
        await msg.answer("Сигнал погас. Квест завершён. Но ты можешь успеть в следующий раз. Следи за анонсами.")
        return
    if msg.from_user.id in WAITING:
        await msg.answer("Ты уже в игре. Осталось немного. Жди сигнала.")
        return
    WAITING.add(msg.from_user.id)
    count = len(WAITING)
    await msg.answer(f"Ты в списке финалистов. Сейчас тебя <b>{count}/{WINNER_LIMIT}</b>.\n\n"
                     f"Жди. Как только наберётся {WINNER_LIMIT} человек — все получат координаты тайника одновременно. "
                     f"Действовать придётся быстро.",
                     parse_mode="HTML")
    if count >= WINNER_LIMIT:
        await start_final()

async def start_final():
    global FINISHED, WAITING, winner_id
    if FINISHED:
        return
    text = (
        "🏁 <b>ФИНАЛЬНАЯ ГОНКА</b>\n\n"
        "Внимание. Тайник здесь:\n"
        "📍 <b>Пруд-копанка на Ольшанке, бетонная плита у воды, восточная сторона.</b>\n\n"
        "В капсуле — 30 BYN и кодовое слово. Кто первым найдёт капсулу — пиши кодовое слово сюда. "
        "Остальным — удача в другой раз.\n\n"
        "Время пошло."
    )
    for uid in WAITING.copy():
        try:
            await bot.send_message(uid, text, parse_mode="HTML")
        except:
            pass

@dp.message(lambda m: m.text and m.text.strip().upper() == FINAL_CODE)
async def win(msg: Message):
    global FINISHED, winner_id
    if FINISHED:
        await msg.answer("Квест уже завершён.")
        return
    FINISHED = True
    winner_id = msg.from_user.id
    await msg.answer(
        "🎉 <b>Ты первый.</b>\n\n"
        "Приз твой — 30 BYN. Забери деньги из капсулы.\n\n"
        "Для подтверждения и связи с организатором напиши: <b>@Anubis96613</b>",
        parse_mode="HTML"
    )
    for uid in WAITING:
        if uid != winner_id:
            try:
                await bot.send_message(uid, "Квест завершён. Победитель уже забрал приз. Спасибо за участие. Следи за новыми сигналами.")
            except:
                pass
    WAITING.clear()

# ==================== ПАСХАЛКИ ====================

@dp.message(Command("map"))
async def map_cmd(msg: Message):
    await msg.answer(
        "🗺 <b>ОБРЫВКИ СИГНАЛА</b>\n\n"
        "1 — Новый замок. Лев. Мел.\n"
        "2 — Набережная. QR. Морзянка.\n"
        "3 — Серебряная игла. 24 шага на север.\n"
        "4 — Улица Ожешко. Плоский камень. Координаты.\n"
        "5 — Красная звезда. Изображение. Скрытый текст.\n"
        "6 — Ольшанка. Роща. Дерево с тремя стволами.\n\n"
        "Дойди до контрольной точки — найдёшь код для входа в финал.",
        parse_mode="HTML"
    )

@dp.message(Command("prize"))
async def prize_cmd(msg: Message):
    await msg.answer(
        "💰 Приз: 30 белорусских рублей. Наличные.\n"
        "Находятся в герметичной капсуле в финальном тайнике.\n"
        "Не в боте. Не у организатора. В городе. Реально."
    )

@dp.message(Command("rules"))
async def rules_cmd(msg: Message):
    await msg.answer(
        "📜 <b>ПРАВИЛА</b>\n\n"
        "1. Квест открыт для всех. Участие бесплатное.\n"
        "2. Все этапы расположены в общедоступных местах. Лезть в закрытые зоны, ломать, копать глубоко — не нужно.\n"
        "3. Будь осторожен. Смотри по сторонам. Головой отвечаешь сам.\n"
        "4. Приз забирает тот, кто первым найдёт капсулу и введёт верное кодовое слово боту.\n"
        "5. Организатор не даёт подсказок вне бота. Даже не проси.",
        parse_mode="HTML"
    )

# ==================== НЕИЗВЕСТНАЯ КОМАНДА ====================

@dp.message()
async def unknown(msg: Message):
    if msg.text and msg.text.strip().upper() in [SECRET_CODE, FINAL_CODE]:
        return
    await msg.answer("Ты пробуешь частоту. Тишина.\nМожет, попробуешь /help?")

# ==================== ЗАПУСК ====================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())