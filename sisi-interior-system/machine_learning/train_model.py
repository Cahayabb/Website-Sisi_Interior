from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import psycopg2
import psycopg2.extras
import pickle
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# DB CONFIG
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host"    : os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "sisiinterior"),
    "user"    : os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "123"),
    "port"    : os.getenv("DB_PORT", "5433"),
}

MODEL_PATH = "model_estimasi.pkl"


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# ─────────────────────────────────────────────
# HELPER: SIMPAN RIWAYAT TRAINING KE DB
# ─────────────────────────────────────────────
def simpan_riwayat(nama: str, mae: float, status: str, jumlah_data: int):
    """Menyimpan hasil training ke tabel riwayat_training."""
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO riwayat_training
                (nama_training, nilai_mae, status, jumlah_data, tanggal_training)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, mae, status, jumlah_data, datetime.now()))
        conn.commit()
    except Exception as e:
        print("Gagal simpan riwayat:", e)
    finally:
        cur.close()
        conn.close()



# ─────────────────────────────────────────────
# CORE: FUNGSI TRAINING
# ─────────────────────────────────────────────
def jalankan_training():
    conn = get_conn()
    try:
        query = """
            SELECT
                luas_area,
                tingkat_kerumitan,
                durasi_pengerjaan,
                jenis_ruangan,
                jenis_pekerjaan,
                spesifikasi_design,
                harga_proyek
            FROM data_proyek
            WHERE harga_proyek IS NOT NULL
        """
        df = pd.read_sql(query, conn)

    finally:
        conn.close()

    jumlah_raw = len(df)

    # ── Cleaning ──────────────────────────────
    df = df.dropna()

    # Fix: mapping sesuai nilai aktual di database
    df["tingkat_kerumitan"] = df["tingkat_kerumitan"].str.strip().map({
        "Mudah": 1,
        "Sedang": 2,
        "Sulit" : 3,
    })

    df["luas_area"]         = pd.to_numeric(df["luas_area"],         errors="coerce")
    df["durasi_pengerjaan"] = pd.to_numeric(df["durasi_pengerjaan"], errors="coerce")
    df["harga_proyek"]      = pd.to_numeric(df["harga_proyek"],      errors="coerce")

    df = df.dropna()
    jumlah_bersih = len(df)

    if jumlah_bersih < 10:
        raise ValueError(f"Data terlalu sedikit untuk training: {jumlah_bersih} baris")

    # ── Encoding ──────────────────────────────
    df = pd.get_dummies(df, columns=[
        "jenis_ruangan",
        "jenis_pekerjaan",
        "spesifikasi_design",
    ])

    X = df.drop("harga_proyek", axis=1)
    y = df["harga_proyek"]

    # ── Training ──────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)


    # ── Evaluasi ──────────────────────────────
    pred = model.predict(X_test)
    mae  = float(mean_absolute_error(y_test, pred))

    # Status akurasi berdasarkan threshold MAE
    if mae < 2_000_000:
        status_akurasi = "Baik"
    elif mae < 5_000_000:
        status_akurasi = "Cukup"
    else:
        status_akurasi = "Perlu Ditinjau"

    # ── Simpan model ──────────────────────────
    pickle.dump({
        "model"  : model,
        "columns": X.columns.tolist(),
    }, open(MODEL_PATH, "wb"))

    # ── Simpan riwayat ────────────────────────
    nama_training = f"Training-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    simpan_riwayat(nama_training, mae, status_akurasi, jumlah_bersih)

    return {
        "nama_training" : nama_training,
        "jumlah_data"   : jumlah_bersih,
        "data_raw"      : jumlah_raw,
        "mae"           : mae,
        "status_akurasi": status_akurasi,
        "status_model"  : "Siap Digunakan",
        "tanggal"       : datetime.now().isoformat(),
    }

# ─────────────────────────────────────────────
# ENDPOINT: LATIH MODEL (tombol "Latih")
# ─────────────────────────────────────────────
@app.route("/train", methods=["POST"])
def train():
    try:
        hasil = jalankan_training()
        return jsonify({"success": True, "data": hasil}), 200
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        print("TRAIN ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────
# ENDPOINT: LATIH ULANG (hapus model lama dulu)
# ─────────────────────────────────────────────
@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
            print("Model lama dihapus.")

        hasil = jalankan_training()
        return jsonify({"success": True, "data": hasil}), 200
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        print("RETRAIN ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500

# ─────────────────────────────────────────────
# ENDPOINT: RIWAYAT TRAINING
# ─────────────────────────────────────────────
@app.route("/train/riwayat", methods=["GET"])
def riwayat_training():
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT id, nama_training, nilai_mae, status, jumlah_data, tanggal_training
            FROM riwayat_training
            ORDER BY tanggal_training DESC
            LIMIT 20
        """)
        rows = cur.fetchall()
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ─────────────────────────────────────────────
# ENDPOINT: DELETE RIWAYAT
# ─────────────────────────────────────────────
@app.route("/train/riwayat/<int:id>", methods=["DELETE"])
def delete_riwayat(id):
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("DELETE FROM riwayat_training WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ─────────────────────────────────────────────
# ENDPOINT: RINGKASAN DATASET
# ─────────────────────────────────────────────
@app.route("/train/ringkasan", methods=["GET"])
def ringkasan_dataset():
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("SELECT COUNT(*) AS total FROM data_proyek")
        total = cur.fetchone()["total"]

        cur.execute("SELECT COUNT(*) AS siap FROM data_proyek WHERE harga_proyek IS NOT NULL")
        siap = cur.fetchone()["siap"]

        cur.execute("SELECT MAX(updated_at) AS last_update FROM data_proyek")
        last_update = cur.fetchone()["last_update"]

        return jsonify({
            "success": True,
            "data": {
                "total_data"   : total,
                "data_siap"    : siap,
                "last_update"  : last_update.isoformat() if last_update else None,
                "variabel_input": ["Luas Ruangan", "Tingkat Kerumitan", "Durasi"],
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)