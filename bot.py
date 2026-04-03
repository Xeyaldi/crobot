import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIG VARS (Heroku-dan oxunur) ---
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

# --- MONGODB BAĞLANTISI ---
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["cro_bot_db"]
users_col = db["users"]
groups_col = db["groups"]

app = Client("izah_et_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- 150+ SÖZLÜK BAZA (TAM SİYAHI - HİÇ NƏ SİLİNMƏDİ) ---
words = {
    "tarix": [
        "Atabəylər", "Şah İsmayıl", "Nadir Şah", "Çaldıran döyüşü", "Tomris", "Babək", "Cavanşir", "M.Ə.Rəsulzadə", 
        "Şah Abbas", "Gülüstan müqaviləsi", "Türkmənçay müqaviləsi", "Səfəvilər", "Hülakülər", "Səlcuqlular", "Osmanlı", 
        "Napoleon", "Hitler", "Atatürk", "Xətai", "Qara Qoyunlu", "Ağ Qoyunlu", "Şirvanşahlar", "Dərbənd", "Xəzər Xaqanlığı",
        "Atropatena", "Albaniya", "Manna", "Sümerlər", "Misir piramidaları", "Roma İmperiyası", "Yulius Sezar", "Spartak", 
        "Çingiz Xan", "Əmir Teymur", "Sultan Süleyman", "Fatih Sultan Mehmet", "Məlhəmə döyüşü", "İkinci Dünya Müharibəsi",
        "Qarabağ müharibəsi", "Şuşa bəyannaməsi", "Naxçıvan xanlığı", "Cavad xan", "Pənahəli xan", "Xurşidbanu Natəvan",
        "Mirzə Fətəli Axundov", "Nizami Gəncəvi", "Füzuli", "Nəsimi", "Dədə Qorqud", "Koroğlu", "Qaçaq Nəbi", "Zəngəzur",
        "İrəvan xanlığı", "Bakı xanlığı", "Gəncə mühasirəsi", "20 Yanvar", "Xocalı soyqırımı", "ADR", "Vikinqlər", 
        "Raqnar Lodbrok", "Alfred Veliki", "Uhtred", "Ekskalibur", "Qızıl Orda", "Monqollar", "Səlib yürüşləri", 
        "Renessans", "Fransız inqilabı", "Sənaye inqilabı", "Kolumb", "Magellan", "Vasko da Qama", "Da Vinçi", 
        "Eynşteyn", "Nyuton", "Arximed", "Pifaqor", "Sokrat", "Platon", "Aristotel", "Böyük İskəndər", "Dara", 
        "Hannibal", "Alparslan", "Malazgird döyüşü", "Ertuğrul Qazi", "Osman Qazi", "Şah Təhmasib", "Zərdabi", 
        "A.Bakıxanov", "Əhməd Cavad", "Üzeyir Hacıbəyov", "Lütfi Zadə", "Heydər Əliyev", "İlham Əliyev", "Zəfər Günü", 
        "Xudafərin", "Araz", "Kür", "Göyçə", "Borçalı", "Təbriz", "Ərdəbil", "Urmiya", "Zənjan", "Qəzvin", "Həmədan", 
        "Marağa", "Xoy", "Maku", "Quba xanlığı", "Şəki xanlığı", "Hacı Çələbi", "Fətəli xan", "İbrahimxəlil xan", 
        "Vaqif", "Vidadi", "Molla Nəsrəddin", "Sabir", "Cavid", "Müşfiq", "Vurğun", "Şəhriyar", "B.Vahabzadə", 
        "Xəlil Rza", "Məmməd Araz", "İsmayıl Şıxlı", "Anar", "Elçin", "Çingiz Abdullayev", "Mesopotamiya", "Babil", 
        "Hammurapi qanunları", "Assuriya", "Urartu", "Mediya", "Əhəmənilər", "Parfiya", "Bizans", "Frank dövləti", 
        "I Pyotr", "II Yekaterina", "I Dünya Müharibəsi", "Mudros barışığı", "Sevr müqaviləsi", "Lozan müqaviləsi", 
        "Soyuq müharibə", "SSRİ", "NATO", "Varşava müqaviləsi", "BMT", "UNESCO", "İslam Həmrəyliyi"
    ],
    "cografiya": [
        "Everest", "Amazon", "Xəzər dənizi", "Bakı", "Gəncə", "Sumqayıt", "Naxçıvan", "Lənkəran", "Şəki", "Quba", "Şuşa",
        "Kəlbəcər", "Ağdam", "Füzuli", "Cəbrayıl", "Zəngilan", "Qubadlı", "Laçın", "Xocalı", "Xocavənd", "Ağdərə", "Xankəndi",
        "Böyük Qafqaz", "Kiçik Qafqaz", "Murovdağ", "Şahdağ", "Tufandağ", "Bazardüzü", "Kür çayı", "Araz çayı", "Qanıx", 
        "Qabırrı", "Tərtər çayı", "Ağstafa çayı", "Göy Göl", "Maral Göl", "Batabat", "Ceyranbatan", "Mingəçevir", 
        "Abşeron", "Səhra", "Savanna", "Tayqa", "Tundra", "Cəngəllik", "Sakit Okean", "Atlantik Okean", "Hind Okeanı",
        "Antarktida", "Avstraliya", "Afrika", "Avropa", "Asiya", "Şimali Amerika", "Cənubi Amerika", "Nil çayı", 
        "Missisipi", "Yantszı", "Yenisey", "Volqa", "Dunay", "Alp dağları", "And dağları", "Himalay", "Ural dağları", 
        "Böyük Səhra", "Qobi", "Qaraqum", "Qızılqum", "Atakama", "Viktoriya şəlaləsi", "Niqara", "Anxel", "Baykal gölü", 
        "Egey dənizi", "Aralıq dənizi", "Qara dəniz", "Qırmızı dəniz", "Ölü dəniz", "Cəbəllüttariq", "Süveyş kanalı", 
        "Panama kanalı", "İstanbul boğazı", "Dardanel", "Yaponiya", "Çin", "Hindistan", "Rusiya", "Türkiyə", "İran", 
        "Gürcüstan", "Fransa", "Almaniya", "İtaliya", "İspaniya", "ABŞ", "Kanada", "Braziliya", "Argentina", "Misir", 
        "Pakistan", "İndoneziya", "Meksika", "Qazaxıstan", "Özbəkistan", "Tbilisi", "Ankara", "Moskva", "London", "Paris", 
        "Berlin", "Roma", "Madrid", "Vaşinqton", "Tokio", "Pekin", "Qahirə", "Astana", "Daşkənd", "Ekvator", "Meridian", 
        "Paralel", "Enlik", "Uzunluq", "Xəritə", "Qlobus", "Kompas", "Azimut", "Relyef", "İqlim", "Atmosfer", "Litosfer", 
        "Hidrosfer", "Biosfer", "Maqma", "Vulkan", "Zəlzələ", "Cunami", "Geyser", "Stalaktit", "Stalaqmit", "Arxipelaq", 
        "Ada", "Yarımada", "Körfəz", "Boğaz", "Dərə", "Kanyon", "Plato", "Oazis", "Musson", "Passat", "Siklon", "Antisiklon",
        "Barometr", "Hiqrometr", "Termometr", "Anemometr", "Seysmoqraf", "Radiasiya", "Ozon qatı", "Urbanizasiya"
    ],
    "insan_adlari": [
        "Xəyal", "Əli", "Zəhra", "Murad", "Leyla", "Aysu", "Kənan", "Nigar", "Orxan", "Fidan", "Rəşad", "Günay", "Elvin", 
        "Aytən", "Vüsal", "Sevinc", "Tural", "Arzu", "Emin", "Nərmin", "Anar", "Lalə", "Samir", "Aysel", "Rauf", "Gültən",
        "İlqar", "Pərvin", "Zaur", "Aynur", "Eldar", "Ülviyyə", "Nicat", "Səbinə", "Fuad", "Elnarə", "Rövşən", "Türkan",
        "Namiq", "Könül", "İlkin", "Səidə", "Ayxan", "Nisə", "Tofiq", "Bəsti", "Ramil", "Dilarə", "Seymur", "Elmira",
        "Pəviz", "Jasmin", "Aqil", "Nəzrin", "Şahin", "Fatimə", "Cavid", "Xədicə", "Taleh", "Mədinə", "Mənsur", "Rəna",
        "Üzeyir", "Sona", "Babək", "Banu", "İbrahim", "Zeynəb", "Hüseyn", "Gülnar", "Həsən", "Nailə", "Kamran", "Esmira",
        "Fariz", "Məryəm", "Azər", "Şəbnəm", "Nurlan", "Gülər", "Pənah", "Afaq", "Teymur", "Səid", "Yusif", "Sara", "Adil",
        "Fəridə", "Asif", "Ləman", "Vasif", "Nərgiz", "Hikmət", "Səmayə", "Musa", "Həvva", "İsa", "Məsumə", "Yəhya", "Asya",
        "İsmayıl", "Gülşən", "Osman", "Fərhad", "Şirin", "Məcnun", "Leyli", "Kərəm", "Əsli", "Səməd", "Vurğun", "Mikayıl",
        "Müşfiq", "Hüseyn Javid", "Nəbi", "Xəzər", "Araz", "Göyçə", "Zəngəzur", "Təbriz", "Bakı", "Polad", "Mübariz", "İlqar",
        "Şükür", "Xudayar", "Cəbrayıl", "Yalçın", "Elşən", "Afət", "Nadir", "Sultan", "Məhəmməd", "Ömər", "Osman", "Abbas",
        "Cəfər", "Kazım", "Rza", "Taqi", "Naqi", "Mehdi", "Zəki", "Bəxtiyar", "Vidadi", "Vaqif", "Zakir", "Hadi", "Səhənd",
        "Səməndər", "Tərlan", "Şahin", "Laçın", "Toğrul", "Çingiz", "Elman", "Rüstəm", "Zöhrab", "Siyavuş", "Esmira", "Solmaz"
    ],
    "qarisig": [
        "Telefon", "Kitab", "Təyyarə", "Futbol", "Musiqi", "Televizor", "Kompüter", "Soyuducu", "Maşın", "Velosiped", "Saat",
        "Eynək", "Qələm", "Dəftər", "Çanta", "Ayaqqabı", "Paltar", "Yataq", "Masa", "Kürsü", "Pəncərə", "Qapı", "Divar",
        "Həyət", "Bağça", "Gül", "Ağaç", "Günəş", "Ay", "Ulduz", "Bulud", "Yağış", "Qar", "Külək", "Şimşək", "Dəniz", 
        "Çay", "Dağ", "Meşə", "Yol", "Körpü", "Bina", "Məktəb", "Xəstəxana", "Aptek", "Market", "Restoran", "Kino", "Teatr", 
        "Muzey", "Park", "Heyvanxana", "Pişik", "İt", "At", "İnək", "Qoyun", "Toyuq", "Quş", "Balıq", "Arı", "Kəpənək", 
        "Alma", "Armud", "Nar", "Üzüm", "Banan", "Limon", "Kartof", "Soğan", "Pomidor", "Xiyar", "Çörək", "Su", "Çay", 
        "Qəhvə", "Süd", "Şirə", "Dondurma", "Şokolad", "Konfet", "Tort", "Pizza", "Burger", "Kabab", "Plov", "Dovğa", 
        "Həkim", "Müəllim", "Mühəndis", "Polis", "Əsgər", "Sürücü", "Aşpaz", "Rəssam", "Müğənni", "Aktyor", "Futbolçu", 
        "Şahmat", "Tennis", "Voleybol", "Basketbol", "Üzgüçülük", "Boks", "Güləş", "Karate", "Gitara", "Pianino", "Tar", 
        "Kamança", "Saz", "Radio", "Kamera", "Batareya", "Lampa", "Ütü", "Tozsoran", "Fen", "Tərəzi", "Mikroskop", 
        "Teleskop", "Reket", "Peyk", "Raket", "Kosmos", "Planet", "Mars", "Yupiter", "Qara dəlik", "Qalaktika", "Uçan boşqab"
    ]
}

# --- XAL VƏ LOG FUNKSİYALARI ---
async def add_point(user, chat_id=None):
    await users_col.update_one({"user_id": user.id}, {"$inc": {"points": 5}, "$set": {"name": user.first_name}}, upsert=True)
    if chat_id:
        await groups_col.update_one({"group_id": chat_id, "user_id": user.id}, {"$inc": {"points": 5}, "$set": {"name": user.first_name}}, upsert=True)

# --- BOTUN MESAJ İZLƏMƏSİ (LOG QRUPU) ---
@app.on_message(filters.all & ~filters.service, group=-1)
async def logger_func(client, message):
    if LOG_GROUP and message.chat.id != LOG_GROUP:
        u_name = message.from_user.first_name if message.from_user else "Bilinmir"
        u_id = message.from_user.id if message.from_user else "N/A"
        chat_title = message.chat.title or "Şəxsi"
        log_text = f"👤 **İstifadəçi:** {u_name} (ID: {u_id})\n📍 **Yer:** {chat_title}\n💬 **Mesaj:** {message.text or 'Media'}"
        
        keyboard = None
        if message.from_user and message.from_user.id == OWNER_ID:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📊 Aktivliyi Gör", callback_data="stats")]])
        
        await client.send_message(LOG_GROUP, log_text, reply_markup=keyboard)

# --- START, KOMEKCRO, STOP ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = f"👋 **Salam! Mən HT-Cro botuyam.**\n\n🎬 Qruplarda Səssiz Sinema oynamaq üçün məni qrupa əlavə edin!\n\n📖 Kömək: /komekcro"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Qrupa Əlavə Et", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("🏆 Global Reytinq", callback_data="global_rank")],
        [InlineKeyboardButton("📢 Kanal", url=BOT_CHANNEL), InlineKeyboardButton("👤 Sahib", url=OWNER_LINK)],
        [InlineKeyboardButton("🛠 Kömək", url=SUPPORT_GRP)]
    ])
    await message.reply_photo(photo=START_IMG, caption=text, reply_markup=keyboard)

