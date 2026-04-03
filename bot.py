import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIG VARS (TOXUNULMADI) ---
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

# MongoDB (TOXUNULMADI)
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["cro_bot_db"]
users_col = db["users"]
groups_col = db["groups"]

app = Client("izah_et_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Aktiv oyunlar
active_games = {} 

# --- SÖZ BAZASI (TAMDIR, BİR HƏRF BELƏ SİLİNMƏDİ) ---
words = {
    "tarix": ["Atabəylər", "Şah İsmayıl", "Nadir Şah", "Çaldıran döyüşü", "Tomris", "Babək", "Cavanşir", "M.Ə.Rəsulzadə", "Şah Abbas", "Gülüstan müqaviləsi", "Türkmənçay müqaviləsi", "Səfəvilər", "Hülakülər", "Səlcuqlular", "Osmanlı", "Napoleon", "Hitler", "Atatürk", "Xətai", "Qara Qoyunlu", "Ağ Qoyunlu", "Şirvanşahlar", "Dərbənd", "Xəzər Xaqanlığı", "Atropatena", "Albaniya", "Manna", "Sümerlər", "Misir piramidaları", "Roma İmperiyası", "Yulius Sezar", "Spartak", "Çingiz Xan", "Əmir Teymur", "Sultan Süleyman", "Fatih Sultan Mehmet", "Məlhəmə döyüşü", "İkinci Dünya Müharibəsi", "Qarabağ müharibəsi", "Şuşa bəyannaməsi", "Naxçıvan xanlığı", "Cavad xan", "Pənahəli xan", "Xurşidbanu Natəvan", "Mirzə Fətəli Axundov", "Nizami Gəncəvi", "Füzuli", "Nəsimi", "Dədə Qorqud", "Koroğlu", "Qaçaq Nəbi", "Zəngəzur", "İrəvan xanlığı", "Bakı xanlığı", "Gəncə mühasirəsi", "20 Yanvar", "Xocalı soyqırımı", "ADR", "Vikinqlər", "Raqnar Lodbrok", "Alfred Veliki", "Uhtred", "Ekskalibur", "Qızıl Orda", "Monqollar", "Səlib yürüşləri", "Renessans", "Fransız inqilabı", "Sənaye inqilabı", "Kolumb", "Magellan", "Vasko da Qama", "Da Vinçi", "Eynşteyn", "Nyuton", "Arximed", "Pifaqor", "Sokrat", "Platon", "Aristotel", "Böyük İskəndər", "Dara", "Hannibal", "Alparslan", "Malazgird döyüşü", "Ertuğrul Qazi", "Osman Qazi", "Şah Təhmasib", "Zərdabi", "A.Bakıxanov", "Əhməd Cavad", "Üzeyir Hacıbəyov", "Lütfi Zadə", "Heydər Əliyev", "İlham Əliyev", "Zəfər Günü", "Xudafərin", "Araz", "Kür", "Göyçə", "Borçalı", "Təbriz", "Ərdəbil", "Urmiya", "Zənjan", "Qəzvin", "Həmədan", "Marağa", "Xoy", "Maku", "Quba xanlığı", "Şəki xanlığı", "Hacı Çələbi", "Fətəli xan", "İbrahimxəlil xan", "Vaqif", "Vidadi", "Molla Nəsrəddin", "Sabir", "Cavid", "Müşfiq", "Vurğun", "Şəhriyar", "B.Vahabzadə", "Xəlil Rza", "Məmməd Araz", "İsmayıl Şıxlı", "Anar", "Elçin", "Çingiz Abdullayev", "Mesopotamiya", "Babil", "Hammurapi qanunları", "Assuriya", "Urartu", "Mediya", "Əhəmənilər", "Parfiya", "Bizans", "Frank dövləti", "I Pyotr", "II Yekaterina", "I Dünya Müharibəsi", "Mudros barışığı", "Sevr müqaviləsi", "Lozan müqaviləsi", "Soyuq müharibə", "SSRİ", "NATO", "Varşava müqaviləsi", "BMT", "UNESCO", "İslam Həmrəyliyi"],
    "cografiya": ["Everest", "Amazon", "Xəzər dənizi", "Bakı", "Gəncə", "Sumqayıt", "Naxçıvan", "Lənkəran", "Şəki", "Quba", "Şuşa", "Kəlbəcər", "Ağdam", "Füzuli", "Cəbrayıl", "Zəngilan", "Qubadlı", "Laçın", "Xocalı", "Xocavənd", "Ağdərə", "Xankəndi", "Böyük Qafqaz", "Kiçik Qafqaz", "Murovdağ", "Şahdağ", "Tufandağ", "Bazardüzü", "Kür çayı", "Araz çayı", "Qanıx", "Qabırrı", "Tərtər çayı", "Ağstafa çayı", "Göy Göl", "Maral Göl", "Batabat", "Ceyranbatan", "Mingəçevir", "Abşeron", "Səhra", "Savanna", "Tayqa", "Tundra", "Cəngəllik", "Sakit Okean", "Atlantik Okean", "Hind Okeanı", "Antarktida", "Avstraliya", "Afrika", "Avropa", "Asiya", "Şimali Amerika", "Cənubi Amerika", "Nil çayı", "Missisipi", "Yantszı", "Yenisey", "Volqa", "Dunay", "Alp dağları", "And dağları", "Himalay", "Ural dağları", "Böyük Səhra", "Qobi", "Qaraqum", "Qızılqum", "Atakama", "Viktoriya şəlaləsi", "Niqara", "Anxel", "Baykal gölü", "Egey dənizi", "Aralıq dənizi", "Qara dəniz", "Qırmızı dəniz", "Ölü dəniz", "Cəbəllüttariq", "Süveyş kanalı", "Panama kanalı", "İstanbul boğazı", "Dardanel", "Yaponiya", "Çin", "Hindistan", "Rusiya", "Türkiyə", "İran", "Gürcüstan", "Fransa", "Almaniya", "İtaliya", "İspaniya", "ABŞ", "Kanada", "Braziliya", "Argentina", "Misir", "Pakistan", "İndoneziya", "Meksika", "Qazaxıstan", "Özbəkistan", "Tbilisi", "Ankara", "Moskva", "London", "Paris", "Berlin", "Roma", "Madrid", "Vaşinqton", "Tokio", "Pekin", "Qahirə", "Astana", "Daşkənd", "Ekvator", "Meridian", "Paralel", "Enlik", "Uzunluq", "Xəritə", "Qlobus", "Kompas", "Azimut", "Relyef", "İqlim", "Atmosfer", "Litosfer", "Hidrosfer", "Biosfer", "Maqma", "Vulkan", "Zəlzələ", "Cunami", "Geyser", "Stalaktit", "Stalaqmit", "Arxipelaq", "Ada", "Yarımada", "Körfəz", "Boğaz", "Dərə", "Kanyon", "Plato", "Oazis", "Musson", "Passat", "Siklon", "Antisiklon", "Barometr", "Hiqrometr", "Termometr", "Anemometr", "Seysmoqraf", "Radiasiya", "Ozon qatı", "Urbanizasiya"],
    "insan_adlari": ["Xəyal", "Əli", "Zəhra", "Murad", "Leyla", "Aysu", "Kənan", "Nigar", "Orxan", "Fidan", "Rəşad", "Günay", "Elvin", "Aytən", "Vüsal", "Sevinc", "Tural", "Arzu", "Emin", "Nərmin", "Anar", "Lalə", "Samir", "Aysel", "Rauf", "Gültən", "İlqar", "Pərvin", "Zaur", "Aynur", "Eldar", "Ülviyyə", "Nicat", "Səbinə", "Fuad", "Elnarə", "Rövşən", "Türkan", "Namiq", "Könül", "İlkin", "Səidə", "Ayxan", "Nisə", "Tofiq", "Bəsti", "Ramil", "Dilarə", "Seymur", "Elmira", "Pəviz", "Jasmin", "Aqil", "Nəzrin", "Şahin", "Fatimə", "Cavid", "Xədicə", "Taleh", "Mədinə", "Mənsur", "Rəna", "Üzeyir", "Sona", "Babək", "Banu", "İbrahim", "Zeynəb", "Hüseyn", "Gülnar", "Həsən", "Nailə", "Kamran", "Esmira", "Fariz", "Məryəm", "Azər", "Şəbnəm", "Nurlan", "Gülər", "Pənah", "Afaq", "Teymur", "Səid", "Yusif", "Sara", "Adil", "Fəridə", "Asif", "Ləman", "Vasif", "Nərgiz", "Hikmət", "Səmayə", "Musa", "Həvva", "İsa", "Məsumə", "Yəhya", "Asya", "İsmayıl", "Gülşən", "Osman", "Fərhad", "Şirin", "Məcnun", "Leyli", "Kərəm", "Əsli", "Səməd", "Vurğun", "Mikayıl", "Müşfiq", "Hüseyn Javid", "Nəbi", "Xəzər", "Araz", "Göyçə", "Zəngəzur", "Təbriz", "Bakı", "Polad", "Mübariz", "İlqar", "Şükür", "Xudayar", "Cəbrayıl", "Yalçın", "Elşən", "Afət", "Nadir", "Sultan", "Məhəmməd", "Ömər", "Osman", "Abbas", "Cəfər", "Kazım", "Rza", "Taqi", "Naqi", "Mehdi", "Zəki", "Bəxtiyar", "Vidadi", "Vaqif", "Zakir", "Hadi", "Səhənd", "Səməndər", "Tərlan", "Şahin", "Laçın", "Toğrul", "Çingiz", "Elman", "Rüstəm", "Zöhrab", "Siyavuş", "Esmira", "Solmaz"],
    "qarisig": ["Telefon", "Kitab", "Təyyarə", "Futbol", "Musiqi", "Televizor", "Kompüter", "Soyuducu", "Maşın", "Velosiped", "Saat", "Eynək", "Qələm", "Dəftər", "Çanta", "Ayaqqabı", "Paltar", "Yataq", "Masa", "Kürsü", "Pəncərə", "Qapı", "Divar", "Həyət", "Bağça", "Gül", "Ağaç", "Günəş", "Ay", "Ulduz", "Bulud", "Yağış", "Qar", "Külək", "Şimşək", "Dəniz", "Çay", "Dağ", "Meşə", "Yol", "Körpü", "Bina", "Məktəb", "Xəstəxana", "Aptek", "Market", "Restoran", "Kino", "Teatr", "Muzey", "Park", "Heyvanxana", "Pişik", "İt", "At", "İnək", "Qoyun", "Toyuq", "Quş", "Balıq", "Arı", "Kəpənək", "Alma", "Armud", "Nar", "Üzüm", "Banan", "Limon", "Kartof", "Soğan", "Pomidor", "Xiyar", "Çörək", "Su", "Çay", "Qəhvə", "Süd", "Şirə", "Dondurma", "Şokolad", "Konfet", "Tort", "Pizza", "Burger", "Kabab", "Plov", "Dovğa", "Həkim", "Müəllim", "Mühəndis", "Polis", "Əsgər", "Sürücü", "Aşpaz", "Rəssam", "Müğənni", "Aktyor", "Futbolçu", "Şahmat", "Tennis", "Voleybol", "Basketbol", "Üzgüçülük", "Boks", "Güləş", "Karate", "Gitara", "Pianino", "Tar", "Kamança", "Saz", "Radio", "Kamera", "Batareya", "Lampa", "Ütü", "Tozsoran", "Fen", "Tərəzi", "Mikroskop", "Teleskop", "Reket", "Peyk", "Raket", "Kosmos", "Planet", "Mars", "Yupiter", "Qara dəlik", "Qalaktika", "Uçan boşqab"]
}

# --- FUNKSİYALAR (TOXUNULMADI) ---
async def add_point(user, chat_id=None):
    await users_col.update_one({"user_id": user.id}, {"$inc": {"points": 5}, "$set": {"name": user.first_name}}, upsert=True)
    if chat_id:
        await groups_col.update_one({"group_id": chat_id, "user_id": user.id}, {"$inc": {"points": 5}, "$set": {"name": user.first_name}}, upsert=True)

# --- MESAJ YOXLIYAN (SÖZÜ TAPAN) ---
@app.on_message(filters.text & filters.group, group=1)
async def check_word(client, message):
    chat_id = message.chat.id
    if chat_id in active_games:
        game_data = active_games[chat_id]
        correct_word = game_data['word'].lower()
        if message.text.lower() == correct_word:
            user = message.from_user
            await add_point(user, chat_id)
            
            mode = game_data.get('mode', 'chat')
            cat = game_data.get('cat', 'qarisig')
            new_word = random.choice(words[cat])
            
            if mode == "chat":
                # Chatda Cro: Tapan yeni aparıcı olur
                active_games[chat_id] = {"word": new_word, "apariçi": user.id, "mode": "chat", "cat": cat}
                text = f"{user.mention} - sözü tapdı **{correct_word.capitalize()}** və yeni sözü izah edir"
                apariçi_id = user.id
            else:
                # Səslidə Cro: Aparıcı sabit qalır
                active_games[chat_id]['word'] = new_word
                apariçi_id = game_data['apariçi']
                try:
                    old_apariçi = await client.get_users(apariçi_id)
                    ap_mention = old_apariçi.mention
                except:
                    ap_mention = "Aparıcı"
                text = f"{user.mention} - sözü tapdı **{correct_word.capitalize()}**.\n\n{ap_mention} yeni sözü izah edir"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Sözə Baxmaq 🔍", callback_data=f"look_{new_word}")],
                [InlineKeyboardButton("Fikrimi Dəyişdim ❌", callback_data="imtina")],
                [InlineKeyboardButton("Növbeti Söz ♻️", callback_data=f"next_{cat}_{mode}")]
            ])
            await message.reply(text, reply_markup=keyboard)

