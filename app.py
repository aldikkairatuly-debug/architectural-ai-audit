from google import genai
from PIL import Image
import streamlit as st

# 1. Настройка страницы (широкий макет)
st.set_page_config(
    page_title="Architectural AI Audit | ArchiTech",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Кастомные стили в архитектурной эстетике
st.markdown(
    """
    <style>
        /* Убираем лишние отступы сверху и системный футер */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Верхний баннер проекта */
        .hero-card {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 1.4rem 1.8rem;
            color: #f8fafc;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
        }
        .hero-badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 999px;
            padding: 0.2rem 0.75rem;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.55rem;
            letter-spacing: 0.02em;
        }
        .hero-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
            color: #ffffff;
        }
        .hero-sub {
            font-size: 0.96rem;
            color: #cbd5e1;
            margin: 0;
            line-height: 1.5;
        }

        /* Карточка отчета */
        .report-box {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            border-radius: 12px;
            padding: 1.25rem 1.4rem;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }

        /* Кнопка запуска */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
            transform: translateY(-1px);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Боковая панель настроек
with st.sidebar:
    st.markdown("### ⚙️ Настройки / Баптаулар")
    lang = st.radio(
        "Язык интерфейса и отчёта / Тіл:",
        ["Русский", "Қазақша"],
        horizontal=True,
    )

    api_key = st.text_input(
        "Gemini API Key:" if lang == "Русский" else "Gemini API Key енгізіңіз:",
        type="password",
        placeholder="AIzaSy...",
    )

    st.divider()
    st.markdown(
        "**Команда:** ArchiTech (АЖиОЗ 25-14)\n\n"
        "**Модель:** `gemini-2.5-flash` (Vision)\n\n"
        "**Назначение:** экспресс-проверка планировок и ручных эскизов на эргономику и нормы (СНиП / СП РК)."
        if lang == "Русский"
        else "**Команда:** ArchiTech (АЖиОЗ 25-14)\n\n"
        "**Модель:** `gemini-2.5-flash` (Vision)\n\n"
        "**Мақсаты:** жоспарлаулар мен қолмен сызылған эскиздерді эргономика мен құрылыс нормаларына (ҚНжЕ / ҚР ЕЖ) жылдам тексеру."
    )

# 4. Верхний баннер
if lang == "Русский":
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-badge">📐 ARCHITECH • ARCHITECTURAL AI AUDIT</div>
            <h1 class="hero-title">Интеллектуальный экспресс-аудит планировок</h1>
            <p class="hero-sub">
                Загрузите изображение плана или ручного эскиза, выберите тип объекта и получите
                структурированный разбор по эргономике, зонированию и строительным нормам.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-badge">📐 ARCHITECH • ARCHITECTURAL AI AUDIT</div>
            <h1 class="hero-title">Сәулеттік жоспарлауларға интеллектуалды экспресс-аудит</h1>
            <p class="hero-sub">
                Жоспардың немесе қолмен сызылған эскиздің суретін жүктеңіз, нысан түрін таңдаңыз
                және эргономика мен құрылыс нормалары бойынша жылдам сараптамалық есеп алыңыз.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 5. Основной двухколоночный интерфейс
col_left, col_right = st.columns([1, 1.15], gap="large")

with col_left:
    st.subheader("1. Исходные данные" if lang == "Русский" else "1. Бастапқы деректер")

    room_options = (
        [
            "Квартира / жилая комната",
            "Офис / рабочее пространство",
            "Коммерческое / общественное помещение",
        ]
        if lang == "Русский"
        else [
            "Пәтер / тұрғын бөлме",
            "Кеңсе / жұмыс кеңістігі",
            "Коммерциялық / қоғамдық ғимарат",
        ]
    )

    room_type = st.selectbox(
        "Тип объекта / помещения:" if lang == "Русский" else "Нысан / бөлме түрі:",
        room_options,
    )

    uploaded_file = st.file_uploader(
        "Выберите изображение плана или эскиза (PNG, JPG, JPEG)"
        if lang == "Русский"
        else "Жоспар немесе эскиз суретін таңдаңыз (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
    )

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption=(
                f"Загруженный план ({image.size[0]}×{image.size[1]} px)"
                if lang == "Русский"
                else f"Жүктелген жоспар ({image.size[0]}×{image.size[1]} px)"
            ),
            use_container_width=True,
        )

        analyze_clicked = st.button(
            "🚀 Запустить анализ планировки"
            if lang == "Русский"
            else "🚀 Жоспарлауды талдауды бастау"
        )
    else:
        analyze_clicked = False
        st.info(
            "👈 Загрузите фото чертежа или файл планировки, чтобы начать экспресс-аудит."
            if lang == "Русский"
            else "👈 Экспресс-аудитті бастау үшін сызба фотосын немесе жоспар суретін жүктеңіз."
        )

with col_right:
    st.subheader("2. Результат ИИ-аудита" if lang == "Русский" else "2. ЖИ-аудит нәтижесі")

    if uploaded_file is not None and analyze_clicked:
        if not api_key:
            st.error(
                "Пожалуйста, введите Gemini API Key в боковой панели слева!"
                if lang == "Русский"
                else "Сол жақтағы бүйірлік панельге Gemini API Key енгізіңіз!"
            )
        else:
            status_label = (
                "ИИ анализирует планировку..."
                if lang == "Русский"
                else "ЖИ жоспарлауды талдап жатыр..."
            )
            with st.status(status_label, expanded=True) as status:
                try:
                    st.write(
                        "• Подключение к Google Gemini Vision API..."
                        if lang == "Русский"
                        else "• Google Gemini Vision API желісіне қосылу..."
                    )
                    client = genai.Client(api_key=api_key)

                    if lang == "Русский":
                        prompt = (
                            "Ты — эксперт по архитектуре, строительным нормам (СНиП/СП РК) и"
                            " эргономике. Тип объекта: "
                            f"{room_type}. Проанализируй изображение планировки (включая ручные эскизы) и оформи"
                            " ответ строго по разделам:\n"
                            "1. **Краткое описание увиденной планировки**\n"
                            "2. **Потенциальные ошибки и нарушения норм/эргономики** (проходы,"
                            " зонирование, мокрые зоны, открывание дверей, освещение/инсоляция, если видно)\n"
                            "3. **Конкретные рекомендации по улучшению**\n"
                            "Если на изображении не хватает размеров или деталей для точного вывода, честно"
                            " укажи, чего именно не хватает."
                        )
                    else:
                        prompt = (
                            "Сен сәулет, құрылыс нормалары (ҚНжЕ / ҚР ЕЖ) және эргономика бойынша сарапшысың."
                            f" Нысан түрі: {room_type}. Жүктелген жоспардың немесе қолмен сызылған эскиздің суретін талдап,"
                            " жауапты қазақ тілінде мына бөлімдер бойынша нақты рәсімде:\n"
                            "1. **Жоспарлаудың қысқаша сипаттамасы**\n"
                            "2. **Эргономика мен құрылыс нормалары бойынша ықтимал қателіктер** (өту жолдарының ені,"
                            " аймақтарға бөлу, ылғалды аймақтар, есіктердің ашылуы, табиғи жарық)\n"
                            "3. **Жақсарту және түзету бойынша нақты ұсыныстар**\n"
                            "Егер суретте өлшемдер немесе бөлшектер жеткіліксіз болса, не жетіспейтінін ашық көрсет."
                        )

                    st.write(
                        "• Проверка геометрии, проходов и функциональных зон..."
                        if lang == "Русский"
                        else "• Геометрияны, өту жолдарын және аймақтарды тексеру..."
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash", contents=[image, prompt]
                    )

                    st.session_state["audit_result"] = response.text
                    status.update(
                        label="Анализ завершён!" if lang == "Русский" else "Талдау аяқталды!",
                        state="complete",
                        expanded=False,
                    )

                except Exception as e:
                    status.update(
                        label="Ошибка при анализе" if lang == "Русский" else "Талдау қатесі",
                        state="error",
                    )
                    st.error(f"Ошибка при обращении к ИИ: {e}")

    if "audit_result" in st.session_state and st.session_state["audit_result"]:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(st.session_state["audit_result"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="💾 Скачать отчёт (.txt)" if lang == "Русский" else "💾 Есепті жүктеу (.txt)",
            data=st.session_state["audit_result"],
            file_name="architectural_audit_report.txt",
            mime="text/plain",
            use_container_width=True,
        )
    elif not analyze_clicked:
        st.markdown(
            """
            <div class="report-box" style="color: #475569;">
                <b>Здесь появится экспертный разбор планировки:</b><br><br>
                • Краткое описание структуры помещений<br>
                • Проверка ширины проходов, зонирования и мокрых зон<br>
                • Практические рекомендации по исправлению ошибок
            </div>
            """
            if lang == "Русский"
            else """
            <div class="report-box" style="color: #475569;">
                <b>Мұнда жоспарлаудың сараптамалық есебі шығады:</b><br><br>
                • Бөлме құрылымының қысқаша сипаттамасы<br>
                • Өту жолдарының енін, аймақтарға бөлуді және ылғалды аймақтарды тексеру<br>
                • Қателіктерді түзету бойынша нақты ұсыныстар
            </div>
            """,
            unsafe_allow_html=True,
        )
