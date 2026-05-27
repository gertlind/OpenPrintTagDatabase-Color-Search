from flask import Flask, render_template, request
from pathlib import Path
import yaml

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "openprinttag-database" / "data"


def normalize_hex(value):
    if not value:
        return ""

    value = str(value).strip().lower()

    if not value.startswith("#"):
        value = "#" + value

    if len(value) == 7:
        value += "ff"

    return value


def load_yaml_files(folder):
    items = []

    if not folder.exists():
        print(f"Databasmappen finns inte: {folder}")
        return items

    files = list(folder.rglob("*.yaml")) + list(folder.rglob("*.yml"))

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if isinstance(data, dict):
                data["_file"] = str(file.relative_to(DB_DIR))
                items.append(data)

            elif isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        entry["_file"] = str(file.relative_to(DB_DIR))
                        items.append(entry)

        except Exception as e:
            print(f"Fel vid läsning av {file}: {e}")

    return items


def text_match(search, value):
    if not search or not value:
        return False

    return search.lower() in str(value).lower()


def get_color_hex(item):
    if isinstance(item.get("primary_color"), dict):
        if item["primary_color"].get("color_rgba"):
            return normalize_hex(item["primary_color"].get("color_rgba"))

    for key in ["hex", "color_hex", "colour_hex", "color_rgba"]:
        if item.get(key):
            return normalize_hex(item.get(key))

    if isinstance(item.get("color"), str):
        return normalize_hex(item.get("color"))

    if isinstance(item.get("color"), dict):
        for key in ["hex", "rgba", "value"]:
            if item["color"].get(key):
                return normalize_hex(item["color"].get(key))

    return ""


def get_brand(item):
    brand = (
        item.get("manufacturer")
        or item.get("manufactorer")
        or item.get("vendor")
        or ""
    )

    if not brand and isinstance(item.get("brand"), dict):
        brand = item["brand"].get("slug", "")

    if not brand:
        brand = item.get("brand", "")

    if isinstance(brand, str):
        brand = brand.replace("-", " ").title()

    return brand


def get_material(item):
    material = (
        item.get("type")
        or item.get("abbreviation")
        or item.get("material")
        or ""
    )

    if isinstance(material, dict):
        material = ""

    return str(material).strip().upper()


def get_name(item):
    return (
        item.get("name")
        or item.get("display_name")
        or item.get("title")
        or ""
    )


def find_url(item):
    for key in ["url", "website", "link", "productUrl", "product_url"]:
        if item.get(key):
            return item.get(key)

    urls = item.get("urls")

    if isinstance(urls, dict):
        for value in urls.values():
            if value:
                return value

    if isinstance(urls, list):
        for value in urls:
            if value:
                return value

    links = item.get("links")

    if isinstance(links, dict):
        for value in links.values():
            if value:
                return value

    return ""


def find_photo(item):
    photos = item.get("photos") or item.get("photo") or item.get("images")

    if isinstance(photos, list) and photos:
        first = photos[0]

        if isinstance(first, str):
            return first

        if isinstance(first, dict):
            return first.get("url", "")

    if isinstance(photos, str):
        return photos

    return ""


def get_database_stats():
    filaments = load_yaml_files(DB_DIR)

    brands = set()
    materials = set()

    for item in filaments:
        brand = get_brand(item)
        material = get_material(item)

        if brand:
            brands.add(brand)

        if material:
            materials.add(material)

    return {
        "brands": len(brands),
        "materials": len(materials),
        "filaments": len(filaments),
    }


def search_filaments(manufacturer="", material="", name="", color=""):
    search_color = normalize_hex(color)

    results = []
    filaments = load_yaml_files(DB_DIR)

    print(f"Laddade {len(filaments)} YAML-objekt")

    for item in filaments:
        brand = get_brand(item)
        mat = get_material(item)
        filament_name = get_name(item)
        filament_color = get_color_hex(item)

        checks = []

        if manufacturer:
            checks.append(text_match(manufacturer, brand))

        if material:
            checks.append(text_match(material, mat))

        if name:
            checks.append(text_match(name, filament_name))

        if color:
            checks.append(filament_color == search_color)

        if checks and all(checks):
            results.append({
                "brand": brand,
                "name": filament_name,
                "color": filament_color,
                "url": find_url(item),
                "photo": find_photo(item),
                "file": item.get("_file", ""),
                "has_properties": bool(item.get("properties")),
            })

    results.sort(key=lambda x: (x["brand"], x["name"]))

    return results


@app.route("/", methods=["GET"])
def index():
    manufacturer = request.args.get("manufacturer", "").strip()
    material = request.args.get("material", "").strip()
    name = request.args.get("name", "").strip()
    color = request.args.get("color", "").strip()

    results = []

    if manufacturer or material or name or color:
        results = search_filaments(
            manufacturer=manufacturer,
            material=material,
            name=name,
            color=color
        )

    stats = get_database_stats()

    return render_template(
        "index.html",
        results=results,
        manufacturer=manufacturer,
        material=material,
        name=name,
        color=color,
        stats=stats
    )


@app.route("/properties/<path:file>")
def properties_page(file):
    yaml_file = DB_DIR / file

    if not yaml_file.exists():
        return "Filen hittades inte", 404

    with open(yaml_file, "r", encoding="utf-8") as f:
        item = yaml.safe_load(f)

    properties = item.get("properties", {})

    if not properties:
        return "Inga properties finns för detta filament", 404

    return render_template(
        "properties.html",
        brand=get_brand(item),
        name=get_name(item),
        color=get_color_hex(item),
        photo=find_photo(item),
        properties=properties
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
