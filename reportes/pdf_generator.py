"""
Generador de reportes PDF con ReportLab.
Tema claro profesional con acentos en indigo/violeta.
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# ── Paleta: tema claro profesional ──
PRIMARY      = colors.HexColor('#6366f1')   # indigo
PRIMARY_DARK = colors.HexColor('#4f46e5')
ACCENT       = colors.HexColor('#8b5cf6')   # violeta
PAGE_BG      = colors.HexColor('#f5f5f7')   # gris muy claro
SURFACE      = colors.HexColor('#ffffff')   # blanco
SURFACE_ALT  = colors.HexColor('#f0f0f3')   # gris alternado
BORDER       = colors.HexColor('#e2e2e7')
TEXT_DARK    = colors.HexColor('#111118')   # casi negro
TEXT_BODY    = colors.HexColor('#3f3f46')
TEXT_MUTED   = colors.HexColor('#71717a')
SUCCESS      = colors.HexColor('#16a34a')
WARNING      = colors.HexColor('#d97706')
DANGER       = colors.HexColor('#dc2626')
ORANGE       = colors.HexColor('#ea580c')

# ── Estilos de texto ──
styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    'ReportTitle',
    parent=styles['Title'],
    fontSize=20,
    textColor=TEXT_DARK,
    spaceAfter=2,
    fontName='Helvetica-Bold',
)

SUBTITLE_STYLE = ParagraphStyle(
    'ReportSubtitle',
    parent=styles['Normal'],
    fontSize=9,
    textColor=TEXT_MUTED,
    spaceAfter=14,
)

SECTION_STYLE = ParagraphStyle(
    'SectionTitle',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=PRIMARY_DARK,
    spaceBefore=14,
    spaceAfter=6,
    fontName='Helvetica-Bold',
)

CELL_STYLE = ParagraphStyle(
    'CellStyle',
    parent=styles['Normal'],
    fontSize=8,
    textColor=TEXT_BODY,
    leading=10,
)

CELL_MUTED = ParagraphStyle(
    'CellMuted',
    parent=styles['Normal'],
    fontSize=8,
    textColor=TEXT_MUTED,
    leading=10,
)


def _build_header(title, subtitle=None):
    """Encabezado de reporte."""
    fecha = datetime.now().strftime('%d/%m/%Y  %H:%M')
    return [
        Paragraph(f"StockPro  —  {title}", TITLE_STYLE),
        Paragraph(
            f"Generado: {fecha}" + (f"   |   {subtitle}" if subtitle else ""),
            SUBTITLE_STYLE,
        ),
        HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12),
    ]


def _build_stat_row(stats: list):
    """Fila de tarjetas de estadisticas."""
    data = [[]]
    for label, value, hex_color in stats:
        cell = Paragraph(
            f'<font size="17" color="{hex_color}"><b>{value}</b></font><br/>'
            f'<font size="7" color="#71717a">{label}</font>',
            ParagraphStyle('stat', alignment=TA_CENTER, leading=20),
        )
        data[0].append(cell)

    col_width = 130
    table = Table(data, colWidths=[col_width] * len(stats))
    table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), SURFACE),
        ('BOX',           (0, 0), (-1, -1), 0.8, PRIMARY),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table


def _table_style():
    """Estilo base para tablas de datos."""
    return TableStyle([
        # Header
        ('BACKGROUND',    (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        # Body
        ('BACKGROUND',    (0, 1), (-1, -1), SURFACE),
        ('TEXTCOLOR',     (0, 1), (-1, -1), TEXT_BODY),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING',    (0, 1), (-1, -1), 6),
        # Grid
        ('GRID',          (0, 0), (-1, -1), 0.5, BORDER),
        ('ALIGN',         (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [SURFACE, SURFACE_ALT]),
    ])


def _page_background(canvas, doc):
    """Fondo de pagina y pie de pagina."""
    width, height = doc.pagesize
    canvas.saveState()
    # Fondo blanco
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, width, height, fill=True, stroke=False)
    # Franja de pie de pagina
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, 0, width, 28, fill=True, stroke=False)
    # Texto pie de pagina
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(40, 9, f"StockPro  —  Sistema de Inventario   |   Pagina {doc.page}")
    canvas.drawRightString(width - 40, 9, datetime.now().strftime('%d/%m/%Y %H:%M'))
    canvas.restoreState()


# ─────────────────────────────────────────
#  Reportes
# ─────────────────────────────────────────

def generar_inventario_completo():
    """PDF del inventario completo."""
    from models import ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30, bottomMargin=50, leftMargin=30, rightMargin=30,
    )

    productos = ProductoModel.query.filter_by(activo=True).order_by(ProductoModel.nombre).all()

    elements = _build_header("Inventario Completo", f"{len(productos)} productos activos")

    total = len(productos)
    bajo_stock = sum(1 for p in productos if p.stock_actual <= p.stock_minimo)
    valor_total = sum((p.precio_venta or 0) * (p.stock_actual or 0) for p in productos)

    elements.append(_build_stat_row([
        ('Total Productos',   str(total),            '#6366f1'),
        ('Stock Bajo',        str(bajo_stock),        '#dc2626'),
        ('Valor Inventario',  f'${valor_total:,.2f}', '#16a34a'),
    ]))
    elements.append(Spacer(1, 14))

    headers = ['Producto', 'Codigo', 'Categoria', 'Proveedor', 'P. Compra', 'P. Venta', 'Stock', 'Min', 'Estado']
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

    for i, row in enumerate(data[1:], start=1):
        estado = row[-1]
        if estado == 'AGOTADO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), DANGER)
            style.add('FONTNAME',  (-1, i), (-1, i), 'Helvetica-Bold')
        elif estado == 'BAJO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), WARNING)
            style.add('FONTNAME',  (-1, i), (-1, i), 'Helvetica-Bold')
        else:
            style.add('TEXTCOLOR', (-1, i), (-1, i), SUCCESS)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer


def generar_stock_bajo():
    """PDF de productos con stock bajo."""
    from models import ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30, bottomMargin=50, leftMargin=30, rightMargin=30,
    )

    productos = ProductoModel.query.filter(
        ProductoModel.stock_actual <= ProductoModel.stock_minimo,
        ProductoModel.activo == True,
    ).order_by(ProductoModel.stock_actual).all()

    elements = _build_header("Reporte de Stock Bajo", f"{len(productos)} productos requieren atencion")

    agotados = sum(1 for p in productos if p.stock_actual == 0)
    criticos  = sum(1 for p in productos if 0 < p.stock_actual <= (p.stock_minimo // 2))

    elements.append(_build_stat_row([
        ('Total Alertas', str(len(productos)), '#ea580c'),
        ('Agotados',      str(agotados),       '#dc2626'),
        ('Criticos',      str(criticos),        '#d97706'),
    ]))
    elements.append(Spacer(1, 14))

    headers = ['Producto', 'Codigo', 'Proveedor', 'Contacto', 'Telefono', 'Stock', 'Min', 'Nivel']
    data = [headers]

    for p in productos:
        if p.stock_actual == 0:
            nivel = 'AGOTADO'
        elif p.stock_actual <= (p.stock_minimo // 2):
            nivel = 'CRITICO'
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
            style.add('FONTNAME',  (-1, i), (-1, i), 'Helvetica-Bold')
        elif nivel == 'CRITICO':
            style.add('TEXTCOLOR', (-1, i), (-1, i), ORANGE)
            style.add('FONTNAME',  (-1, i), (-1, i), 'Helvetica-Bold')
        else:
            style.add('TEXTCOLOR', (-1, i), (-1, i), WARNING)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=_page_background, onLaterPages=_page_background)
    buffer.seek(0)
    return buffer


def generar_reporte_categorias():
    """PDF del reporte por categorias."""
    from models import CategoriaModel, ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=30, bottomMargin=50, leftMargin=30, rightMargin=30,
    )

    categorias = CategoriaModel.query.order_by(CategoriaModel.nombre).all()

    elements = _build_header("Reporte por Categorias", f"{len(categorias)} categorias registradas")

    for cat in categorias:
        productos = ProductoModel.query.filter_by(
            categoria_id=cat.id, activo=True
        ).order_by(ProductoModel.nombre).all()

        valor_cat = sum((p.precio_venta or 0) * (p.stock_actual or 0) for p in productos)

        elements.append(Paragraph(
            f'{cat.nombre}   '
            f'<font size="8" color="#71717a">({len(productos)} productos  —  ${valor_cat:,.2f})</font>',
            SECTION_STYLE,
        ))

        if cat.descripcion:
            elements.append(Paragraph(
                cat.descripcion,
                ParagraphStyle('desc', fontSize=8, textColor=TEXT_MUTED, spaceAfter=6),
            ))

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
                'Sin productos en esta categoria.',
                ParagraphStyle('empty', fontSize=8, textColor=TEXT_MUTED, spaceAfter=6),
            ))

        elements.append(Spacer(1, 10))

    # Productos sin categoria
    sin_cat = ProductoModel.query.filter_by(categoria_id=None, activo=True).order_by(ProductoModel.nombre).all()
    if sin_cat:
        elements.append(Paragraph(
            f'Sin Categoria   <font size="8" color="#71717a">({len(sin_cat)} productos)</font>',
            SECTION_STYLE,
        ))
        data = [['Producto', 'P. Venta', 'Stock', 'Estado']]
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
    """PDF del reporte de proveedores."""
    from models import ProveedorModel, ProductoModel

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=30, bottomMargin=50, leftMargin=30, rightMargin=30,
    )

    proveedores = ProveedorModel.query.order_by(ProveedorModel.nombre).all()
    activos = sum(1 for p in proveedores if p.activo)

    elements = _build_header("Reporte de Proveedores", f"{len(proveedores)} proveedores ({activos} activos)")

    headers = ['Proveedor', 'Contacto', 'Telefono', 'Email', 'Productos', 'Valor Total', 'Estado']
    data = [headers]

    for prov in proveedores:
        productos = ProductoModel.query.filter_by(proveedor_id=prov.id, activo=True).all()
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
