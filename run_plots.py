# run_plots.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.db_manager.db import Database
from src.analytics.analyzer import Analyzer
from src.analytics.infographics import generate_all_plots

if __name__ == '__main__':
    print("Подключаюсь к базе данных...")
    db = Database()
    db.connect()
    
    print("Запускаю анализ...")
    analyzer = Analyzer(db)
    results = analyzer.full_analysis()
    
    print("Генерирую графики...")
    generate_all_plots(results)
    
    db.disconnect()
    print("✅ Готово! Графики сохранены в reports/plots/")
