# from __future__ import annotations
# 
# теж тестовий режим лише з бібліотекою ключових категорій, підкатегорій та просто слів по яким вони обираються для режиму basic_categorizer.py
# 
# CATEGORY_KEYWORDS: dict[str, dict[str, list[str]]] = {
#     "Study":
#         { "Labs":
#               [ "лабораторна", "лабораторна робота", "практична робота", "практичне завдання", "дослід", "дослідження", "експеримент", "експериментальні дані", "вимірювання", "обчислення", "розрахунок", "методика виконання", "хід роботи", "лабораторне обладнання", "результати експерименту", "аналіз результатів", "тестування", "моделювання", "simulation", "laboratory", "laboratory work", "lab", "practical work", "practical task", "experiment", "experimental data", "measurement", "calculation", "procedure", "protocol", "analysis results", "lab equipment", "testing", ],
#           "Reports":
#               [ "звіт", "звіт з практики", "підсумковий звіт", "пояснювальна записка", "результати роботи", "висновки", "аналіз", "опис виконання", "оформлення звіту", "дослідницький звіт", "підсумок", "report", "final report", "summary", "reporting", "results", "conclusions", "findings", "analysis", "analytical report", "research report", "explanatory note", ],
#           "Lectures":
#               [ "лекція", "лекції", "конспект лекції", "матеріал лекції", "тема лекції", "курс лекцій", "теоретичний матеріал", "теорія", "вступ", "основи", "навчальний матеріал", "навчальна презентація", "презентація", "lecture", "lectures", "lecture notes", "study material", "theory", "theoretical material", "introduction", "basics", "presentation", "slides", ],
#           "Coursework":
#               [ "курсова", "курсова робота", "курсовий проєкт", "проєкт", "студентський проєкт", "дипломна робота", "бакалаврська робота", "магістерська робота", "кваліфікаційна робота", "захист проєкту", "розробка", "coursework", "course project", "project work", "student project", "thesis", "bachelor thesis", "master thesis", "graduation work", "qualification work", "project defense", "development project", ],
#           "Notes":
#               [ "нотатки", "записи", "конспект", "чернетка", "чернові записи", "помітки", "коротко", "ідеї", "список тем", "матеріали до теми", "notes", "draft", "drafts", "summary notes", "remarks", "annotations", "ideas", "topic list", "observations", ],
#           "Research":
#               [ "дослідження", "наукове дослідження", "наукова стаття", "стаття", "публікація", "журнал", "методологія", "гіпотеза", "аналіз даних", "огляд літератури", "дисертація", "research", "scientific research", "article", "paper", "publication", "journal", "methodology", "hypothesis", "data analysis", "literature review", "review", "dissertation", ],
#           "Assignments":
#               [ "завдання", "домашнє завдання", "навчальне завдання", "вправа", "задача", "розв'язання", "контрольна робота", "перевірочна робота", "тест", "практичне завдання", "assignment", "homework", "study assignment", "task", "exercise", "solution", "test work", "quiz", "practical task", ]},
#
#     "Documents":
#         { "Contracts":
#               [ "договір", "договори", "угода", "угоди", "контракт", "контракти", "сторони договору", "предмет договору", "умови договору", "термін дії", "відповідальність сторін", "додаткова угода", "орендна угода", "правочин", "legal agreement", "agreement", "contract", "contracts", "terms and conditions", "parties", "subject of agreement", "duration", "liability", "additional agreement", "lease agreement", ],
#           "Certificates":
#               [ "сертифікат", "сертифікати", "свідоцтво", "посвідчення", "довідка", "підтвердження", "атестат", "диплом", "ліцензія", "акредитація", "реєстраційне посвідчення", "certificate", "certificates", "credential", "credentials", "attestation", "license", "licence", "accreditation", "confirmation", "proof of completion", "registration certificate", ],
#           "Applications":
#               [ "заява", "заявка", "звернення", "клопотання", "прохання", "аплікаційна форма", "подання", "реєстраційна заява", "application", "applications", "request", "petition", "submission", "registration application", "application form", "formal request", ],
#           "Manuals":
#               [ "інструкція", "керівництво", "настанова", "посібник", "порядок використання", "порядок дій", "правила користування", "технічний опис", "експлуатація", "manual", "guide", "guidelines", "instruction", "instructions", "user guide", "technical manual", "operation manual", "usage rules", "operating procedure", ],
#           "Forms":
#               [ "форма", "бланк", "шаблон", "анкета", "опитувальник", "реєстраційна форма", "табель", "відомість", "form", "forms", "template", "blank form", "questionnaire", "survey form", "registration form", "statement form", ],
#           "Reports":
#               [ "службова записка", "акт", "звітний документ", "протокол", "відомість", "довідковий документ", "опис результатів", "документ звітності", "report document", "record", "protocol", "statement", "official note", "memorandum", "act", "summary record", "documentation report", ],
#           "Instructions":
#               [ "положення", "регламент", "вказівка", "розпорядження", "наказ", "внутрішня інструкція", "службова інструкція", "процедура", "policy", "regulation", "order", "directive", "instruction", "internal instruction", "service instruction", "procedure", "operational instruction", ]},
#
#     "IT":
#         { "Programming":
#               [ "код", "програма", "програмування", "алгоритм", "функція", "клас", "метод", "змінна", "структура даних", "цикл", "умова", "скрипт", "розробка", "система", "логіка програми", "source code", "code", "programming", "function", "class", "method", "variable", "data structure", "loop", "condition", "script", "development", "application", ],
#           "Databases":
#               [ "база даних", "бд", "запит", "таблиця", "схема", "sql", "запити sql", "з'єднання таблиць", "індекс", "primary key", "foreign key", "database", "databases", "query", "table", "schema", "sql query", "join", "index", "primary key", "foreign key", "database structure", ],
#           "Cybersecurity":
#               [ "безпека", "кібербезпека", "шифрування", "криптографія", "захист", "автентифікація", "авторизація", "уразливість", "атака", "penetration test", "encryption", "decryption", "security", "cybersecurity", "authentication", "authorization", "vulnerability", "exploit", "attack", "hash", ],
#           "Networks":
#               [ "мережа", "мережевий", "tcp", "ip", "http", "ftp", "dns", "сервер", "клієнт", "з'єднання", "протокол", "network", "networking", "tcp", "ip", "http", "ftp", "dns", "server", "client", "connection", "protocol", ],
#           "DevOps":
#               [ "деплой", "розгортання", "контейнер", "docker", "kubernetes", "ci cd", "pipeline", "інфраструктура", "серверна частина", "автоматизація", "deployment", "deploy", "container", "docker", "kubernetes", "ci cd", "pipeline", "infrastructure", "automation", "build", ],
#           "Software":
#               [ "програма", "застосунок", "додаток", "система", "інтерфейс", "користувацький інтерфейс", "ui", "ux", "desktop app", "mobile app", "software", "application", "app", "system", "interface", "user interface", "ui", "ux", "desktop application", "mobile application", ],
#           "Scripts":
#               [ "скрипт", "автоматизація", "команда", "bash", "shell", "powershell", "batch", "automation script", "task automation", "script file", "script", "automation", "command", "bash", "shell", "powershell", "batch", "automation script", "task script", ]},
#
#     "Books":
#         { "Technical":
#               [ "технічна книга", "довідник", "технічний посібник", "інженерний посібник", "керівництво", "технічна документація", "technical book", "technical guide", "manual", "reference book", "engineering book", "technical documentation", "handbook", "reference guide", ],
#           "Fiction":
#               [ "роман", "повість", "оповідання", "художня література", "сюжет", "персонаж", "вигадана історія", "novel", "story", "fiction", "narrative", "characters", "plot", "fantasy", "literature", ],
#           "Education":
#               [ "підручник", "навчальна книга", "посібник", "учбовий матеріал", "теорія", "основи", "курс", "textbook", "educational book", "study book", "learning material", "theory", "basics", "course book", ],
#           "Science":
#               [ "наукова книга", "наукова література", "дослідження", "науковий матеріал", "публікація", "scientific book", "science book", "research", "scientific material", "publication", "science literature", ],
#           "History":
#               [ "історія", "історична книга", "історичні події", "минуле", "хронологія", "історичний опис", "history book", "historical", "historical events", "chronology", "past events", ],
#           "Guides":
#               [ "гайд", "керівництво", "інструкція", "як зробити", "покроково", "посібник", "guide", "how to", "step by step", "instruction", "user guide", "guidebook", ],
#           "SelfDevelopment":
#               [ "саморозвиток", "мотивація", "особистісний розвиток", "звички", "продуктивність", "успіх", "self development", "self improvement", "motivation", "habits", "productivity", "success", "personal growth", ]},
#
#     "Personal":
#         { "CV":
#               [ "резюме", "cv", "curriculum vitae", "портфоліо", "portfolio", "досвід роботи", "work experience", "навички", "skills", "освіта", "education background", "career summary", "job application cv", ],
#           "Notes":
#               [ "особисті нотатки", "мої записи", "особистий запис", "замітки", "нагадування", "список справ", "to do", "todo", "reminder", "notes", "personal notes", "thoughts", "ideas", "daily notes", ],
#           "Diary":
#               [ "щоденник", "особистий щоденник", "запис дня", "події дня", "мої думки", "рефлексія", "diary", "journal", "daily journal", "personal journal", "daily entry", "reflection", ],
#           "Documents":
#               [ "паспорт", "паспортні дані", "ідентифікаційний код", "документи особи", "особистий документ", "скан паспорта", "identity document", "passport", "id card", "personal document", "personal data", "identification", ],
#           "Scans":
#               [ "скан", "скан документу", "відскановано", "сканкопія", "копія документу", "scan", "scanned", "scanned copy", "document scan", "image scan", ],
#           "PrivateFiles":
#               [ "особисте", "приватне", "конфіденційно", "закрито", "не для інших", "private", "confidential", "personal file", "private data", "restricted", ],
#           "Backups":
#              [ "резервна копія", "бекап", "backup", "archive copy", "збереження", "копія даних", "backup file", "data backup", "saved copy", ]},
#
#     "Media":
#         { "Images":
#               [ "зображення", "фото", "картинка", "скріншот", "скрін", "фотографія", "галерея", "image", "photo", "picture", "screenshot", "jpg", "png", "jpeg", "gallery", ],
#           "Videos":
#               [ "відео", "ролик", "запис відео", "кліп", "фільм", "серіал", "movie", "video", "clip", "film", "recording", "mp4", "avi", "mkv", ],
#           "Music":
#               [ "музика", "пісня", "трек", "аудіо", "звук", "альбом", "music", "song", "track", "audio", "mp3", "wav", "flac", ],
#           "Recordings":
#               [ "запис", "запис екрану", "запис голосу", "екран запис", "voice record", "recording", "screen record", "voice note", "audio recording", ],
#           "Design":
#               [ "дизайн", "макет", "інтерфейс", "ui", "ux", "layout", "design", "mockup", "prototype", "figma", "adobe", "photoshop", ],
#           "Animations":
#               [ "анімація", "анімаційний файл", "gif", "motion", "animation", "animated", "motion design", ],
#           "Streams":
#               [ "стрім", "трансляція", "запис стріму", "stream", "live stream", "broadcast", ]},
#
#     "Finance":
#         { "Reports":
#               [ "фінансовий звіт", "звіт про доходи", "звіт про витрати", "баланс", "фінансова звітність", "дохід", "витрати", "financial report", "income report", "expense report", "balance sheet", "financial statement", "profit", "loss", ],
#           "Invoices":
#               [ "рахунок", "інвойс", "рахунок-фактура", "оплата", "платіж", "invoice", "bill", "payment", "receipt", "transaction", ],
#           "Taxes":
#               [ "податок", "податкова декларація", "податкова звітність", "пдв", "податковий облік", "tax", "tax report", "tax declaration", "vat", "tax form", ],
#           "Banking":
#               [ "банк", "банківський рахунок", "виписка", "транзакція", "переказ", "bank", "bank statement", "transaction", "transfer", "account", ],
#           "Investments":
#               [ "інвестиції", "акції", "облігації", "портфель", "ринок", "investments", "stocks", "bonds", "portfolio", "trading", ],
#           "Salary":
#               [ "зарплата", "дохід", "оплата праці", "нарахування", "salary", "payroll", "income", "wage", ],
#           "Budget":
#               [ "бюджет", "план витрат", "фінансовий план", "контроль витрат", "budget", "expense plan", "financial planning", "cost control", ]},
#
#     "Psychology":
#         { "Therapy":
#               [ "психотерапія", "терапія", "консультація", "психологічна допомога", "сеанс", "психолог", "psychotherapy", "therapy", "counseling", "session", "psychological help", ],
#           "Diagnostics":
#               [ "діагностика", "тест особистості", "психологічний тест", "оцінка стану", "аналіз поведінки", "diagnostics", "psychological test", "assessment", "evaluation", "personality test", ],
#           "Research":
#               [ "психологічне дослідження", "аналіз поведінки", "експеримент", "наукова робота", "дослідження", "psychology research", "behavior analysis", "experiment", "study", "research paper", ],
#           "Reports":
#               [ "звіт психолога", "висновок", "психологічний звіт", "аналіз клієнта", "psychology report", "evaluation report", "assessment report", ],
#           "Methods":
#               [ "методика", "підхід", "техніка", "психологічна практика", "інструменти", "method", "technique", "approach", "practice", "tools", ],
#           "Coaching":
#               [ "коучинг", "особистісний розвиток", "мотивація", "менторство", "план розвитку", "coaching", "mentoring", "motivation", "personal growth plan", ]},
#
#     "Industry":
#         { "Manufacturing":
#               [ "виробництво", "виробничий процес", "лінія виробництва", "завод", "фабрика", "виготовлення", "manufacturing", "production", "factory", "plant", "assembly line", "industrial process", ],
#           "Engineering":
#               [ "інженерія", "інженерний проєкт", "технічне рішення", "розробка", "конструкція", "engineering", "engineering project", "technical solution", "design", "construction", ],
#           "Automation":
#               [ "автоматизація", "автоматизована система", "керування процесом", "роботизація", "control system", "automation", "automated system", "process control", "robotics", ],
#           "Electronics":
#               [ "електроніка", "електронні компоненти", "схема", "плата", "pcb", "мікросхема", "electronics", "circuit", "pcb", "microcontroller", "electronic components", ],
#           "Mechanics":
#               [ "механіка", "механічна система", "деталь", "механізм", "конструкція", "mechanics", "mechanical system", "mechanism", "part", "assembly", ],
#           "QualityControl":
#               [ "контроль якості", "перевірка", "дефекти", "тестування", "інспекція", "quality control", "inspection", "testing", "defects", ],
#           "Safety":
#               [ "техніка безпеки", "інструкція безпеки", "охорона праці", "ризики", "safety", "safety instruction", "risk", "hazard", ]},
#
#     "Energy":
#         { "PowerGeneration":
#               [ "генерація енергії", "електростанція", "теплова станція", "атомна станція", "гідроелектростанція", "energy generation", "power plant", "thermal power", "nuclear power", "hydropower",],
#           "Renewable":
#               [ "відновлювана енергія", "сонячна енергія", "вітрова енергія", "сонячні панелі", "альтернативна енергія", "renewable energy", "solar energy", "wind energy", "solar panels", "green energy",],
#           "Electrical":
#               [ "електрика", "електромережа", "напруга", "струм", "електрична система", "electricity", "power grid", "voltage", "current", "electrical system",],
#           "Distribution":
#               [ "розподіл енергії", "електромережа", "передача енергії", "трансформатор", "distribution", "power distribution", "transmission", "transformer",],
#           "OilGas":
#               ["нафта", "газ", "нафтова промисловість", "газова промисловість", "видобуток", "oil", "gas", "oil industry", "gas industry", "extraction",],
#           "Efficiency":
#               [ "енергоефективність", "споживання енергії", "економія енергії", "оптимізація", "energy efficiency", "energy consumption", "optimization", "saving energy",]},
#
#     "Transport":
#         { "Cars":
#               [ "автомобіль", "машина", "легковий автомобіль", "двигун", "авто", "car", "vehicle", "engine", "automobile", "sedan", ],
#           "Trucks":
#               [ "вантажівка", "фура", "вантажний транспорт", "перевезення вантажів", "truck", "lorry", "cargo transport", "freight", ],
#           "PublicTransport":
#               [ "громадський транспорт", "автобус", "трамвай", "метро", "маршрутка", "public transport", "bus", "tram", "metro", ],
#           "Railway":
#               [ "залізниця", "поїзд", "вагон", "локомотив", "railway", "train", "wagon", "locomotive", ],
#           "Aviation":
#               [ "авіація", "літак", "аеропорт", "політ", "пілот", "aviation", "aircraft", "plane", "flight", "airport", ],
#           "Marine":
#               [ "морський транспорт", "корабель", "судно", "порт", "sea transport", "ship", "vessel", "port", ],
#           "Logistics":
#               [ "логістика", "доставка", "маршрут", "перевезення", "ланцюг постачання", "logistics", "delivery", "route", "supply chain", ],
#           "Maintenance":
#               [ "обслуговування", "ремонт", "техогляд", "діагностика авто", "maintenance", "repair", "service", "inspection", ]},
#
#     "Business":
#         { "Strategy":
#               [ "бізнес стратегія", "стратегія розвитку", "план розвитку", "аналіз ринку", "позиціонування", "business strategy", "growth strategy", "market analysis", "positioning", "strategic plan", ],
#           "Management":
#               [ "управління", "менеджмент", "керування", "організація процесів", "керівник", "management", "business management", "team management", "operations", "leadership", ],
#           "Marketing":
#               [ "маркетинг", "реклама", "просування", "бренд", "аудиторія", "marketing", "advertising", "promotion", "branding", "audience", ],
#           "Sales":
#               [ "продажі", "угода", "клієнт", "комерційна пропозиція", "sales", "deal", "client", "offer", "commercial proposal", ],
#           "Projects":
#               [ "проєкт", "бізнес проєкт", "планування", "задачі", "дедлайн", "project", "project plan", "task", "deadline", "milestone", ],
#           "HR":
#               [ "персонал", "найм", "співробітник", "відбір", "кадри", "human resources", "hr", "recruitment", "employee", "hiring", ],
#           "Operations":
#               [ "операційна діяльність", "процеси", "робочі процеси", "виконання", "operations", "workflow", "process", "execution", ]},
#
#     "Law":
#         { "Contracts":
#               [ "договір", "контракт", "угода", "сторони договору", "умови договору", "contract", "agreement", "terms", "legal agreement", "contract terms", ],
#           "Regulations":
#               [ "закон", "норматив", "правило", "регуляція", "нормативний акт", "law", "regulation", "legal act", "rule", "compliance", ],
#           "Court":
#               [ "суд", "рішення суду", "позов", "судова справа", "судове рішення", "court", "lawsuit", "legal case", "court decision", ],
#           "Licenses":
#               [ "ліцензія", "дозвіл", "сертифікат", "право на діяльність", "license", "permit", "certificate", "authorization", ],
#           "Compliance":
#               [ "відповідність", "перевірка", "вимоги", "аудит", "compliance", "requirements", "audit", "regulatory", ],
#           "Policies":
#               [ "політика", "правила компанії", "внутрішні правила", "policy", "company policy", "internal rules", "guidelines", ]},
#
#     "Healthcare":
#         { "Diagnostics":
#               [ "діагноз", "обстеження", "аналізи", "результати аналізів", "медичний висновок", "diagnosis", "medical test", "analysis results", "medical report", "examination", ],
#           "Treatment":
#               [ "лікування", "терапія", "призначення", "лікар", "рецепт", "treatment", "therapy", "prescription", "doctor", "medication", ],
#           "MedicalRecords":
#               [ "медична карта", "історія хвороби", "запис пацієнта", "медичні дані", "medical record", "patient record", "health record", "medical history", ],
#           "Research":
#               [ "медичне дослідження", "клінічне дослідження", "наукова робота", "експеримент", "medical research", "clinical research", "study", "experiment", ],
#           "Pharmacy":
#               [ "ліки", "препарат", "дозування", "інструкція препарату", "medicine", "drug", "dosage", "pharmaceutical", ],
#           "Reports":
#               [ "медичний звіт", "висновок лікаря", "обстеження результат", "medical report", "doctor report", "health report", ],
#           "Insurance":
#               [ "страхування", "медичне страхування", "поліс", "insurance", "health insurance", "policy", ]},
#
#     "RealEstate":
#         { "Rent":
#               [ "оренда", "оренда квартири", "оренда будинку", "договір оренди", "знімати житло", "rent", "rental", "lease", "rent agreement", "tenant", ],
#           "Sales":
#               [ "продаж нерухомості", "купівля квартири", "угода купівлі", "продаж будинку", "sale", "real estate sale", "purchase property", "buy house", "sell apartment", ],
#           "Listings":
#               [ "оголошення", "нерухомість", "варіанти квартир", "пропозиція", "об'єкт", "listing", "property listing", "offer", "real estate offer", ],
#           "Documents":
#               [ "право власності", "документ на квартиру", "свідоцтво", "кадастр", "ownership", "property document", "certificate", "registry", ],
#           "Management":
#               [ "керування нерухомістю", "обслуговування", "орендодавець", "управління об'єктом", "property management", "maintenance", "landlord", "management", ],
#           "Evaluation":
#               [ "оцінка", "вартість нерухомості", "ціна квартири", "ринкова ціна", "evaluation", "property value", "price estimation", "market value", ]},
#
#     "Art":
#         { "Drawing":
#               [ "малюнок", "ескіз", "ілюстрація", "рисунок", "графіка", "drawing", "sketch", "illustration", "artwork", "graphics", ],
#           "Painting":
#               [ "живопис", "картина", "полотно", "фарби", "painting", "art painting", "canvas", "oil painting", "watercolor", ],
#           "DigitalArt":
#               [ "цифрове мистецтво", "digital art", "concept art", "render", "3d art", "art design", "цифровий арт", ],
#           "Photography":
#               [ "фотографія", "фотоарт", "художнє фото", "photography", "photo art", "creative photo", ],
#           "Concepts":
#               [ "концепт", "арт концепт", "ідея дизайну", "візуальна концепція", "concept", "concept art", "visual idea", "design concept", ],
#           "Portfolios":
#               [ "портфоліо", "роботи", "збірка робіт", "art portfolio", "portfolio", "art collection", ]},
#
#     "Music":
#         { "Production":
#               [ "музичне виробництво", "створення музики", "аранжування", "біт", "трек створення", "music production", "beat making", "arrangement", "track production", "producer", ],
#           "Recording":
#               [ "запис", "студія", "запис вокалу", "аудіо запис", "recording", "studio recording", "voice recording", "audio session", ],
#           "Mixing":
#               [ "мікс", "зведення", "обробка звуку", "баланс", "mixing", "sound mixing", "audio mixing", "balance", ],
#           "Mastering":
#               [ "мастеринг", "фінальна обробка", "завершення треку", "mastering", "final processing", "track mastering", ],
#           "Composition":
#               [ "композиція", "музична ідея", "мелодія", "гармонія", "composition", "melody", "harmony", "music idea", ],
#           "Sheets":
#               [ "ноти", "партитура", "музичний лист", "sheet music", "score", "music sheet", ],
#           "Projects":
#               [ "проект fl studio", "ableton проект", "logic project", "music project", "daw project", ]},
#
#     "Architecture":
#         { "Designs":
#               [ "архітектурний проєкт", "план будівлі", "планування", "архітектурний дизайн", "архітектурна схема", "architectural design", "building plan", "floor plan", "layout", "architecture project", ],
#           "Drawings":
#               [ "креслення", "архітектурне креслення", "схема будівлі", "технічний план", "drawing", "architectural drawing", "blueprint", "technical drawing", ],
#           "3DModels":
#               [ "3d модель будівлі", "візуалізація", "рендер будинку", "3d проект", "3d model", "render", "visualization", "3d building", ],
#           "UrbanPlanning":
#               [ "містобудування", "план міста", "інфраструктура", "район", "urban planning", "city plan", "infrastructure", "district planning", ],
#           "Interior":
#               [ "інтер'єр", "дизайн інтер'єру", "план кімнати", "оформлення", "interior", "interior design", "room layout", "decoration", ],
#           "ConstructionDocs":
#               [ "будівельна документація", "документи будівництва", "проєкт будівництва", "construction documents", "building documentation", "construction project", ]},
#
#     "Military":
#         { "Equipment":
#               [ "військова техніка", "озброєння", "зброя", "танк", "бронетехніка", "artillery", "weapon", "military equipment", "tank", "armored vehicle", "weapon system", ],
#           "Aviation":
#               [ "військова авіація", "винищувач", "бомбардувальник", "бойовий літак", "дрон", "military aviation", "fighter jet", "bomber", "combat aircraft", "uav", "drone", ],
#           "Naval":
#               [ "військово-морські сили", "корабель", "флот", "підводний човен", "navy", "naval forces", "warship", "submarine", "fleet", ],
#           "Strategy":
#               [ "стратегія", "тактика", "операція", "бойові дії", "планування бою", "military strategy", "tactics", "operation", "combat planning", ],
#           "Intelligence":
#               [ "розвідка", "дані розвідки", "аналіз", "спостереження", "intelligence", "reconnaissance", "analysis", "surveillance", ],
#           "Logistics":
#               [ "військова логістика", "постачання", "перевезення", "забезпечення", "military logistics", "supply", "deployment", ],
#           "Training":
#               [ "тренування", "підготовка", "навчання військових", "курс", "training", "military training", "exercise", ]},
#
#     "Sport":
#         { "Training":
#               [ "тренування", "план тренувань", "вправи", "фітнес", "програма тренувань", "training", "workout", "exercise", "fitness", "training plan", ],
#           "Nutrition":
#               [ "харчування", "дієта", "спортивне харчування", "раціон", "nutrition", "diet", "meal plan", "sports nutrition", ],
#           "Programs":
#               [ "програма", "тренувальна програма", "план занять", "fitness program", "training program", "exercise plan", ],
#           "Competitions":
#               [ "змагання", "турнір", "результати", "чемпіонат", "competition", "tournament", "results", "championship", ],
#           "Coaching":
#               [ "тренер", "коуч", "план тренера", "наставник", "coach", "coaching", "trainer", ],
#           "Tracking":
#               [ "прогрес", "результати тренувань", "статистика", "замір", "progress", "tracking", "stats", "performance", ]},
#
#     "Travel":
#         { "Plans":
#               [ "план подорожі", "маршрут", "поїздка", "відпустка", "подорож", "travel plan", "trip plan", "itinerary", "route", "vacation", ],
#           "Tickets":
#               [ "квиток", "бронювання", "переліт", "поїзд", "ticket", "booking", "flight ticket", "train ticket", ],
#           "Hotels":
#               [ "готель", "бронювання готелю", "проживання", "номер", "hotel", "hotel booking", "accommodation", "reservation", ],
#           "Guides":
#               [ "гайд", "путівник", "рекомендації", "що відвідати", "guide", "travel guide", "recommendations", "places to visit", ],
#           "Documents":
#               [ "віза", "паспорт для поїздки", "страховка", "документи для подорожі", "visa", "travel document", "insurance", ],
#           "Experiences":
#               [ "враження", "подорожній щоденник", "відгук", "опис поїздки", "experience", "travel diary", "review", "trip notes", ]}}
#
# MAIN_CATEGORY_DESCRIPTIONS: dict[str, str] = {
#     "Study": (
#         "education learning university college school lectures laboratory works reports "
#         "assignments coursework research academic materials навчання освіта університет "
#         "лекції лабораторні звіти завдання курсова дослідження" ),
#     "Documents": (
#         "official documents forms certificates applications manuals contracts instructions "
#         "administrative paperwork документи офіційні форми сертифікати заяви інструкції договори" ),
#     "IT": (
#         "software programming code development databases cybersecurity networks systems "
#         "applications computers програмування розробка коду бази даних кібербезпека мережі системи" ),
#     "Books": (
#         "books literature reading textbook reference fiction non-fiction book materials "
#         "книги література читання підручник довідник" ),
#     "Personal": (
#         "personal private files notes diary cv identity reminders personal records "
#         "особисті приватні файли нотатки щоденник резюме" ),
#     "Media": (
#         "images video audio screenshots recordings multimedia content visual media "
#         "зображення відео аудіо скріншоти записи мультимедіа" ),
#     "Finance": (
#         "money accounting invoices taxes salary banking payments budget investments "
#         "фінанси бухгалтерія інвойси податки зарплата банк платежі бюджет інвестиції" ),
#     "Psychology": (
#         "psychology therapy counseling behavior assessment diagnostics coaching methods "
#         "психологія терапія консультування поведінка оцінка діагностика" ),
#     "Industry": (
#         "industry manufacturing engineering automation electronics mechanics production "
#         "quality control industrial systems промисловість виробництво інженерія автоматизація електроніка" ),
#     "Energy": (
#         "energy electricity power generation power systems renewable oil gas electrical infrastructure "
#         "енергетика електрика генерація енергії електросистеми відновлювана енергія нафта газ" ),
#     "Transport": (
#         "transport vehicles cars trucks railway aviation marine logistics maintenance "
#         "транспорт автомобілі вантажівки залізниця авіація логістика обслуговування" ),
#     "Business": (
#         "business management strategy marketing sales projects operations human resources "
#         "бізнес управління стратегія маркетинг продажі проєкти операційна діяльність" ),
#     "Law": (
#         "law legal regulations contracts court policies licenses compliance "
#         "право юридичні норми договори суд політики ліцензії відповідність" ),
#     "Medicine": (
#         "medicine healthcare diagnosis treatment pharmacy medical records examination "
#         "медицина охорона здоров'я діагностика лікування ліки медичні записи" ),
#     "RealEstate": (
#         "real estate property rent apartments houses ownership listings property management "
#         "нерухомість оренда квартири будинки власність оголошення" ),
#     "Art": (
#         "art drawing painting illustration digital art photography creative works "
#         "мистецтво малюнок живопис ілюстрація цифрове мистецтво фотографія" ),
#     "Music": (
#         "music production recording mixing mastering composition audio projects "
#         "музика продакшн запис зведення мастеринг композиція аудіо" ),
#     "Architecture": (
#         "architecture building design floor plans drawings blueprints interior urban planning "
#         "архітектура проєктування будівель плани креслення інтер'єр містобудування" ),
#     "Military": (
#         "military weapons equipment tactics operations intelligence logistics aviation defense "
#         "військова справа зброя техніка тактика операції розвідка логістика авіація оборона" ),
#     "Sport": (
#         "sport training fitness exercise coaching competitions nutrition performance "
#         "спорт тренування фітнес вправи тренер змагання харчування" ),
#     "Travel": (
#         "travel trips routes tickets hotels tourism vacation booking destinations "
#         "подорожі поїздки маршрути квитки готелі туризм відпустка бронювання" ),
#     "Misc": (
#         "miscellaneous unknown mixed uncategorized unclear other "
#         "різне невідоме змішане некатегоризоване неясне" ), }
