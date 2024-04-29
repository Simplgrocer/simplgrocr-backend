from typing import List, Tuple
from fpdf import FPDF


def generate_grocery_list_summary(
    name: str,
    total_price: int,
    grocery_list_items: List[Tuple],
    description: str = None,
) -> bytearray:
    pdf = FPDF(orientation="landscape")

    pdf.add_page()

    pdf.set_font("Times", "B", size=20)
    pdf.write(5, name)
    pdf.ln(10)

    pdf.set_font("Times", size=14)
    pdf.write(5, description if description else "")
    pdf.ln(15)

    with pdf.table(
        text_align="LEFT",
    ) as table:
        for data_row in grocery_list_items:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

        pdf.set_font("Times", "B", size=14)

        row = table.row()
        row.cell("Total", colspan=7)
        row.cell(str(total_price), colspan=1)

    return pdf.output()
