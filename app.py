from flask import Flask, request, render_template
from backend import get_shops

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"


@app.route('/', methods=["GET", "POST"])
async def main():
    if request.method == "POST":
        # Get shops data from OpenStreetMap
        shops = get_shops(request.form["lat"], request.form["lon"])

        # Initialize variables
        id_counter = 0
        markers = ''
        for node in shops.nodes:

            # Create unique ID for each marker
            idd = 'shop' + str(id_counter)
            id_counter += 1

            # Check if shops have name and website in OSM
            try:
                shop_brand = node.tags['brand']
            except:
                shop_brand = 'null'

            try:
                shop_website = node.tags['website']
            except:
                shop_website = 'null'

            # Create the marker and its pop-up for each shop
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                        {idd}.addTo(map).bindPopup('{brand}<br>{website}');".format(idd=idd, latitude=node.lat,\
                                                                                     longitude=node.lon,
                                                                                     brand=shop_brand,\
                                                                                     website=shop_website)

        # Render the page with the map
        return render_template('results.html', markers=markers, lat=request.form["lat"], lon=request.form["lon"])


    else:
        # Render the input form
        return render_template('input.html')
