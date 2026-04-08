import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIG VARS ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")
LOG_GROUP = int(os.environ.get("LOG_GROUP", 0))
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

START_IMG = os.environ.get("START_IMG", "https://telegra.ph/file/79965a3d00f7b0f68800a.jpg")
SUPPORT_GRP = os.environ.get("SUPPORT_GRP", "https://t.me/your_group")
BOT_CHANNEL = os.environ.get("BOT_CHANNEL", "https://t.me/your_channel")
OWNER_LINK = os.environ.get("OWNER_LINK", "https://t.me/your_username")

# MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["cro_bot_db"]
users_col = db["users"]
groups_col = db["groups"]

app = Client("izah_et_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

active_games = {} 

# --- SÖZ BAZASI (DƏYİŞİLMƏDİ) ---
words = {
    "tarix": ["Atabəylər", "Şah İsmayıl", "Nadir Şah", "Çaldıran döyüşü", "Tomris", "Babək", "Cavanşir", "M.Ə.Rəsulzadə", "Şah Abbas", "Gülüstan müqaviləsi", "Türkmənçay müqaviləsi", "Səfəvilər", "Hülakülər", "Səlcuqlular", "Osmanlı", "Napoleon", "Hitler", "Atatürk", "Xətai", "Qara Qoyunlu", "Ağ Qoyunlu", "Şirvanşahlar", "Dərbənd", "Xəzər Xaqanlığı", "Atropatena", "Albaniya", "Manna", "Sümerlər", "Misir piramidaları", "Roma İmperiyası", "Yulius Sezar", "Spartak", "Çingiz Xan", "Əmir Teymur", "Sultan Süleyman", "Fatih Sultan Mehmet", "Məlhəmə döyüşü", "İkinci Dünya Müharibəsi", "Qarabağ müharibəsi", "Şuşa bəyannaməsi", "Naxçıvan xanlığı", "Cavad xan", "Pənahəli xan", "Xurşidbanu Natəvan", "Mirzə Fətəli Axundov", "Nizami Gəncəvi", "Füzuli", "Nəsimi", "Dədə Qorqud", "Koroğlu", "Qaçaq Nəbi", "Zəngəzur", "İrəvan xanlığı", "Bakı xanlığı", "Gəncə mühasirəsi", "20 Yanvar", "Xocalı soyqırımı", "ADR", "Vikinqlər", "Raqnar Lodbrok", "Alfred Veliki", "Uhtred", "Ekskalibur", "Qızıl Orda", "Monqollar", "Səlib yürüşləri", "Renessans", "Fransız inqilabı", "Sənaye inqilabı", "Kolumb", "Magellan", "Vasko da Qama", "Da Vinçi", "Eynşteyn", "Nyuton", "Arximed", "Pifaqor", "Sokrat", "Platon", "Aristotel", "Böyük İskəndər", "Dara", "Hannibal", "Alparslan", "Malazgird döyüşü", "Ertuğrul Qazi", "Osman Qazi", "Şah Təhmasib", "Zərdabi", "A.Bakıxanov", "Əhməd Cavad", "Üzeyir Hacıbəyov", "Lütfi Zadə", "Heydər Əliyev", "İlham Əliyev", "Zəfər Günü", "Xudafərin", "Araz", "Kür", "Göyçə", "Borçalı", "Təbriz", "Ərdəbil", "Urmiya", "Zənjan", "Qəzvin", "Həmədan", "Marağa", "Xoy", "Maku", "Quba xanlığı", "Şəki xanlığı", "Hacı Çələbi", "Fətəli xan", "İbrahimxəlil xan", "Vaqif", "Vidadi", "Molla Nəsrəddin", "Sabir", "Cavid", "Müşfiq", "Vurğun", "Şəhriyar", "B.Vahabzadə", "Xəlil Rza", "Məmməd Araz", "İsmayıl Şıxlı", "Anar", "Elçin", "Çingiz Abdullayev", "Mesopotamiya", "Babil", "Hammurapi qanunları", "Assuriya", "Urartu", "Mediya", "Əhəmənilər", "Parfiya", "Bizans", "Frank dövləti", "I Pyotr", "II Yekaterina", "I Dünya Müharibəsi", "Mudros barışığı", "Sevr müqaviləsi", "Lozan müqaviləsi", "Soyuq müharibə", "SSRİ", "NATO", "Varşava müqaviləsi", "BMT", "UNESCO", "İslam Həmrəyliyi"],
    "cografiya": ["Everest", "Amazon", "Xəzər dənizi", "Bakı", "Gəncə", "Sumqayıt", "Naxçıvan", "Lənkəran", "Şəki", "Quba", "Şuşa", "Kəlbəcər", "Ağdam", "Füzuli", "Cəbrayıl", "Zəngilan", "Qubadlı", "Laçın", "Xocalı", "Xocavənd", "Ağdərə", "Xankəndi", "Böyük Qafqaz", "Kiçik Qafqaz", "Murovdağ", "Şahdağ", "Tufandağ", "Bazardüzü", "Kür çayı", "Araz çayı", "Qanıx", "Qabırrı", "Tərtər çayı", "Ağstafa çayı", "Göy Göl", "Maral Göl", "Batabat", "Ceyranbatan", "Mingəçevir", "Abşeron", "Səhra", "Savanna", "Tayqa", "Tundra", "Cəngəllik", "Sakit Okean", "Atlantik Okean", "Hind Okeanı", "Antarktida", "Avstraliya", "Afrika", "Avropa", "Asiya", "Şimali Amerika", "Cənubi Amerika", "Nil çayı", "Missisipi", "Yantszı", "Yenisey", "Volqa", "Dunay", "Alp dağları", "And dağları", "Himalay", "Ural dağları", "Böyük Səhra", "Qobi", "Qaraqum", "Qızılqum", "Atakama", "Viktoriya şəlaləsi", "Niqara", "Anxel", "Baykal gölü", "Egey dənizi", "Aralıq dənizi", "Qara dəniz", "Qırmızı dəniz", "Ölü dəniz", "Cəbəllüttariq", "Süveyş kanalı", "Panama kanalı", "İstanbul boğazı", "Dardanel", "Yaponiya", "Çin", "Hindistan", "Rusiya", "Türkiyə", "İran", "Gürcüstan", "Fransa", "Almaniya", "İtaliya", "İspaniya", "ABŞ", "Kanada", "Braziliya", "Argentina", "Misir", "Pakistan", "İndoneziya", "Meksika", "Qazaxıstan", "Özbəkistan", "Tbilisi", "Ankara", "Moskva", "London", "Paris", "Berlin", "Roma", "Madrid", "Vaşinqton", "Tokio", "Pekin", "Qahirə", "Astana", "Daşkənd", "Ekvator", "Meridian", "Paralel", "Enlik", "Uzunluq", "Xəritə", "Qlobus", "Kompas", "Azimut", "Relyef", "İqlim", "Atmosfer", "Litosfer", "Hidrosfer", "Biosfer", "Maqma", "Vulkan", "Zəlzələ", "Cunami", "Geyser", "Stalaktit", "Stalaqmit", "Arxipelaq", "Ada", "Yarımada", "Körfəz", "Boğaz", "Dərə", "Kanyon", "Plato", "Oazis", "Musson", "Passat", "Siklon", "Antisiklon", "Barometr", "Hiqrometr", "Termometr", "Anemometr", "Seysmoqraf", "Radiasiya", "Ozon qatı", "Urbanizasiya"],
    "insan_adlari": ["Xəyal", "Əli", "Zəhra", "Murad", "Leyla", "Aysu", "Kənan", "Nigar", "Orxan", "Fidan", "Rəşad", "Günay", "Elvin", "Aytən", "Vüsal", "Sevinc", "Tural", "Arzu", "Emin", "Nərmin", "Anar", "Lalə", "Samir", "Aysel", "Rauf", "Gültən", "İlqar", "Pərvin", "Zaur", "Aynur", "Eldar", "Ülviyyə", "Nicat", "Səbinə", "Fuad", "Elnarə", "Rövşən", "Türkan", "Namiq", "Könül", "İlkin", "Səidə", "Ayxan", "Nisə", "Tofiq", "Bəsti", "Ramil", "Dilarə", "Seymur", "Elmira", "Pəviz", "Jasmin", "Aqil", "Nəzrin", "Şahin", "Fatimə", "Cavid", "Xədicə", "Taleh", "Mədinə", "Mənsur", "Rəna", "Üzeyir", "Sona", "Babək", "Banu", "İbrahim", "Zeynəb", "Hüseyn", "Gülnar", "Həsən", "Nailə", "Kamran", "Esmira", "Fariz", "Məryəm", "Azər", "Şəbnəm", "Nurlan", "Gülər", "Pənah", "Afaq", "Teymur", "Səid", "Yusif", "Sara", "Adil", "Fəridə", "Asif", "Ləman", "Vasif", "Nərgiz", "Hikmət", "Səmayə", "Musa", "Həvva", "İsa", "Məsumə", "Yəhya", "Asya", "İsmayıl", "Gülşən", "Osman", "Fərhad", "Şirin", "Məcnun", "Leyli", "Kərəm", "Əsli", "Səməd", "Vurğun", "Mikayıl", "Müşfiq", "Hüseyn Javid", "Nəbi", "Xəzər", "Araz", "Göyçə", "Zəngəzur", "Təbriz", "Bakı", "Polad", "Mübariz", "İlqar", "Şükür", "Xudayar", "Cəbrayıl", "Yalçın", "Elşən", "Afət", "Nadir", "Sultan", "Məhəmməd", "Ömər", "Osman", "Abbas", "Cəfər", "Kazım", "Rza", "Taqi", "Naqi", "Mehdi", "Zəki", "Bəxtiyar", "Vidadi", "Vaqif", "Zakir", "Hadi", "Səhənd", "Səməndər", "Tərlan", "Şahin", "Laçın", "Toğrul", "Çingiz", "Elman", "Rüstəm", "Zöhrab", "Siyavuş", "Esmira", "Solmaz"],
    "qarisig": ["Telefon", "Kitab", "Təyyarə", "Futbol", "Musiqi", "Televizor", "Kompüter", "Soyuducu", "Maşın", "Velosiped", "Saat", "Eynək", "Qələm", "Dəftər", "Çanta", "Ayaqqabı", "Paltar", "Yataq", "Masa", "Kürsü", "Pəncərə", "Qapı", "Divar", "Həyət", "Bağça", "Gül", "Ağaç", "Günəş", "Ay", "Ulduz", "Bulud", "Yağış", "Qar", "Külək", "Şimşək", "Dəniz", "Çay", "Dağ", "Meşə", "Yol", "Körpü", "Bina", "Məktəb", "Xəstəxana", "Aptek", "Market", "Restoran", "Kino", "Teatr", "Muzey", "Park", "Heyvanxana", "Pişik", "İt", "At", "İnək", "Qoyun", "Toyuq", "Quş", "Balıq", "Arı", "Kəpənək", "Alma", "Armud", "Nar", "Üzüm", "Banan", "Limon", "Kartof", "Soğan", "Pomidor", "Xiyar", "Çörək", "Su", "Çay", "Qəhvə", "Süd", "Şirə", "Dondurma", "Şokolad", "Konfet", "Tort", "Pizza", "Burger", "Kabab", "Plov", "Dovğa", "Həkim", "Müəllim", "Mühəndis", "Polis", "Əsgər", "Sürücü", "Aşpaz", "Rəssam", "Müğənni", "Aktyor", "Futbolçu", "Şahmat", "Tennis", "Voleybol", "Basketbol", "Üzgüçülük", "Boks", "Güləş", "Karate", "Gitara", "Pianino", "Tar", "Kamança", "Saz", "Radio", "Kamera", "Batareya", "Lampa", "Ütü", "Tozsoran", "Fen", "Tərəzi", "Mikroskop", "Teleskop", "Reket", "Peyk", "Raket", "Kosmos", "Planet", "Mars", "Yupiter", "Qara dəlik", "Qalaktika", "Uçan boşqab"]
}

async def add_point(user, chat_id=None, chat_title="Naməlum Qrup"):
    await users_col.update_one({"user_id": user.id}, {"$inc": {"points": 5}, "$set": {"name": user.first_name}}, upsert=True)
    if chat_id:
        # None yazmasın deyə chat_title yoxlanılır
        title = chat_title if chat_title else "Qrup"
        await groups_col.update_one(
            {"group_id": chat_id, "user_id": user.id}, 
            {"$inc": {"points": 5}, "$set": {"name": user.first_name, "group_name": title}}, 
            upsert=True
        )

# --- MESAJ YOXLIYAN ---
@app.on_message(filters.text & filters.group, group=1)
async def check_word(client, message):
    chat_id = message.chat.id
    if chat_id in active_games:
        game_data = active_games[chat_id]
        if not game_data.get('apariçi'): return 
        correct_word = game_data['word'].lower()
        if message.from_user.id == game_data['apariçi']:
            if message.text.lower() == correct_word:
                try: await message.delete()
                except: pass
                await message.reply(f"🚫 {message.from_user.mention}, sözü qrupa yaza bilməzsiniz!")
            return 
        if message.text.lower() == correct_word:
            user = message.from_user
            await add_point(user, chat_id, message.chat.title)
            mode, cat = game_data['mode'], game_data['cat']
            new_word = random.choice(words[cat])
            if mode == "chat":
                active_games[chat_id] = {"word": new_word, "apariçi": user.id, "mode": "chat", "cat": cat}
                text = f"🎉 {user.mention} tapdı: **{correct_word.capitalize()}**\nYeni aparıcı odur!"
            else:
                active_games[chat_id]['word'] = new_word
                text = f"🎊 {user.mention} tapdı: **{correct_word.capitalize()}**\nAparıcı davam edir!"
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("Sözə Baxmaq 🔍", callback_data=f"look_{new_word}")],
                [InlineKeyboardButton("İmtina ❌", callback_data="imtina")],
                [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]
            ])
            await message.reply(text, reply_markup=kb)

