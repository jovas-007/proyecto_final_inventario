"""
Generador de reportes PDF con ReportLab.
Genera PDFs profesionales con tema oscuro y diseño premium.
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# ── Colores del tema ──
PRIMARY = colors.HexColor('#7c3aed')
PRIMARY_LIGHT = colors.HexColor('#a78bfa')
DARK_BG = colors.HexColor('#0f0f23')
SURFACE = colors.HexColor('#1a1a3e')
BORDER = colors.HexColor('#2a2a5a')
TEXT_WHITE = colors.HexColor('#ffffff')
TEXT_MUTED = colors.HexColor('#8888aa')
SUCCESS = colors.HexColor('#22c55e')
WARNING = colors.HexColor('#eab308')
DANGER = colors.HexColor('#ef4444')
ORANGE = colors.HexColor('#f97316')

# ── Estilos ──
styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=22,
    textColor=TEXT_WHITE,
    spaceAfter=4,
    fontName='Helvetica-Bold',
)

SUBTITLE_STYLE = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=TEXT_MUTED,
    spaceAfter=20,
)

SECTION_STYLE = ParagraphStyle(
    'SectionTitle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=PRIMARY_LIGHT,
    spaceBefore=16,
    spaceAfter=8,
    fontName='Helvetica-Bold',
)

NORMAL_STYLE = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=9,
    textColor=TEXT_WHITE,
)

CELL_STYLE = ParagraphStyle(
    'CellStyle',
    parent=styles['Normal'],
    fontSize=8,
    textColor=TEXT_WHITE,
    leading=10,
)

HEADER_CELL_STYLE = ParagraphStyle(
    'HeaderCell',
    parent=styles['Normal'],
    fontSize=8,
    textColor=TEXT_WHITE,
    fontName='Helvetica-Bold',
    leading=10,
)


def _build_header(title, subtitle=None):
    """Construye el encabezado del reporte."""
    fecha = datetime.now().strftime('%d/%m/%Y  %H:%M')
    elements = [
        Paragraph(f"StockPro — {title}", TITLE_STYLE),
        Paragraph(
            f"Generado: {fecha}" + (f"  |  {subtitle}" if subtitle else ""),
            SUBTITLE_STYLE,
        ),
        HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=12),
    ]
    return elements


def _build_stat_row(stats: list):
    """Construye una fila de estadísticas tipo tarjeta."""
    data = [[]]
    for label, value, color in stats:
        cell = Paragraph(
            f'<font size="16" color="{color}"><b>{value}</b></font><br/>'
            f'<font size="7" color="#8888aa">{label}</font>',
            ParagraphStyle('stat', alignment=TA_CENTER, leading=18),
        )
        data[0].append(cell)

    col_width = 130
    table = Table(data, colWidths=[col_width] * len(stats))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SURFACE),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table


def _table_style():
    """Estilo base para tablas de datos."""
    return TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), SURFACE),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_WHITE),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [SURFACE, DARK_BG]),
    ])


def _page_background(canvas, doc):
    """Dibuja el fondo oscuro y el pie de página."""
    width, height = doc.pagesize
    canvas.saveState()
    # Fondo oscuro
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, width, height, fill=True, stroke=False)
    # Pie de página
    canvas.setFillColor(TEXT_MUTED)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(
        40, 20,
        f"StockPro — Sistema de Inventario  |  Página {doc.page}"
    )
    canvas.drawRightString(
        width - 40,
        20,
        datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
    canvas.restoreState()


def generar_inventario_completo():
    """Genera el PDF del inventario completo."""
    from models import ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30,
        bottomMargin=40,
        leftMargin=30,
        rightMargin=30,
    )

    productos = ProductoModel.query.filter_by(activo=True).order_by(ProductoModel.nombre).all()

    elements = _build_header(
        "Inventario Completo",
        f"{len(productos)} productos activos",
    )

    # Estadísticas
    total = len(productos)
    bajo_stock = sum(1 for p in productos if p.stock_actual <= p.stock_minimo)
    valor_total = sum((p.precio_venta or 0) * (p.stock_actual or 0) for p in productos)

    elements.append(_build_stat_row([
        ('Total Productos', str(total), '#a78bfa'),
        ('Stock Bajo', str(bajo_stock), '#ef4444'),
        ('Valor Inventario', f'${valor_total:,.2f}', '#22c55e'),
    ]))
    elements.append(Spacer(1, 16))

    # Tabla
    headers = ['Producto', 'Código', 'Categoría', 'Proveedor', 'P. Compra', 'P. Venta', 'Stock', 'Mín', 'Estado']
    data = [headers]

    for p in productos:
        if p.stock_actual == 0:
            estado = 'AGOTADO'
        elif p.stock_actual <= p.stock_minimo:
            estado = 'BAJO'
        else:
            estado = 'OK'

        data.append([
            Paragraph(p.nombre or '', CELL_STYLE),
            p.codigo_barras or '—',
            p.categoria.nombre if p.categoria else '—',
            p.proveedor.nombre if p.proveedor else '—',
            f'${p.precio_compra:,.2f}' if p.precio_compra else '$0.00',
            f'${p.precio_venta:,.2f}' if p.precio_venta else '$0.00',
            str(p.stock_actual or 0),
            str(p.stock_minimo or 0),
            estado,
        ])

    col_widths = [140, 75, 80, 80, 60, 60, 40, 35, 52]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = _table_style()

    # Colorear estados
    for i, row in enumerate(data[1:], start=1):
        estado = row[-1]
        if estado == 'AGOTADO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), DANGER)
            style.add('FONTNAME', (-1, i), (-1, i), 'Helvetica-Bold')
        elif estado == 'BAJO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), WARNING)
            style.add('FONTNAME', (-1, i), (-1, i), 'Helvetica-Bold')
        else:
            style.add('TEXTCOLOR', (-1, i), (-1, i), SUCCESS)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer


def generar_stock_bajo():
    """Genera PDF de productos con stock bajo."""
    from models import ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30,
        bottomMargin=40,
        leftMargin=30,
        rightMargin=30,
    )

    productos = ProductoModel.query.filter(
        ProductoModel.stock_actual <= ProductoModel.stock_minimo,
        ProductoModel.activo == True,
    ).order_by(ProductoModel.stock_actual).all()

    elements = _build_header(
        "Reporte de Stock Bajo",
        f"{len(productos)} productos requieren atención",
    )

    agotados = sum(1 for p in productos if p.stock_actual == 0)
    criticos = sum(1 for p in productos if 0 < p.stock_actual <= (p.stock_minimo // 2))

    elements.append(_build_stat_row([
        ('Total Alertas', str(len(productos)), '#f97316'),
        ('Agotados', str(agotados), '#ef4444'),
        ('Críticos', str(criticos), '#eab308'),
    ]))
    elements.append(Spacer(1, 16))

    headers = ['Producto', 'Código', 'Proveedor', 'Contacto', 'Teléfono', 'Stock', 'Mín', 'Nivel']
    data = [headers]

    for p in productos:
        if p.stock_actual == 0:
            nivel = 'AGOTADO'
        elif p.stock_actual <= (p.stock_minimo // 2):
            nivel = 'CRÍTICO'
        else:
            nivel = 'BAJO'

        data.append([
            Paragraph(p.nombre or '', CELL_STYLE),
            p.codigo_barras or '—',
            p.proveedor.nombre if p.proveedor else '—',
            p.proveedor.contacto if p.proveedor else '—',
            p.proveedor.telefono if p.proveedor else '—',
            str(p.stock_actual or 0),
            str(p.stock_minimo or 0),
            nivel,
        ])

    col_widths = [140, 80, 100, 90, 80, 45, 40, 60]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = _table_style()

    for i, row in enumerate(data[1:], start=1):
        nivel = row[-1]
        if nivel == 'AGOTADO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), DANGER)
            style.add('FONTNAME', (-1, i), (-1, i), 'Helvetica-Bold')
        elif nivel == 'CRÍTICO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), ORANGE)
            style.add('FONTNAME', (-1, i), (-1, i), 'Helvetica-Bold')
        else:
            style.add('TEXTCOLOR', (-1, i), (-1, i), WARNING)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer


def generar_reporte_categorias():
    """Genera PDF del reporte por categorías."""
    from models import CategoriaModel, ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=30,
        bottomMargin=40,
        leftMargin=30,
        rightMargin=30,
    )

    categorias = CategoriaModel.query.order_by(CategoriaModel.nombre).all()

    elements = _build_header(
        "Reporte por Categorías",
        f"{len(categorias)} categorías registradas",
    )

    for cat in categorias:
        productos = ProductoModel.query.filter_by(
            categoria_id=cat.id, activo=True
        ).order_by(ProductoModel.nombre).all()

        valor_cat = sum((p.precio_venta or 0) * (p.stock_actual or 0) for p in productos)

        elements.append(Paragraph(
            f'{cat.nombre}  <font size="8" color="#8888aa">({len(productos)} productos — ${valor_cat:,.2f})</font>',
            SECTION_STYLE,
        ))

        if cat.descripcion:
            elements.append(Paragraph(cat.descripcion, ParagraphStyle(
                'desc', fontSize=8, textColor=TEXT_MUTED, spaceAfter=8,
            )))

        if productos:
            headers = ['Producto', 'P. Venta', 'Stock', 'Estado']
            data = [headers]

            for p in productos:
                estado = 'BAJO' if p.stock_actual <= p.stock_minimo else 'OK'
                data.append([
                    Paragraph(p.nombre or '', CELL_STYLE),
                    f'${p.precio_venta:,.2f}' if p.precio_venta else '$0.00',
                    str(p.stock_actual or 0),
                    estado,
                ])

            col_widths = [240, 80, 60, 60]
            table = Table(data, colWidths=col_widths, repeatRows=1)
            style = _table_style()

            for i, row in enumerate(data[1:], start=1):
                if row[-1] == 'BAJO':
                    style.add('TEXTCOLOR', (-1, i), (-1, i), WARNING)
                else:
                    style.add('TEXTCOLOR', (-1, i), (-1, i), SUCCESS)

            table.setStyle(style)
            elements.append(table)
        else:
            elements.append(Paragraph(
                '<i>Sin productos en esta categoría</i>',
                ParagraphStyle('empty', fontSize=8, textColor=TEXT_MUTED, spaceAfter=8),
            ))

        elements.append(Spacer(1, 12))

    # Productos sin categoría
    sin_cat = ProductoModel.query.filter_by(
        categoria_id=None, activo=True
    ).order_by(ProductoModel.nombre).all()

    if sin_cat:
        elements.append(Paragraph(
            f'Sin Categoría  <font size="8" color="#8888aa">({len(sin_cat)} productos)</font>',
            SECTION_STYLE,
        ))
        headers = ['Producto', 'P. Venta', 'Stock', 'Estado']
        data = [headers]
        for p in sin_cat:
            estado = 'BAJO' if p.stock_actual <= p.stock_minimo else 'OK'
            data.append([
                Paragraph(p.nombre or '', CELL_STYLE),
                f'${p.precio_venta:,.2f}' if p.precio_venta else '$0.00',
                str(p.stock_actual or 0),
                estado,
            ])
        table = Table(data, colWidths=[240, 80, 60, 60], repeatRows=1)
        table.setStyle(_table_style())
        elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer


def generar_reporte_proveedores():
    """Genera PDF del reporte de proveedores."""
    from models import ProveedorModel, ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30,
        bottomMargin=40,
        leftMargin=30,
        rightMargin=30,
    )

    proveedores = ProveedorModel.query.order_by(ProveedorModel.nombre).all()
    activos = sum(1 for p in proveedores if p.activo)

    elements = _build_header(
        "Reporte de Proveedores",
        f"{len(proveedores)} proveedores ({activos} activos)",
    )

    # Tabla principal
    headers = ['Proveedor', 'Contacto', 'Teléfono', 'Email', 'Productos', 'Valor Total', 'Estado']
    data = [headers]

    for prov in proveedores:
        productos = ProductoModel.query.filter_by(
            proveedor_id=prov.id, activo=True
        ).all()
        valor = sum((p.precio_venta or 0) * (p.stock_actual or 0) for p in productos)

        data.append([
            Paragraph(prov.nombre or '', CELL_STYLE),
            prov.contacto or '—',
            prov.telefono or '—',
            Paragraph(prov.email or '—', CELL_STYLE),
            str(len(productos)),
            f'${valor:,.2f}',
            'Activo' if prov.activo else 'Inactivo',
        ])

    col_widths = [130, 90, 80, 130, 55, 80, 60]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    style = _table_style()

    for i, row in enumerate(data[1:], start=1):
        if row[-1] == 'Inactivo':
            style.add('TEXTCOLOR', (-1, i), (-1, i), DANGER)
        else:
            style.add('TEXTCOLOR', (-1, i), (-1, i), SUCCESS)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer
