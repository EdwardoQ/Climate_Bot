import sqlite3
from typing import Dict, Any, List, Tuple, Optional

TRASH_ITEMS = {
    "Plastic Bottle": 5,
    "Aluminium Can": 10,
    "Newspaper (Paper)": 3,
    "Glass Shard": 8,
    "Styrofoam Cup": 2,
    "Used Battery": 20, 
}

WATER_TRASH = {
    "Plastic Straw": 5,
    "Plastic Bag": 5,
    "Beverage Bottle": 8,
    "Ghost Net": 15,
    "Paint Can": 20,
    "Old Tire": 40,
    "Car Battery": 50,
    "Black Pearl": 150,
    "Treasure Chest": 200
}

EXPLORE_LOCATIONS = {
    "Ancient Forest": ["Tree Bark", "Dry Leaves", "Wild Berries", "Rare Orchid"],
    "Secret Beach": ["Driftwood", "Sea Glass", "Pearl Shell", "Message in a Bottle"],
    "Abandoned City": ["Scrap Metal", "Old Paper", "Copper Wire", "Antique Coin"]
}

EXPLORE_ITEMS ={
    "Tree Bark": 10,
    "Dry Leaves": 5,   
    "Wild Berries": 15,
    "Rare Orchid": 50,
    "Driftwood": 12,
    "Sea Glass": 20,
    "Pearl Shell": 50,
    "Message in a Bottle": 40,
    "Scrap Metal": 25,
    "Old Paper": 8,
    "Copper Wire": 35,
    "Antique Coin": 100 
}

SHOP_ITEMS = {
    # Format: "Item Name": Price
    "Sekop": 200,
    "Tepung Tulang": 300,
    "Sarung Tangan": 500,
    "Tas Daur Ulang": 250,
    "Jaring Pengumpul": 530,
    "Alat Pengambil": 600,
    "Teropong": 1000,
    "Ransel": 1500,
}

UNIQUE_ITEMS = {
    "Sekop",
    "Tepung Tulang",
    "Sarung Tangan",
    "Tas Daur Ulang",
    "Jaring Pengumpul",
    "Alat Pengambil",
    "Teropong",
    "Ransel",
}