@app.on_message(filters.command("komekcro"))
async def help_cmd(client, message):
    await message.reply("📖 **Komandalar:**\n/crostart - Oyunu başladar\n/stop - Oyunu dayandırar\n/croreyting - Global liderlər\n/qrupreyting - Qrup daxili liderlər")

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(client, message):
    await message.reply("🛑 Oyun dayandırıldı.")

# --- OYUN MENYUSU ---
@app.on_message(filters.command(["game", "menu", "crostart"]) & filters.group)
async def menu_cmd(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data="select_qarisig")],
        [InlineKeyboardButton("📜 Tarix", callback_data="select_tarix"), 
         InlineKeyboardButton("🌍 Coğrafiya", callback_data="select_cografiya")],
        [InlineKeyboardButton("👥 İnsan Adları", callback_data="select_insan_adlari")],
        [InlineKeyboardButton("🛑 Oyunu Bitir", callback_data="end_game")]
    ])
    await message.reply("🎮 **HT-Cro modunu seçin:**", reply_markup=keyboard)

# --- REYTİNQ KOMANDALARI ---
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

# --- CALLBACK İŞLƏMƏLƏRİ ---
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
        await callback_query.edit_message_text("👋 **Salam! Mən HT-Cro botuyam.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏆 Global Reytinq", callback_data="global_rank")]]))

    elif data == "stats" and user.id == OWNER_ID:
        u_c = await users_col.count_documents({})
        g_c = len(await groups_col.distinct("group_id"))
        await callback_query.answer(f"📊 Aktivlik:\nİstifadəçi: {u_c}\nQrup: {g_c}", show_alert=True)

    elif data.startswith("select_"):
        mod = data.replace("select_", "")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎤 Sözü İzah Et (+5 Xal)", callback_data=f"start_{mod}")],
            [InlineKeyboardButton("⬅️ Geri", callback_data="back_menu")]
        ])
        await callback_query.edit_message_text(f"✅ **{mod.capitalize()}** seçildi. Kim izah edir?", reply_markup=keyboard)

    elif data.startswith("start_"):
        cat = data.replace("start_", "")
        word = random.choice(words[cat])
        await client.answer_callback_query(callback_query.id, text=f"Söz: {word}", show_alert=True)
        await add_point(user, cid)
        text = f"👤 **Aparıcı:** {user.mention} (+5 Xal)\n📁 **Mod:** {cat.capitalize()}\n📢 İzah edir..."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Sözə Bax", callback_data=f"look_{word}")],
            [InlineKeyboardButton("❌ İmtina", callback_data="imtina")],
            [InlineKeyboardButton("♻️ Növbəti", callback_data=f"start_{cat}")]
        ])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    elif data.startswith("look_"):
        await client.answer_callback_query(callback_query.id, text=f"Söz: {data.split('_')[1]}", show_alert=True)

    elif data == "imtina":
        await callback_query.edit_message_text(f"❌ {user.mention} imtina etdi. Kim aparıcı olmaq istəyir?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Mən olacam ✅", callback_data="back_menu")]]))

    elif data == "back_menu":
        # Menyunu yenidən göstər
        await callback_query.edit_message_text("🎮 **Mod seçin:**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌀 Qarışıq", callback_data="select_qarisig")]]))

    elif data == "end_game":
        await callback_query.edit_message_text("🛑 Oyun bitdi.")

# --- İŞƏ SALMA ---
async def main():
    await app.start()
    print("HT-Cro Bot İşləyir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
