import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Config Vars (Heroku Settings-dən daxil edəcəksən)
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Yeni Linklər (Heroku-da bunları KEY olaraq əlavə et)
START_IMG = os.environ.get("START_IMG", "https://telegra.ph/file/default.jpg") # Şəkil linki
SUPPORT_GRP = os.environ.get("SUPPORT_GRP", "https://t.me/your_group") # Kömək qrupu
BOT_CHANNEL = os.environ.get("BOT_CHANNEL", "https://t.me/your_channel") # Bot kanalı
OWNER_LINK = os.environ.get("OWNER_LINK", "https://t.me/your_username") # Sahib linki

app = Client("izah_et_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# SƏNİN 600+ SÖZLÜK BAZAN (Toxunulmadı)
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

# Start Mesajı və Effekti
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    bot = await client.get_me()
    text = (
        f"👋 **Salam! Mən {bot.first_name} botuyam.**\n\n"
        "🎬 Mən qruplarda Səssiz Sinema (Cro) oynamaq üçün yaradılmışam.\n"
        "📜 Tarix, Coğrafiya və digər modlarda sözləri izah edərək əylənə bilərsiniz.\n\n"
        "🎮 Oyunu başlatmaq üçün məni qrupa əlavə edin!"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Məni Qrupa Əlavə Et", url=f"https://t.me/{bot.username}?startgroup=true")],
        [InlineKeyboardButton("📢 Bot Kanalı", url=BOT_CHANNEL), InlineKeyboardButton("👤 Sahib", url=OWNER_LINK)],
        [InlineKeyboardButton("🛠 Kömək Qrupu", url=SUPPORT_GRP)]
    ])
    
    # Şəkil ilə göndərmə
    await message.reply_photo(photo=START_IMG, caption=text, reply_markup=keyboard)

# Oyun Menyusu (HT-Cro dizaynı)
@app.on_message(filters.command(["game", "menu"]))
async def game_menu(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data="select_qarisig")],
        [InlineKeyboardButton("📜 Tarix", callback_data="select_tarix"), 
         InlineKeyboardButton("🌍 Coğrafiya", callback_data="select_cografiya")],
        [InlineKeyboardButton("👥 İnsan Adları", callback_data="select_insan_adlari")],
        [InlineKeyboardButton("🛑 Oyunu Bitir", callback_data="end_game")]
    ])
    await message.reply(f"🎮 **HT-Cro modunu seçin:**", reply_markup=keyboard)

# Callback İşləmələri
@app.on_callback_query()
async def handle_query(client, callback_query: CallbackQuery):
    data = callback_query.data
    user = callback_query.from_user

    # Mod seçildi (HT-Cro şəkli 2-dəki kimi)
    if data.startswith("select_"):
        mod = data.replace("select_", "")
        mod_name = mod.replace("_", " ").capitalize()
        text = f"✅ **{mod_name}** modu seçildi!\n\n👇 Kim izah etmək istəyir? Butona basın."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎤 Sözü İzah Et", callback_data=f"start_{mod}")],
            [InlineKeyboardButton("⬅️ Modu Dəyiş", callback_data="back_to_menu")],
            [InlineKeyboardButton("🛑 Oyunu Bitir", callback_data="end_game")]
        ])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    # Oyuna Başla (Aparıcı təyin olundu)
    elif data.startswith("start_"):
        category = data.replace("start_", "")
        word = random.choice(words[category])
        await client.answer_callback_query(callback_query.id, text=f"Sözünüz: {word}", show_alert=True)
        
        cat_names = {"tarix": "Tarix", "cografiya": "Coğrafiya", "insan_adlari": "İnsan Adları", "qarisig": "Qarışıq"}
        
        text = (
            f"👤 **Aparıcı:** {user.mention}\n"
            f"📁 **Mod:** {cat_names[category]}\n"
            f"📢 Sözü izah edir... Tapın görək!"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Sözə Baxmaq", callback_data=f"look_{word}")],
            [InlineKeyboardButton("❌ Fikrimi Dəyişdim", callback_data="imtina")],
            [InlineKeyboardButton("♻️ Növbəti Söz", callback_data=f"start_{category}")]
        ])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    elif data.startswith("look_"):
        word = data.replace("look_", "")
        await client.answer_callback_query(callback_query.id, text=f"Söz: {word}", show_alert=True)

    elif data == "imtina":
        text = f"❌ {user.mention} aparıcılıqdan imtina etdi!\n\nKim aparıcı olmaq istəyir? ✅"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Aparıcı olmaq istəyirəm ✅", callback_data="back_to_menu")]])
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    elif data == "back_to_menu":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data="select_qarisig")],
            [InlineKeyboardButton("📜 Tarix", callback_data="select_tarix"), 
             InlineKeyboardButton("🌍 Coğrafiya", callback_data="select_cografiya")],
            [InlineKeyboardButton("👥 İnsan Adları", callback_data="select_insan_adlari")],
            [InlineKeyboardButton("🛑 Oyunu Bitir", callback_data="end_game")]
        ])
        await callback_query.edit_message_text("🎮 **HT-Cro modunu seçin:**", reply_markup=keyboard)

    elif data == "end_game":
        await callback_query.edit_message_text("🛑 Oyun bitirildi. Yeni oyun üçün /game yazın.")

# Asyncio Başlatma
async def main():
    await app.start()
    print("Bot HT-Cro dizaynı ilə aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
