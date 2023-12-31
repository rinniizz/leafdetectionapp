# -*- coding: utf-8 -*-
import sqlite3

def create_connection():
    conn = sqlite3.connect('disease.db')
    return conn

def insert_disease_detail(detail):
    conn = create_connection()
    cursor = conn.cursor()
    for dat in detail:
        cursor.execute("INSERT INTO disease_detail (disease, disease_name, cause, details, epidemic, treatment) VALUES ( ?, ?, ?, ?, ?, ?)",
                    dat)
    conn.commit()
    disease_detail_id = cursor.lastrowid
    conn.close()

    return disease_detail_id


# ตัวอย่างการเรียกใช้งาน insert_disease_detail
detail=[('Bacteria','โรคใบจุดมะเขือเทศ',
        'เกิดจากเชื้อรา Corynespora cassiicola',
        'อาการของโรคนี้ใกล้เคียงกับโรคใบจุดวงมาก แต่แผลบนใบมักมีขนาดเล็ก การขยาย ตัวของโรคใบจุดเกิดเป็นวงไม่ค่อยชัดเจน และแผลมักมีสีเหลืองล้อมรอบ อาการบนผลเป็นจุดเล็ก ๆ กระจายอยู่ทั่วไป แผลสีครีม หรือน้ำตาลอ่อน',
        'โรคนี้พบระบาดมากในภาคเหนือ โดยเฉพาะถ้ามีความชื้นสูง หรือมีฝนตก โรคจะ ระบาดอย่างรวดเร็ว ใบที่เป็นโรคมาก ๆ จะร่วงหลุดไป',
        'พยายามรักษาความชื้นในแปลงปลูกอย่าให้สูงมากเกินไป และเมื่อพบโรค พ่นด้วยสารป้องกันกำจัดโรคพืช เช่น เบนโนมิล คาร์เบนดาซิม'),
        ('Blight','โรคใบไหม้',
         'เกิดจากเชื้อรา Phytophthora infestans',
         'จะพบปรากฏอยู่บนใบส่วนล่าง ๆ ของต้นก่อน โดยเกิดเป็นจุดฉ่ำน้ำสีเขียวเข้มเหมือน ใบถูกน้ำร้อนลวก รอยช้ำนี้จะขยายขนาดออกไปอย่างรวดเร็วทางด้านใต้ใบ โดยเฉพาะขอบ ๆ แผล จะสังเกตเห็นเส้นใยสีขาวอยู่รอบ ๆ รอยช้ำนั้น เมื่อเชื้อเจริญมากขึ้นใบจะแห้ง อาการที่กิ่งและลำต้นเป็นแผลสีดำ อาการบนผลมีรอยช้ำเหมือนถูกน้ำร้อนลวก',
         'โรคนี้พบระบาดมากทางภาคเหนือของประเทศไทยในฤดูหนาว เพราะสภาพแวดล้อม เหมาะต่อการเกิดโรค โดยมีอุณหภูมิเฉลี่ย 18-28 องศาเซลเซียส และมีความชื้นสัมพัทธ์สูงกว่า 90 % ในเขตที่อุณหภูมิต่ำและความชื้นต่ำโรคจะไม่ระบาดนอกจากมีฝนโปรยลงมาโรคจะระบาดอย่างรุนแรงและรวดเร็วภายหลังจากที่มีฝน ส่วนของพืชที่ถูกเชื้อเข้าทำลายจะตายภายใน 1 สัปดาห์',
         'ถ้าปลูกมะเขือเทศแบบยกค้าง ควรตัดแต่งใบล่างให้โปร่ง และเมื่อเริ่มพบโรค ควรใช้สารป้องกันกำจัดโรคพืช เช่น คลอโรทาโลนิล เมตาแลกซิล + แมนโคเซบ พ่นให้ทั่วทั้งต้น'),
        ('Leaf','ใบมะเขือเทศ','-','-','-','-'),
        ('Mold','โรครากำมะหยี่',
         'เกิดจากเชื้อรา Cladosporium fulvum',
         'ผิวด้านบนของใบแก่เป็นจุดสีขาว ซึ่งขยายออกอย่างรวดเร็วและเปลี่ยนเป็นสีเหลือง ใต้ใบบริเวณที่เห็นเป็นสีเหลืองมีขุยสีกำมะหยี่ เมื่อโรคระบาดรุนแรงมากขึ้นใบจะแห้ง',
         'โรคนี้จะพบมากในมะเขือเทศที่ปลูกในฤดูฝน หรือมีฝนตกระหว่างฤดูปลูกปกติ เชื้อรา จะสร้างสปอร์จำนวนมากทางด้านใต้ใบ สปอร์นี้สามารถทนต่อสภาพอากาศที่ไม่เหมาะสม และมีชีวิตอยู่ได้นานหลายเดือน เชื้อราเข้าทำลายใบแก่ที่อยู่ทางตอนล่าง ๆ ของต้น และอยู่ทางด้านใต้ใบ',
         'ตัดแต่งกิ่งมะเขือเทศเพื่อให้การหมุนเวียนของอากาศในแปลงดีขึ้น และเมื่อเริ่มพบโรค ควรพ่นด้วยสารป้องกันกำจัดโรคพืชบางชนิด เช่น แมนโคเซบ เบนโนมิล คาร์เบนดาซิม'),
        ('Normal','ใบปกติ','-','-','-','-'),
        ('Yellow_Virus','ไวรัสใบหงิกเหลืองมะเขือเทศ',
         'เกิดจากบีโกโมไวรัส (Begomovirus)',
         'ใบอ่อนที่แตกใหม่มีขนาดเล็ก ขอบใบม้วนงอ ผิวใบไม่เรียบและมีสีเหลือง ต่อมา ใบยอดเป็นพุ่มและหงิกเหลือง ช่อดอกฝ่อทำให้ดอกหลุดร่วงง่าย ถ้าเชื้อเข้าทำลายตั้งแต่ระยะต้นกล้า พืชแสดงอาการของโรคอย่างรุนแรง ต้นแคระแกร็นมาก และไม่ติดดอกออกผล',
         'ในสภาพธรรมชาติโรคนี้แพร่ระบาดโดยมีแมลงหวี่ขาวยาสูบ (Bemisia tabaci) เป็น พาหะนำโรค ซึ่งเจริญและขยายพันธุ์ได้ดีในเขตร้อน มักพบระบาดรุนแรงในฤดูแล้ง มีพืชอาศัยส่วนใหญ่ อยู่ในวงศ์ Solanaceae เช่น มะเขือเทศ มะเขือยาว มะเขือเปราะ พริก ยาสูบใบเล็ก และลำโพง รวมทั้ง วัชพืชอีกหลายชนิด เช่น สาบแร้งสาบกา กะเม็ง โทงเทง ครอบจักรวาล ไม้กวาด หญ้ายาง และกระทกรก',
         'หว่านแปลงเพาะกล้าด้วยสารฆ่าแมลง คาร์โบฟูราน ก่อนหว่านเมล็ดมะเขือเทศ หลังย้ายกล้า ควรพ่นสารกำจัดแมลงหวี่ขาว เช่น คาร์โบซัลแฟน หรืออิมิดาโคลพริด โดยเฉพาะในช่วงอากาศอบอ้าว เพราะเป็นช่วงที่ประชากรของแมลงหวี่ขาวทวีจำนวนอย่างรวดเร็ว และถอนต้นพืชเป็นโรค เผาทำลายทิ้งทันทีที่พบ และวิธีทางเขตกรรม เช่น การกำจัดพืชอาศัยชนิดอื่นในแปลงปลูก รวมทั้งวัชพืชที่แสดงอาการ ใบด่างเหลืองหรือใบหงิกเหลือง เพื่อกำจัดแหล่งสะสมของเชื้อและแมลงพาหะ สุดท้ายปลูกพืชหมุนเวียนที่ไม่ใช่พืชอาศัยของไวรัส'
         )]

insert_disease_detail(detail)