# --- KÖMƏK VƏ KOMANDALAR MƏTNİ ---
HELP_TEXT = (
    "🚀 **Botun Komandaları və İzahları:**\n\n"
    "🔹 `/start` - Botu işə salar və menyunu göstərər.\n"
    "🔹 `/game` - Qrupda yeni Cro oyunu başladar.\n"
    "🔹 `/reyting` - Ümumi, qrup və top qruplar reytinqi.\n"
    "🔹 `/myreyting` - Sizin şəxsi xalınızı göstərər.\n"
    "🔹 `/komekcro` - Bu kömək menyusunu açar.\n\n"
    "💡 **Qayda:** Aparıcı sözü tapana qədər izah etməlidir, amma sözün özünü yazmaq qadağandır!"
)

# --- START MESAJI ---
@app.on_message(filters.command("start"))
async def start(client, message):
    bot = await client.get_me()
    m = await message.reply("⚙️ **Yüklənir...**")
    await asyncio.sleep(0.4); await m.delete()
    
    text = (
        f"✨ **Salam, mən {bot.first_name}!**\n\n"
        "🎮 Mən qruplarda **Səssiz Sinema (Cro)** oynadan əyləncəli botam.\n"
        "Aparıcı sözü izah edir, digərləri tapmağa çalışır.\n\n"
        "/komekcro **yazaraq komutlar haqqında məlumat əldə edə bilərsiniz**"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")],
        [InlineKeyboardButton("📜 Komandalar", callback_data="help_menu"), InlineKeyboardButton("🏆 Reyting", callback_data="back_rating")],
        [InlineKeyboardButton("⚔️ Digər botlar", url=BOT_CHANNEL), InlineKeyboardButton("👩🏻‍💻 𝐨𝐰𝐧𝐞𝐫𝐚", url=OWNER_LINK)]
    ])
    await message.reply_photo(photo=START_IMG, caption=text, reply_markup=kb)

