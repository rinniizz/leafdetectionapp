import sqlite3

def create_connection():
    conn = sqlite3.connect('disease.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS disease_statics (
                    bacteria REAL,
                    blight REAL,
                    leaf REAL,
                    mold REAL,
                    normal REAL,
                    yellow_virus REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS disease_detail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease TEXT,
                    disease_name TEXT NOT NULL,
                    cause TEXT,
                    details TEXT,
                    epidemic TEXT,
                    treatment TEXT
                    )''')
    
    conn.commit()
    conn.close()

def insert_disease_statics(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO disease_statics (bacteria, blight, leaf, mold, normal, yellow_virus) VALUES (?, ?, ?, ?, ?, ?)",
               (data['Bacteria'], data['Blight'], data['Leaf'], data['Mold'], data['Normal'], data['Yellow_Virus']))

    conn.commit()
    disease_statics_id = cursor.lastrowid
    conn.close()

    return disease_statics_id

def get_top_disease_detail(data):
    conn = create_connection()
    cursor = conn.cursor()
    # ค้นหา top_disease จากข้อมูลที่ส่งเข้ามา
    max_value = max(data.values())
    max_disease = [k for k, v in data.items() if v == max_value][0]
    print(max_disease)
    cursor.execute("SELECT disease_name,cause,details,epidemic,treatment FROM disease_detail WHERE disease = ?", (max_disease,))
    result = cursor.fetchone()

    print(result)
    conn.close()

    return result

def get_static():
    conn = create_connection()
    cursor = conn.cursor()
    
    # คำนวณผลรวมของจำนวนแต่ละโรค
    cursor.execute("SELECT SUM(bacteria), SUM(blight), SUM(leaf), SUM(mold), SUM(normal), SUM(yellow_virus) FROM disease_statics")
    result = cursor.fetchone()
    
    # คำนวณค่าสถิติรวม
    total = sum(result)
    if total > 0:
        percent = {k: round(v/total*100, 2) for k, v in zip(['Bacteria', 'Blight', 'Leaf', 'Mold', 'Normal', 'Yellow_Virus'], result)}
    else:
        percent = {k: 0 for k in ['Bacteria', 'Blight', 'Leaf', 'Mold', 'Normal', 'Yellow_Virus']}
    
    conn.close()

    return percent
    

create_tables()