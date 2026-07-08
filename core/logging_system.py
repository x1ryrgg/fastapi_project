import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # ← Запись в файл
        logging.StreamHandler()          # ← Вывод в консоль (опционально)
    ]
)

logger = logging.getLogger(__name__)