@app.on_message(filters.command("komekcro"))
async def help_cmd(client, message):
    await message.reply(HELP_TEXT)

@app.on_message(filters.command("myreyting"))
async def my_rank(client, message):
    user = await users_col.find_one({"user_id": message.from_user.id})
    points = user['points'] if user else 0
    text = f"👤 **Sizin Reytinqiniz:**\n\n🏆 Toplam xalınız: **{points}**\n\nDaha çox xal üçün qruplarda Cro oynayın!"
    try: await client.send_message(message.from_user.id, text)
    except: await message.reply("❌ Zəhmət olmasa botun şəxisinə yazıb '/start' verin ki, sizə mesaj göndərə bilim.")

@app.on_message(filters.command("reyting"))
async def rating_cmd(client, message):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Qrup Reytinqi", callback_data="group_rank"), InlineKeyboardButton("📊 Ümumi Reytinq", callback_data="global_rank")],
        [InlineKeyboardButton("📕 Top Qruplar", callback_data="top_groups")]
    ])
    await message.reply("📊 **Reytinq Menyusu**\nBaxmaq istədiyiniz bölməni seçin:", reply_markup=kb)

# --- OYUN MENYUSU ---
@app.on_message(filters.command(["game", "menu", "crostart"]) & filters.group)
async def menu_cmd(client, message):
    if message.chat.id in active_games:
        return await message.reply("⚠️ **Aktiv oyun var!** Bitməsini və ya imtinanı gözləyin.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Chatda Cro", callback_data="sel_chat"), InlineKeyboardButton("🎤 Səslidə Cro", callback_data="sel_voice")]
    ])
    await message.reply("🎮 **Səssiz Sinema (Cro)**\nHansı rejimdə oynamaq istəyirsiniz?\n\n💬 *Chat:* Tapan yeni aparıcı olur.\n🎙 *Səsli:* Aparıcı sabit qalır.", reply_markup=kb)

