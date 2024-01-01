# Перевірка перенесення налаштувань логера у модулі
import logging

logging.warning('From module')

def log_warning() :
    logging.warning('From function')
    