# --- START MESAJI ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    bot = await client.get_me()
    text = f"👋 **Salam! Mən {bot.first_name} botuyam.**\n\n🎬 Qruplarda Səssiz Sinema (Cro) oynamaq üçün məni qrupa əlavə edin!"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")],
        [InlineKeyboardButton("🏆 Global Reytinq", callback_data="global_rank")],
        [InlineKeyboardButton("📢 Kanal", url=BOT_CHANNEL), InlineKeyboardButton("👤 Sahib", url=OWNER_LINK)]
    ])
    await message.reply_photo(photo=START_IMG, caption=text, reply_markup=keyboard)

# --- REYTİNQ KOMANDALARI (TOXUNULMADI) ---
@app.on_message(filters.command("croreyting"))
async def g_rank(client, message):
    top = await users_col.find().sort("points", -1).limit(10).to_list(10)
    text = "🌍 **Global Reytinq (Top 10):**\n\n"
    for i, u in enumerate(top, 1): text += f"{i}. {u['name']} — {u['points']} xal\n"
    await message.reply(text)

@app.on_message(filters.command("qrupreyting") & filters.group)
async def q_rank(client, message):
    top = await groups_col.find({"group_id": message.chat.id}).sort("points", -1).limit(10).to_list(10)
    text = f"🏠 **Qrup Reytinqi:**\n\n"
    for i, u in enumerate(top, 1): text += f"{i}. {u['name']} — {u['points']} xal\n"
    await message.reply(text if top else "Hələ xal yoxdur.")