# --- CALLBACKS ---
@app.on_callback_query()
async def queries(client, callback_query: CallbackQuery):
    data, user, cid = callback_query.data, callback_query.from_user, callback_query.message.chat.id

    if data == "help_menu":
        await callback_query.edit_message_caption(caption=HELP_TEXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_start")]]))

    elif data == "global_rank":
        top = await users_col.find().sort("points", -1).limit(10).to_list(10)
        text = "🌍 **Ümumi Reytinqlər:**\n\n" + "\n".join([f"{i}. {u['name']} — {u['points']} xal" for i, u in enumerate(top, 1)])
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "group_rank":
        top = await groups_col.find({"group_id": cid}).sort("points", -1).limit(10).to_list(10)
        text = "📈 **Qrup üzrə Reytinqlər:**\n\n" + "\n".join([f"{i}. {u['name']} — {u['points']} xal" for i, u in enumerate(top, 1)])
        await callback_query.edit_message_text(text if top else "Xal yoxdur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "top_groups":
        pipeline = [{"$group": {"_id": "$group_id", "total": {"$sum": "$points"}, "n": {"$first": "$group_name"}}}, {"$sort": {"total": -1}}, {"$limit": 10}]
        top_g = await groups_col.aggregate(pipeline).to_list(10)
        text = "📕 **Ən Aktiv Qruplar:**\n\n"
        for i, g in enumerate(top_g, 1):
            name = g['n'] if g['n'] else "Gizli Qrup" # None problemi burada həll olundu
            text += f"{i}. {name} — {g['total']} xal\n"
        await callback_query.edit_message_text(text if top_g else "Aktiv qrup yoxdur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "back_rating":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📈 Qrup", callback_data="group_rank"), InlineKeyboardButton("📊 Ümumi", callback_data="global_rank")], [InlineKeyboardButton("📕 Top Qruplar", callback_data="top_groups")], [InlineKeyboardButton("⬅️ Ana Menyu", callback_data="back_start")]])
        if callback_query.message.photo: await callback_query.edit_message_caption(caption="📊 Reytinq bölməsi:", reply_markup=kb)
        else: await callback_query.edit_message_text("📊 Reytinq bölməsi:", reply_markup=kb)

    elif data == "back_start":
        bot = await client.get_me()
        text = f"✨ **Salam, mən {bot.first_name}!**\n\nOynamaq üçün məni qrupa əlavə et!"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")], [InlineKeyboardButton("📜 Komandalar", callback_data="help_menu"), InlineKeyboardButton("🏆 Reyting", callback_data="back_rating")]])
        if callback_query.message.photo: await callback_query.edit_message_caption(caption=text, reply_markup=kb)
        else: await start(client, callback_query.message)

    elif data.startswith("sel_"):
        mode = data.replace("sel_", "")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🌀 Qarışıq", callback_data=f"set_{mode}_qarisig")], [InlineKeyboardButton("📜 Tarix", callback_data=f"set_{mode}_tarix"), InlineKeyboardButton("🌍 Coğrafiya", callback_data=f"set_{mode}_cografiya")], [InlineKeyboardButton("👥 Adlar", callback_data=f"set_{mode}_insan_adlari")]])
        await callback_query.edit_message_text(f"📂 Mod: {mode.capitalize()}\nKateqoriya seçin:", reply_markup=kb)

    elif data.startswith("set_"):
        parts = data.split("_")
        mode, cat = parts[1], "_".join(parts[2:])
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🙋‍♂️ Mən Aparıcı Olum", callback_data=f"run_{mode}_{cat}")]])
        await callback_query.edit_message_text(f"✅ Kateqoriya: {cat.upper()}\nKim izah edəcək?", reply_markup=kb)

    elif data.startswith("run_"):
        parts = data.split("_")
        mode, cat = parts[1], "_".join(parts[2:])
        word = random.choice(words[cat])
        active_games[cid] = {"word": word, "apariçi": user.id, "mode": mode, "cat": cat}
        await client.answer_callback_query(callback_query.id, text=f"🎯 Sözün: {word}", show_alert=True)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{word}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]])
        await callback_query.edit_message_text(f"🎤 {user.mention} izah edir!", reply_markup=kb)

    elif data.startswith("next_"):
        parts = data.split("_")
        mode, cat = parts[-1], "_".join(parts[1:-1])
        if cid in active_games and user.id != active_games[cid]['apariçi']:
            return await callback_query.answer("Yalnız aparıcı!", show_alert=True)
        word = random.choice(words[cat]); active_games[cid]['word'] = word
        await callback_query.answer(f"🔄 Yeni: {word}", show_alert=True)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{word}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]])
        await callback_query.edit_message_text(f"🎤 {user.mention} yeni sözü izah edir!", reply_markup=kb)

    elif data.startswith("look_"):
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            await callback_query.answer(f"🎯 Sözün: {active_games[cid]['word']}", show_alert=True)
        else: await callback_query.answer("Yalnız aparıcı!", show_alert=True)

    elif data == "imtina":
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            active_games[cid]['apariçi'] = None 
            await callback_query.edit_message_text(f"👤 {user.mention} imtina etdi. Kim davam edər?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎤 Mən Olum", callback_data="take_lead")]]))
        else: await callback_query.answer("Yalnız aparıcı!", show_alert=True)

    elif data == "take_lead":
        if cid in active_games and active_games[cid]['apariçi'] is None:
            active_games[cid]['apariçi'] = user.id
            w, c, m = active_games[cid]['word'], active_games[cid]['cat'], active_games[cid]['mode']
            await callback_query.answer(f"🎯 Sözün: {w}", show_alert=True)
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{w}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]
            ])
            await message.reply(text, reply_markup=kb)

