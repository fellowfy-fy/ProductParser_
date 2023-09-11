import logging
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from parser.models import ParseTask

from django.db.models import Q

from products.models import Product

log = logging.getLogger(__name__)

EXPORTS_DIR = os.getenv("EXPORTS_DIR", "exports")


def export_products(task: ParseTask):
    root = ET.Element("root")
    section_products = ET.SubElement(root, "products")
    all_products = Product.objects.filter(Q(task=task) | Q(tasks=task)).distinct().all()

    logging.info(f"Exporting {len(all_products)} products to XML...")

    for product in all_products:
        ET.SubElement(section_products, "product", name=product.name, price=str(product.price))

    date_str = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    path = os.path.join(EXPORTS_DIR, "task_" + str(task.pk), date_str + ".xml")

    logging.info(f"Writing export to: {path}...")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree = ET.ElementTree(root)
    tree.write(path)
    logging.info("Exported.")

    return path
