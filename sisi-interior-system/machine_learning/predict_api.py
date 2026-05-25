from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app) 

# load model
data = pickle.load(open("model_estimasi.pkl", "rb"))
model = data["model"]
columns = data["columns"]

# ─────────────────────────────────────────────
# KONSTANTA MULTIPLIER
# ─────────────────────────────────────────────
DURASI_NORMAL = {
    "Mudah" : 7,
    "Sedang": 14,
    "Sulit" : 21,
}

MULTIPLIER_MULTI_RUANGAN = 0.08   # +8% per ruangan tambahan
MULTIPLIER_RUSH           = 0.15  # +15% jika dikerjakan lebih cepat dari normal
MULTIPLIER_SULIT          = 0.20  # +20% jika tingkat kerumitan = Sulit


def hitung_penyesuaian(base_price: float, req: dict, jumlah_ruangan: int) -> dict:
    """
    Menghitung penyesuaian harga berdasarkan kondisi proyek.
    Mengembalikan dict berisi breakdown dan harga final.
    """
    breakdown = []
    total_multiplier = 0.0

    # ── 1. Multi Ruangan ──────────────────────────────────────
    if jumlah_ruangan > 1:
        tambahan_ruangan = jumlah_ruangan - 1
        m = tambahan_ruangan * MULTIPLIER_MULTI_RUANGAN
        total_multiplier += m
        breakdown.append({
            "kondisi"   : f"Multi ruangan ({jumlah_ruangan} ruangan)",
            "multiplier": m,
            "keterangan": f"+{tambahan_ruangan} ruangan × {MULTIPLIER_MULTI_RUANGAN*100:.0f}%"
        })

    # ── 2. Rush / Deadline Lebih Cepat ────────────────────────
    tingkat     = req.get("tingkat_kerumitan", "")
    durasi_input = int(req.get("durasi_pengerjaan", 0))
    durasi_normal = DURASI_NORMAL.get(tingkat)

    if durasi_normal and durasi_input > 0 and durasi_input < durasi_normal:
        m = MULTIPLIER_RUSH
        total_multiplier += m
        breakdown.append({
            "kondisi"   : "Pengerjaan lebih cepat dari normal (rush)",
            "multiplier": m,
            "keterangan": f"Normal {durasi_normal} hari → diminta {durasi_input} hari"
        })

    # ── 3. Tingkat Kerumitan Sulit ─────────────────────────────
    if tingkat.lower() == "sulit":
        m = MULTIPLIER_SULIT
        total_multiplier += m
        breakdown.append({
            "kondisi"   : "Tingkat kerumitan Sulit",
            "multiplier": m,
            "keterangan": f"+{MULTIPLIER_SULIT*100:.0f}% surcharge kerumitan tinggi"
        })

    harga_penyesuaian = base_price * total_multiplier
    harga_final       = base_price + harga_penyesuaian

    return {
        "base"            : base_price,
        "total_multiplier": total_multiplier,
        "penyesuaian"     : harga_penyesuaian,
        "final"           : harga_final,
        "breakdown"       : breakdown,
    }


@app.route("/predict", methods=["POST"])
def predict():
    try:
        req = request.get_json()
        print("DATA MASUK:", req)

        if not req:
            return jsonify({"error": "Request kosong"}), 400
        
        # HANDLE MULTI ROOM
        jenis_ruangan = req.get("jenis_ruangan", "")
        jumlah_ruangan = 1

        if "," in jenis_ruangan:
            ruangan_list = [r.strip() for r in jenis_ruangan.split(",")]

            # ambil ruangan pertama untuk model
            req["jenis_ruangan"] = ruangan_list[0]

            # tambahan feature opsional
            req["jumlah_ruangan"] = len(ruangan_list)
        else:
            req["jumlah_ruangan"] = 1

        req["jumlah_ruangan"] = jumlah_ruangan

        # ── VALIDASI FIELD WAJIB ──────────────────────────────
        required_fields = [
                "luas_area",
                "tingkat_kerumitan",
                "durasi_pengerjaan",
                "jenis_ruangan",
                "jenis_proyek",
                "spesifikasi_design"
            ]

        # VALIDASI FIELD
        for field in required_fields:
            if field not in req or req[field] in [None, ""]:
                return jsonify({"error": f"{field} wajib diisi"}), 400

        # convert ke dataframe
        df = pd.DataFrame([req])
        # encoding (HARUS sama seperti training)
        df = pd.get_dummies(df)
        # samakan kolom dengan model
        df = df.reindex(columns=columns, fill_value=0)

        base_price = float(model.predict(df)[0])
        print("BASE PRICE:", base_price)

        # ── PENYESUAIAN HARGA ─────────────────────────────────
        hasil = hitung_penyesuaian(base_price, req, jumlah_ruangan)
        print("HASIL FINAL:", hasil)

        return jsonify({
            "estimasi"        : hasil["final"],
            "estimasi_base"   : hasil["base"],
            "penyesuaian"     : hasil["penyesuaian"],
            "total_multiplier": hasil["total_multiplier"],
            "breakdown"       : hasil["breakdown"],
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)