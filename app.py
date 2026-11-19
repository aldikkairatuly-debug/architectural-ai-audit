from google import genai
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Архитектурный ИИ-Аудит", page_icon="🏗️", layout="centered"
)

st.title("🏗️ ИИ-Аудит планировок помещений")
st.write(
    "Загрузите изображение плана или эскиза, выберите тип объекта и получите"
    " экспресс-разбор на соответствие нормам и эргономике."
)

st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите Gemini API Key:", type="password")

room_type = st.selectbox(
    "Тип объекта / помещения:",
    [
        "Квартира / жилая комната",
        "Офис / рабочее пространство",
        "Коммерческое / общественное помещение",
    ],
)

uploaded_file = st.file_uploader(
    "Выберите изображение плана (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Загруженный план", use_container_width=True)

  if st.button("🚀 Запустить анализ планировки"):
    if not api_key:
      st.error("Пожалуйста, введите Gemini API Key в боковой панели!")
    else:
      with st.spinner("ИИ анализирует планировку... Подождите несколько секунд."):
        try:
          client = genai.Client(api_key=api_key)

          prompt = (
              "Ты — эксперт по архитектуре, строительным нормам (СНиП/СП) и"
              " эргономике. Тип объекта: "
              f"{room_type}. Проанализируй изображение планировки и оформи"
              " ответ строго по разделам:\n"
              "1. **Краткое описание увиденной планировки**\n"
              "2. **Потенциальные ошибки и нарушения норм/эргономики** (проходы,"
              " зонирование, мокрые зоны, освещение/инсоляция, если видно)\n"
              "3. **Конкретные рекомендации по улучшению**\n"
              "Если на изображении не хватает деталей для точного вывода, честно"
              " укажи, чего именно не хватает."
          )

          response = client.models.generate_content(
              model="gemini-3.8-flash", contents=[image, prompt]
          )

          st.success("Анализ завершен!")
          st.markdown("### 📋 Экспертный отчет:")
          st.markdown(response.text)

          st.download_button(
              label="💾 Скачать отчёт (.txt)",
              data=response.text,
              file_name="audit_report.txt",
              mime="text/plain",
          )

        except Exception as e:
          st.error(f"Ошибка при обращении к ИИ: {e}")