# --- KÖMƏK VƏ KOMANDALAR MƏTNİ ---
HELP_TEXT = (
    "🚀 **Botun Komandaları və İzahları:**\n\n"
    "🔹 `/start` - Botu işə salar və menyunu göstərər.\n"
    "🔹 `/game` - Qrupda yeni Cro oyunu başladar.\n"
    "🔹 `/reyting` - Ümumi, qrup və top qruplar reytinqi.\n"
    "🔹 `/myreyting` - Sizin şəxsi xalınızı göstərər.\n"
    "🔹 `/komekcro` - Bu kömək menyusunu açar.\n\n"
    "💡 **Qayda:** Aparıcı sözü tapana qədər izah etməlidir, amma sözün özünü yazmaq qadağandır!"
)

# --- START MESAJI ---
@app.on_message(filters.command("start"))
async def start(client, message):
    bot = await client.get_me()
    m = await message.reply("⚙️ **Yüklənir...**")
    await asyncio.sleep(0.4); await m.delete()
    
    text = (
        f"✨ **Salam, mən {bot.first_name}!**\n\n"
        "🎮 Mən qruplarda **Səssiz Sinema (Cro)** oynadan əyləncəli botam.\n"
        "Aparıcı sözü izah edir, digərləri tapmağa çalışır.\n\n"
        "👇 Aşağıdakı düymələrdən istifadə edə bilərsiniz:"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")],
        [InlineKeyboardButton("📜 Komandalar", callback_data="help_menu"), InlineKeyboardButton("🏆 Reyting", callback_data="back_rating")],
        [InlineKeyboardButton("📢 Kanal", url=BOT_CHANNEL), InlineKeyboardButton("👤 Sahib", url=OWNER_LINK)]
    ])
    await message.reply_photo(photo=START_IMG, caption=text, reply_markup=kb)