class ClimateGames:
    def __init__(self, bot):
        self.bot = bot

        self.db_name = 'eco_data.db'
        self.conn: Optional[sqlite3.Connection] = None # Objek koneksi
        self.cursor: Optional[sqlite3.Cursor] = None  # Objek kursor untuk menjalankan perintah
        
        self.active_games: Dict[int, str] = {}
        self.user_states: Dict[int, Dict[str, Any]] = {} 
    
        self._setup_database()

    def _setup_database(self):
        """Menghubungkan ke database SQLite dan membuat tabel jika belum ada."""
        try:
            # 1. Hubungkan ke file database. File akan dibuat jika belum ada.
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            
            # 2. Buat tabel 'users' (untuk skor)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    score INTEGER DEFAULT 0
                )
            """)
            
            # 3. Buat tabel 'inventory' (untuk item)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    user_id INTEGER,
                    item_name TEXT NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    PRIMARY KEY (user_id, item_name),
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            try:
                self.cursor.execute("ALTER TABLE users ADD COLUMN upcycled_count INTEGER DEFAULT 0")
            except sqlite3.OperationalError:          
                pass
 
            self.conn.commit()
            print(f"Database connected: {self.db_name}")
        except sqlite3.Error as e:
            print(f"ERROR: Failed to connect or create database: {e}")

    def _ensure_user_exists(self, user_id: int):
        """Memastikan pengguna ada di tabel users sebelum operasi apapun."""
        if not self.cursor or not self.conn: return
        # INSERT OR IGNORE: jika user_id sudah ada, tidak melakukan apa-apa; jika tidak, masukkan dengan skor 0.
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, score) VALUES (?, 0)", (user_id,))
        self.conn.commit()

    def get_score(self, user_id: int) -> int:
        """Mengambil Eco-Score pengguna dari database."""
        if not self.cursor: return 0
        self._ensure_user_exists(user_id) # Memastikan pengguna ada di database
        
        # Jalankan query SELECT
        self.cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone() # Ambil baris pertama (dan satu-satunya)
        
        return result[0] if result else 0
    
    def update_score(self, user_id: int, amount: int):
        if not self.cursor or not self.conn: return

        # Pastikan pengguna ada
        self._ensure_user_exists(user_id) 
        
        # Perbarui skor di database
        self.cursor.execute(
            "UPDATE users SET score = score + ? WHERE user_id = ?",
            (amount, user_id)
        )
        self.conn.commit()

    def add_item_to_inventory(self, user_id: int, item_name: str, quantity: int = 1):
        """Menambah atau mengupdate item di inventaris pengguna."""
        if not self.cursor or not self.conn: return
        self._ensure_user_exists(user_id)
        
        # 1. Coba perbarui kuantitas jika item sudah ada
        self.cursor.execute(
            "UPDATE inventory SET quantity = quantity + ? WHERE user_id = ? AND item_name = ?",
            (quantity, user_id, item_name)
        )
        
        # 2. Jika tidak ada baris yang diperbarui (rowcount == 0), item baru. Masukkan.
        if self.cursor.rowcount == 0:
            self.cursor.execute(
                "INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, ?)",
                (user_id, item_name, quantity)
            )
            
        self.conn.commit()

    def get_inventory(self, user_id: int) -> List[Tuple[str, int]]:
        """Mengambil daftar item dan jumlahnya dari inventaris pengguna."""
        if not self.cursor: return []
        self._ensure_user_exists(user_id)
        
        self.cursor.execute(
            "SELECT item_name, quantity FROM inventory WHERE user_id = ? AND quantity > 0 ORDER BY item_name",
            (user_id,)
        )
        # fetchall() mengambil semua baris yang cocok
        return self.cursor.fetchall()
    
    def owns_item(self, user_id: int, item_name: str) -> bool:
        """Memeriksa apakah pengguna memiliki item tertentu di inventarisnya."""
        if not self.cursor: return False
        
        # 1. Pastikan pengguna ada
        self._ensure_user_exists(user_id) 
        
        # 2. Jalankan query untuk item spesifik
        self.cursor.execute(
            "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        )
        result = self.cursor.fetchone()
        
        # Item dimiliki jika hasilnya ada (bukan None) dan kuantitasnya > 0
        return result is not None and result[0] > 0
    
    def remove_item_from_inventory(self, user_id: int, item_name: str, quantity: int = 1):
        """Menghapus atau mengurangi jumlah item dari inventaris pengguna."""
        if not self.cursor or not self.conn: return False

        # 1. Cek jumlah item saat ini
        self.cursor.execute(
            "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        )
        result = self.cursor.fetchone()

        if result:
            current_qty = result[0]
            if current_qty > quantity:
                # Kurangi jumlahnya
                self.cursor.execute(
                    "UPDATE inventory SET quantity = quantity - ? WHERE user_id = ? AND item_name = ?",
                    (quantity, user_id, item_name)
                )
            else:
                # Hapus baris jika jumlah yang dihapus >= jumlah yang dimiliki
                self.cursor.execute(
                    "DELETE FROM inventory WHERE user_id = ? AND item_name = ?",
                    (user_id, item_name)
                )
            
            self.conn.commit()
            return True
        return False # Item tidak ditemukan
    
    def clear_trash_data(self, user_id: int, tool_names: list):
        """Deletes all items from inventory except for the specified tools."""
        if not self.cursor or not self.conn: return False
        
        # We use NOT IN to protect your tools from being deleted
        # The '?' placeholders are generated based on the number of tools you have
        placeholders = ', '.join(['?'] * len(tool_names))
        query = f"DELETE FROM inventory WHERE user_id = ? AND item_name NOT IN ({placeholders})"
        
        # Combine user_id and tool names into one tuple for the execution
        params = [user_id] + tool_names
        
        self.cursor.execute(query, params)
        self.conn.commit()
        return True
    
    def get_upcycled_count(self, user_id: int):
        """Mengambil total item yang telah di-upcycle oleh pengguna."""
        self.cursor.execute("SELECT upcycled_count FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def upcycle_all_trash(self, user_id: int, tool_names: list):
        """Menghitung sampah, menambah ke upcycled_count, dan menghapus item dari inventory."""
        if not self.cursor or not self.conn: return None
        
        # Ambil total SEBELUM ditambah untuk pengecekan milestone
        old_total = self.get_upcycled_count(user_id)
        
        placeholders = ', '.join(['?'] * len(tool_names))
        query_select = f"SELECT SUM(quantity) FROM inventory WHERE user_id = ? AND item_name NOT IN ({placeholders})"
        
        params = [user_id] + tool_names
        self.cursor.execute(query_select, params)
        amount_to_add = self.cursor.fetchone()[0] or 0

        if amount_to_add > 0:
            # Update total upcycled_count
            self.cursor.execute(
                "UPDATE users SET upcycled_count = upcycled_count + ? WHERE user_id = ?",
                (amount_to_add, user_id)
            )
            
            # Hapus item dari inventory
            query_delete = f"DELETE FROM inventory WHERE user_id = ? AND item_name NOT IN ({placeholders})"
            self.cursor.execute(query_delete, params)
            
            self.conn.commit()
            
            new_total = old_total + amount_to_add
            return amount_to_add, old_total, new_total
        
        return 0, old_total, old_total
    
    def recycle_all_trash(self, user_id: int, trash_prices: dict, tool_names: list):
        """Calculates total value of trash, updates score, and deletes items."""
        if not self.cursor or not self.conn: return None
        
        # 1. Fetch all items that are NOT in the tools list
        placeholders = ', '.join(['?'] * len(tool_names))
        query = f"SELECT item_name, quantity FROM inventory WHERE user_id = ? AND item_name NOT IN ({placeholders})"
        
        self.cursor.execute(query, (user_id, *tool_names))
        items = self.cursor.fetchall()

        if not items:
            return 0, 0 # No trash to recycle

        total_points_earned = 0
        total_items_count = 0

        for name, qty in items:
            # Get price from your dictionary, default to 2 points if missing
            price_per_unit = trash_prices.get(name, 2)/2
            total_points_earned += price_per_unit * qty
            total_items_count += qty

        # 2. Update the user's score
        self.update_score(user_id, total_points_earned)

        # 3. Delete the recycled items
        delete_query = f"DELETE FROM inventory WHERE user_id = ? AND item_name NOT IN ({placeholders})"
        self.cursor.execute(delete_query, (user_id, *tool_names))
        self.conn.commit()

        return total_items_count, total_points_earned