# --- OYUN MENYUSU ---
@app.on_message(filters.command(["game", "menu", "crostart"]) & filters.group)
async def menu_cmd(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Chatda Cro", callback_data="sel_chat"),
         InlineKeyboardButton("🎤 Səslidə Cro", callback_data="sel_voice")]
    ])
    await message.reply("Hansı Modda oyunu başlatmaq istəyirsiniz ?", reply_markup=keyboard)

# --- CALLBACKS (TAM GENİŞ HALDA) ---
@app.on_callback_query()
async def queries(client, callback_query: CallbackQuery):
    data = callback_query.data
    user = callback_query.from_user
    cid = callback_query.message.chat.id

    if data == "global_rank":
        top = await users_col.find().sort("points", -1).limit(10).to_list(10)
        text = "🌍 **Global Reytinq:**\n\n"
        for i, u in enumerate(top, 1): text += f"{i}. {u['name']} — {u['points']} xal\n"
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_start")]]))

    elif data == "back_start":
        bot = await client.get_me()
        text = f"👋 **Salam! Mən {bot.first_name} botuyam.**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")],
            [InlineKeyboardButton("🏆 Global Reytinq", callback_data="global_rank")],
            [InlineKeyboardButton("📢 Kanal", url=BOT_CHANNEL), InlineKeyboardButton("👤 Sahib", url=OWNER_LINK)]
        ])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    elif data.startswith("sel_"):
        mode = data.replace("sel_", "")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data=f"set_{mode}_qarisig")],
            [InlineKeyboardButton("📜 Tarix", callback_data=f"set_{mode}_tarix"), 
             InlineKeyboardButton("🌍 Coğrafiya", callback_data=f"set_{mode}_cografiya")],
            [InlineKeyboardButton("👥 İnsan Adları", callback_data=f"set_{mode}_insan_adlari")]
        ])
        await callback_query.edit_message_text(f"📂 Mod: **{mode.capitalize()}** seçildi. Kateqoriya seçin:", reply_markup=keyboard)

    elif data.startswith("set_"):
        parts = data.split("_")
        mode = parts[1]
        cat = "_".join(parts[2:])
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📝 Sözü İzah Et", callback_data=f"run_{mode}_{cat}")]])
        await callback_query.edit_message_text(f"✅ Kateqoriya: {cat}\nKim aparıcı olacaq?", reply_markup=keyboard)

    elif data.startswith("run_"):
        parts = data.split("_")
        mode = parts[1]
        cat = "_".join(parts[2:])
        word = random.choice(words[cat])
        active_games[cid] = {"word": word, "apariçi": user.id, "mode": mode, "cat": cat}
        await client.answer_callback_query(callback_query.id, text=f"Söz: {word}", show_alert=True)
        
        text = f"{user.mention} - sözü izah edir"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Sözə Baxmaq 🔍", callback_data=f"look_{word}")],
            [InlineKeyboardButton("Fikrimi Dəyişdim ❌", callback_data="imtina")],
            [InlineKeyboardButton("Növbeti Söz ♻️", callback_data=f"next_{cat}_{mode}")]
        ])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    elif data.startswith("next_"):
        parts = data.split("_")
        mode = parts[-1]
        cat = "_".join(parts[1:-1])
        if cid in active_games and user.id != active_games[cid]['apariçi']:
            return await callback_query.answer("Yalnız aparıcı növbəti sözü keçə bilər!", show_alert=True)
        
        word = random.choice(words[cat])
        active_games[cid]['word'] = word
        await callback_query.answer(f"Yeni Söz: {word}", show_alert=True)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Sözə Baxmaq 🔍", callback_data=f"look_{word}")],
            [InlineKeyboardButton("Fikrimi Dəyişdim ❌", callback_data="imtina")],
            [InlineKeyboardButton("Növbeti Söz ♻️", callback_data=f"next_{cat}_{mode}")]
        ])
        await callback_query.edit_message_text(f"{user.mention} - yeni sözü izah edir", reply_markup=keyboard)

    elif data.startswith("look_"):
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            await callback_query.answer(f"Söz: {active_games[cid]['word']}", show_alert=True)
        else:
            await callback_query.answer("Sözə yalnız aparıcı baxa bilər!", show_alert=True)

    elif data == "imtina":
        if cid in active_games and user.id == active_games[cid]['apariçi']:
            del active_games[cid]
            await callback_query.edit_message_text(f"❌ {user.mention} imtina etdi. Oyun dayandırıldı.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Yeni Oyun 🎮", callback_data="back_menu")]]))
        else:
            await callback_query.answer("Yalnız aparıcı imtina edə bilər!", show_alert=True)

    elif data == "back_menu":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Chatda Cro", callback_data="sel_chat"),
             InlineKeyboardButton("🎤 Səslidə Cro", callback_data="sel_voice")]
        ])
        await callback_query.edit_message_text("Hansı Modda oyunu başlatmaq istəyirsiniz ?", reply_markup=keyboard)

# --- İŞƏ SALMA ---
async def main():
    await app.start()
    await app.set_bot_commands([
        BotCommand("start", "Botu başladar"),
        BotCommand("game", "Oyunu başladar"),
        BotCommand("croreyting", "Global reytinq"),
        BotCommand("qrupreyting", "Qrup reytinqi")
    ])
    print("HT-Cro Bot İşləyir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