@app.on_message(filters.command("komekcro"))
async def help_cmd(client, message):
    await message.reply(HELP_TEXT)

@app.on_message(filters.command("myreyting"))
async def my_rank(client, message):
    user = await users_col.find_one({"user_id": message.from_user.id})
    points = user['points'] if user else 0
    text = f"👤 **Sizin Reytinqiniz:**\n\n🏆 Toplam xalınız: **{points}**\n\nDaha çox xal üçün qruplarda Cro oynayın!"
    try: await client.send_message(message.from_user.id, text)
    except: await message.reply("❌ Zəhmət olmasa botun şəxisinə yazıb '/start' verin ki, sizə mesaj göndərə bilim.")

@app.on_message(filters.command("reyting"))
async def rating_cmd(client, message):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Qrup Reytinqi", callback_data="group_rank"), InlineKeyboardButton("📊 Ümumi Reytinq", callback_data="global_rank")],
        [InlineKeyboardButton("📕 Top Qruplar", callback_data="top_groups")]
    ])
    await message.reply("📊 **Reytinq Menyusu**\nBaxmaq istədiyiniz bölməni seçin:", reply_markup=kb)

# --- OYUN MENYUSU ---
@app.on_message(filters.command(["game", "menu", "crostart"]) & filters.group)
async def menu_cmd(client, message):
    if message.chat.id in active_games:
        return await message.reply("⚠️ **Aktiv oyun var!** Bitməsini və ya imtinanı gözləyin.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Chatda Cro", callback_data="sel_chat"), InlineKeyboardButton("🎤 Səslidə Cro", callback_data="sel_voice")]
    ])
    await message.reply("🎮 **Səssiz Sinema (Cro)**\nHansı rejimdə oynamaq istəyirsiniz?\n\n💬 *Chat:* Tapan yeni aparıcı olur.\n🎙 *Səsli:* Aparıcı sabit qalır.", reply_markup=kb)

