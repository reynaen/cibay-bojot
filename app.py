import re
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "cibay-bojot-secret-key-2026"  # ganti dengan key rahasia sendiri saat deploy

# ------------------------------------------------------------------
# Data produk (statis, sesuai brand Cibay Bojot)
# ------------------------------------------------------------------
PRODUCT = {
    "id": "cibay-bojot",
    "name": "Cibay Bojot",
    "tagline": "Cemilan Bojot Bikin Nagih!",
    "description": "Pilih level chili oil & topping gratismu. Satu produk, ribuan sensasi rasa!",
    "price": 1000,  # per pcs
    "levels": [
        {"id": "level1", "label": "Level 1", "desc": "Aman"},
        {"id": "level2", "label": "Level 2", "desc": "Nampol"},
        {"id": "level3", "label": "Level 3", "desc": "Bojot!"},
    ],
    "toppings": [
        {"id": "bawang", "label": "Bawang Goreng"},
        {"id": "daun_jeruk", "label": "Daun Jeruk"},
    ],
}

ONGKIR = 5000  # ongkos kirim flat


def format_rupiah(value):
    return f"Rp. {value:,.0f}".replace(",", ".")


app.jinja_env.filters["rupiah"] = format_rupiah


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def cart_total(cart):
    return sum(item["subtotal"] for item in cart)


# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------

@app.route("/")
def home():
    cart_count = len(get_cart())
    return render_template("home.html", product=PRODUCT, cart_count=cart_count)


@app.route("/produk", methods=["GET", "POST"])
def produk():
    cart_count = len(get_cart())

    if request.method == "POST":
        level_id = request.form.get("level")
        topping_ids = request.form.getlist("topping")
        qty = request.form.get("qty", "1")

        errors = []
        # Validasi server-side
        valid_levels = [l["id"] for l in PRODUCT["levels"]]
        valid_toppings = [t["id"] for t in PRODUCT["toppings"]]

        if level_id not in valid_levels:
            errors.append("Pilih level chili oil terlebih dahulu.")
        if not topping_ids or not all(t in valid_toppings for t in topping_ids):
            errors.append("Pilih minimal satu topping gratis.")
        try:
            qty = int(qty)
            if qty < 1 or qty > 100:
                errors.append("Jumlah pesanan harus antara 1-100 pcs.")
        except ValueError:
            errors.append("Jumlah pesanan tidak valid.")
            qty = 1

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("product.html", product=PRODUCT, cart_count=cart_count,
                                    form=request.form, selected_toppings=topping_ids)

        level = next(l for l in PRODUCT["levels"] if l["id"] == level_id)
        toppings = [t["label"] for t in PRODUCT["toppings"] if t["id"] in topping_ids]
        subtotal = PRODUCT["price"] * qty

        cart = get_cart()
        cart.append({
            "product_name": PRODUCT["name"],
            "level": level["label"],
            "topping": " & ".join(toppings),
            "qty": qty,
            "price": PRODUCT["price"],
            "subtotal": subtotal,
        })
        save_cart(cart)
        flash(f"{qty} pcs Cibay Bojot ({level['label']}) berhasil ditambahkan ke keranjang!", "success")
        return redirect(url_for("keranjang"))

    return render_template("product.html", product=PRODUCT, cart_count=cart_count, form={},
                            selected_toppings=[])


@app.route("/keranjang")
def keranjang():
    cart = get_cart()
    cart_count = len(cart)
    total = cart_total(cart)
    return render_template("cart.html", cart=cart, total=total, ongkir=ONGKIR if cart else 0,
                            grand_total=total + (ONGKIR if cart else 0), cart_count=cart_count)


@app.route("/keranjang/hapus/<int:index>", methods=["POST"])
def hapus_item(index):
    cart = get_cart()
    if 0 <= index < len(cart):
        cart.pop(index)
        save_cart(cart)
        flash("Item dihapus dari keranjang.", "info")
    return redirect(url_for("keranjang"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    cart_count = len(cart)

    if not cart:
        flash("Keranjang kamu masih kosong. Yuk pesan Cibay Bojot dulu!", "warning")
        return redirect(url_for("produk"))

    total = cart_total(cart)
    grand_total = total + ONGKIR

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        hp = request.form.get("hp", "").strip()
        email = request.form.get("email", "").strip()
        alamat = request.form.get("alamat", "").strip()
        kelurahan = request.form.get("kelurahan", "").strip()
        kecamatan = request.form.get("kecamatan", "").strip()
        kota = request.form.get("kota", "").strip()
        catatan = request.form.get("catatan", "").strip()
        metode_bayar = request.form.get("metode_bayar", "Transfer Bank / QRIS")

        errors = {}

        if len(nama) < 3:
            errors["nama"] = "Nama lengkap minimal 3 karakter."

        hp_pattern = r"^(08|\+62|62)[0-9]{8,13}$"
        if not re.match(hp_pattern, hp):
            errors["hp"] = "Format nomor HP tidak valid. Contoh: 08xxxxxxxxxx."

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            errors["email"] = "Format email tidak valid."

        if len(alamat) < 10:
            errors["alamat"] = "Alamat lengkap minimal 10 karakter."

        if not kelurahan:
            errors["kelurahan"] = "Kelurahan wajib diisi."

        if not kecamatan:
            errors["kecamatan"] = "Kecamatan wajib diisi."

        if not kota:
            errors["kota"] = "Kota / Kabupaten wajib diisi."

        if errors:
            return render_template("checkout.html", cart=cart, total=total, ongkir=ONGKIR,
                                    grand_total=grand_total, cart_count=cart_count,
                                    errors=errors, form=request.form)

        order_id = f"#CBJ-{datetime.now().year}-{random.randint(1000, 99999)}"
        session["last_order"] = {
            "order_id": order_id,
            "nama": nama,
            "hp": hp,
            "email": email,
            "alamat": alamat,
            "kelurahan": kelurahan,
            "kecamatan": kecamatan,
            "kota": kota,
            "catatan": catatan,
            "metode_bayar": metode_bayar,
            "total": grand_total,
            "cart": cart,
        }
        save_cart([])  # kosongkan keranjang setelah order
        return redirect(url_for("selesai"))

    return render_template("checkout.html", cart=cart, total=total, ongkir=ONGKIR,
                            grand_total=grand_total, cart_count=cart_count, errors={}, form={})


@app.route("/selesai")
def selesai():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("home"))
    return render_template("complete.html", order=order, cart_count=0)


if __name__ == "__main__":
    app.run(debug=True)
