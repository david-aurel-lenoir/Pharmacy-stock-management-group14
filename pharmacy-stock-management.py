# Pharmacy Stock Management System
# Group 14 - Beginner Python project
# Database: MySQL (Aiven cloud)
 
import mysql.connector
from datetime import datetime, timedelta
 
# ---------- database connection info ----------
HOST = "mysql-38078a6a-alustudent-15.a.aivencloud.com"
PORT = 23193
USER = "avnadmin"
PASSWORD = "AVNS_T_4s-plq9OVOiSGcOQZ"
DATABASE = "defaultdb"
 
LOW_STOCK = 10           # quantity at or below this = low stock
DAYS_BEFORE_EXPIRY = 30  # warn when a medicine expires within this many days
