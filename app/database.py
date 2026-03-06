import sqlite3
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from fastapi import HTTPException, status

class Database:
    def __init__(self):
        self.conn =sqlite3.connect("shipment.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table("shipments")
        self.table_name = "shipments"
       
    def create_table(self, name: str):
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name}
        (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
        )
        """)
        self.conn.commit()
    
    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute(f"""SELECT MAX(id) FROM {self.table_name}""")
        max_id = self.cur.fetchone()[0]
        if max_id is None:
            max_id = 1
        else:
            max_id = max_id + 1

        self.cur.execute(f"""
            INSERT INTO {self.table_name} (id, content, weight, status) VALUES (:id, :content, :weight, :status)
        """, 
        {
            "id": max_id,
            **shipment.model_dump(),
            "status": "placed"
        })
        self.conn.commit()
        return max_id
    
    def get(self, id: int) -> ShipmentRead:
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = :id", {"id": id})
        shipment = self.cur.fetchone()
        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
        return ShipmentRead(content=shipment[1], weight=shipment[2], status=shipment[3])
    
    def update(self, id: int, shipment: ShipmentUpdate) -> ShipmentRead:
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = :id", {"id": id})
        
        row = self.cur.fetchone()
        
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
        
        self.cur.execute(f"UPDATE {self.table_name} SET status = :status WHERE id = :id", {"status": shipment.status, "id": id})
        
        self.conn.commit()
         
        return self.get(id)
    
    def delete(self, id: int) -> dict[str, str]:
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = :id", {"id": id})
        
        self.conn.commit()
        
        return {"detail": f"Shipment with id {id} deleted"}
    
    def close(self):
        self.conn.close()
    