# --- CALLBACKS ---
@app.on_callback_query()
async def queries(client, callback_query: CallbackQuery):
    data, user, cid = callback_query.data, callback_query.from_user, callback_query.message.chat.id

    if data == "help_menu":
        await callback_query.edit_message_caption(caption=HELP_TEXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_start")]]))

    elif data == "global_rank":
        top = await users_col.find().sort("points", -1).limit(10).to_list(10)
        text = "🌍 **Ümumi Reytinqlər:**\n\n" + "\n".join([f"{i}. {u['name']} — {u['points']} xal" for i, u in enumerate(top, 1)])
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "group_rank":
        top = await groups_col.find({"group_id": cid}).sort("points", -1).limit(10).to_list(10)
        text = "📈 **Qrup üzrə Reytinqlər:**\n\n" + "\n".join([f"{i}. {u['name']} — {u['points']} xal" for i, u in enumerate(top, 1)])
        await callback_query.edit_message_text(text if top else "Xal yoxdur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "top_groups":
        pipeline = [{"$group": {"_id": "$group_id", "total": {"$sum": "$points"}, "n": {"$first": "$group_name"}}}, {"$sort": {"total": -1}}, {"$limit": 10}]
        top_g = await groups_col.aggregate(pipeline).to_list(10)
        text = "📕 **Ən Aktiv Qruplar:**\n\n"
        for i, g in enumerate(top_g, 1):
            name = g['n'] if g['n'] else "Gizli Qrup"
            text += f"{i}. {name} — {g['total']} xal\n"
        await callback_query.edit_message_text(text if top_g else "Aktiv qrup yoxdur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_rating")]]))

    elif data == "back_rating":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📈 Qrup", callback_data="group_rank"), InlineKeyboardButton("📊 Ümumi", callback_data="global_rank")], [InlineKeyboardButton("📕 Top Qruplar", callback_data="top_groups")], [InlineKeyboardButton("⬅️ Ana Menyu", callback_data="back_start")]])
        if callback_query.message.photo: await callback_query.edit_message_caption(caption="📊 Reytinq bölməsi:", reply_markup=kb)
        else: await callback_query.edit_message_text("📊 Reytinq bölməsi:", reply_markup=kb)

    elif data == "back_start":
        bot = await client.get_me()
        text = f"✨ **Salam, mən {bot.first_name}!**\n\nOynamaq üçün məni qrupa əlavə et!"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")], [InlineKeyboardButton("📜 Komandalar", callback_data="help_menu"), InlineKeyboardButton("🏆 Reyting", callback_data="back_rating")]])
        if callback_query.message.photo: await callback_query.edit_message_caption(caption=text, reply_markup=kb)
        else: await start(client, callback_query.message)

    elif data.startswith("sel_"):
        mode = data.replace("sel_", "")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🌀 Qarışıq", callback_data=f"set_{mode}_qarisig")], [InlineKeyboardButton("📜 Tarix", callback_data=f"set_{mode}_tarix"), InlineKeyboardButton("🌍 Coğrafiya", callback_data=f"set_{mode}_cografiya")], [InlineKeyboardButton("👥 Adlar", callback_data=f"set_{mode}_insan_adlari")]])
        await callback_query.edit_message_text(f"📂 Mod: {mode.capitalize()}\nKateqoriya seçin:", reply_markup=kb)

    elif data.startswith("set_"):
        parts = data.split("_")
        mode, cat = parts[1], "_".join(parts[2:])
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🙋‍♂️ Mən Aparıcı Olum", callback_data=f"run_{mode}_{cat}")]])
        await callback_query.edit_message_text(f"✅ Kateqoriya: {cat.upper()}\nKim izah edəcək?", reply_markup=kb)

    elif data.startswith("run_"):
        parts = data.split("_")
        mode, cat = parts[1], "_".join(parts[2:])
        word = random.choice(words[cat])
        active_games[cid] = {"word": word, "apariçi": user.id, "mode": mode, "cat": cat}
        await client.answer_callback_query(callback_query.id, text=f"🎯 Sözün: {word}", show_alert=True)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{word}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]])
        await callback_query.edit_message_text(f"🎤 {user.mention} izah edir!", reply_markup=kb)

    elif data.startswith("next_"):
        parts = data.split("_")
        mode, cat = parts[-1], "_".join(parts[1:-1])
        if cid in active_games and user.id != active_games[cid]['apariçi']:
            return await callback_query.answer("Yalnız aparıcı!", show_alert=True)
        word = random.choice(words[cat]); active_games[cid]['word'] = word
        await callback_query.answer(f"🔄 Yeni: {word}", show_alert=True)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{word}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{cat}_{mode}")]])
        await callback_query.edit_message_text(f"🎤 {user.mention} yeni sözü izah edir!", reply_markup=kb)

    elif data.startswith("look_"):
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            await callback_query.answer(f"🎯 Sözün: {active_games[cid]['word']}", show_alert=True)
        else: await callback_query.answer("Yalnız aparıcı!", show_alert=True)

    elif data == "imtina":
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            active_games[cid]['apariçi'] = None 
            await callback_query.edit_message_text(f"👤 {user.mention} imtina etdi. Kim davam edər?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎤 Mən Olum", callback_data="take_lead")]]))
        else: await callback_query.answer("Yalnız aparıcı!", show_alert=True)

    elif data == "take_lead":
        if cid in active_games and active_games[cid]['apariçi'] is None:
            active_games[cid]['apariçi'] = user.id
            w, c, m = active_games[cid]['word'], active_games[cid]['cat'], active_games[cid]['mode']
            await callback_query.answer(f"🎯 Sözün: {w}", show_alert=True)
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("Sözə Bax 🔍", callback_data=f"look_{w}")], [InlineKeyboardButton("İmtina ❌", callback_data="imtina")], [InlineKeyboardButton("Növbeti ♻️", callback_data=f"next_{c}_{m}")]])
            await callback_query.edit_message_text(f"🎤 Yeni Aparıcı: {user.mention}", reply_markup=kb)

# --- İŞƏ SALMA ---
async def main():
    await app.start()
    await app.set_bot_commands([
        BotCommand("start", "Botu başladar"),
        BotCommand("game", "Yeni oyun başladar"),
        BotCommand("reyting", "Reytinq menyusu"),
        BotCommand("myreyting", "Şəxsi xalınız"),
        BotCommand("komekcro", "Kömək menyusu")
    ])
    print("🚀 HT-Cro Bot İşləyir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
