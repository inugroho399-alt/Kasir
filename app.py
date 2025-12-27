
from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        nama = request.form.get("nama")
        diskon = int(request.form.get("diskon") or 0)
        pajak = int(request.form.get("pajak") or 0)
        diterima = int(request.form.get("diterima") or 0)

        items=[]
        subtotal_all=0
        for n,q,h in zip(
            request.form.getlist("item_nama[]"),
            request.form.getlist("item_qty[]"),
            request.form.getlist("item_harga[]")
        ):
            if n:
                sub=int(q)*int(h)
                subtotal_all+=sub
                items.append(dict(nama=n,qty=q,harga=h,subtotal=sub))

        pot_diskon = subtotal_all*diskon/100
        pot_pajak = subtotal_all*pajak/100
        total = subtotal_all - pot_diskon + pot_pajak
        kembalian = diterima - total
        kurang = kembalian < 0

        nota_id = f"PK-{random.randint(1000,9999)}"
        waktu = datetime.now().strftime("%d %b %Y %H:%M")

        return render_template("nota.html",
            nama=nama, items=items,
            subtotal=subtotal_all,
            diskon=diskon, pajak=pajak,
            pot_diskon=pot_diskon, pot_pajak=pot_pajak,
            total=total,
            diterima=diterima, kembalian=kembalian,
            kurang=kurang,
            nota_id=nota_id, waktu=waktu)

    return render_template("index.html")

@app.route("/laporan")
def laporan():
    return render_template("laporan.html")

if __name__=="__main__":
    app.run(debug=True)
