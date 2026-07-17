from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


# ==========================================================
# PAGE DECORATION
# ==========================================================

def add_page_number(canvas, doc):

    page = canvas.getPageNumber()

    canvas.saveState()

    width, height = doc.pagesize

    # ------------------------------------------------------
    # Border
    # ------------------------------------------------------

    canvas.setStrokeColor(colors.HexColor("#B57EDC"))
    canvas.setLineWidth(1)

    canvas.rect(
        18,
        18,
        width - 36,
        height - 36
    )

    # ------------------------------------------------------
    # Footer Separator
    # ------------------------------------------------------

    canvas.setStrokeColor(colors.HexColor("#D8C3F0"))
    canvas.setLineWidth(0.8)

    canvas.line(
        35,
        42,
        width - 35,
        42
    )

    # ------------------------------------------------------
    # Footer Text
    # ------------------------------------------------------

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5D3A87"))

    canvas.drawString(
        35,
        26,
        "CPU Scheduling Simulator  •  Automatically Generated Scheduling Analysis Report"
    )

    # ------------------------------------------------------
    # Page Number
    # ------------------------------------------------------

    canvas.setFont("Helvetica-Bold", 9)

    canvas.drawRightString(
        width - 35,
        26,
        f"Page {page}"
    )

    canvas.restoreState()


# ==========================================================
# EXPORT REPORT
# ==========================================================

def export_results(filename, algorithm, processes, metrics,graph_paths=None):

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.fontSize = 24
    title_style.leading = 28
    title_style.textColor = colors.white

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#5D3A87")
    heading_style.spaceBefore = 8
    heading_style.spaceAfter = 8

    doc = SimpleDocTemplate(
        filename,
        leftMargin=35,
        rightMargin=35,
        topMargin=35,
        bottomMargin=60
    )

    elements = []
    # ==========================================================
    # REPORT HEADER
    # ==========================================================

    banner = Table(
        [[
            Paragraph(
                """
                <para align='center'>
                <font color='white' size='24'><b>CPU Scheduling Simulator</b></font>
                <br/>
                <font color='white' size='13'>
                Professional Execution Report
                </font>
                </para>
                """,
                title_style
            )
        ]],
        colWidths=[520],
        hAlign="CENTER"
    )

    banner.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#5D3A87")),

        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#A96FD4")),

        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),

    ]))

    elements.append(banner)

    elements.append(Spacer(1, 0.28 * inch))


    # ==========================================================
    # EXECUTION SUMMARY
    # ==========================================================

    summary_heading = Table(
        [["Execution Summary"]],
        colWidths=[520],
        hAlign="CENTER"
    )

    summary_heading.setStyle(TableStyle([

        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#5D3A87")),

        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 13),

        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

    ]))

    elements.append(summary_heading)

    elements.append(Spacer(1, 0.10 * inch))


    summary = Table(

        [

            ["Algorithm", algorithm],

            ["Generated On",
             datetime.now().strftime("%d %B %Y   %I:%M %p")],

            ["Total Processes",
             str(len(processes))],

            ["Execution Status",
             "Completed Successfully"]

        ],

        colWidths=[180, 340],

        hAlign="CENTER"

    )


    summary.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#5D3A87")),
        ("TEXTCOLOR", (0,0), (0,-1), colors.white),

        ("BACKGROUND", (1,0), (1,-1), colors.HexColor("#FBF8FE")),

        ("GRID", (0,0), (-1,-1), 0.7, colors.HexColor("#C9A3E8")),

        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),

        ("FONTSIZE", (0,0), (-1,-1), 10.5),

        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

    ]))

    elements.append(summary)

    elements.append(Spacer(1, 0.30 * inch))
    
    # ==========================================================
    # PROCESS EXECUTION DETAILS
    # ==========================================================

    process_heading = Table(
        [["Process Execution Details"]],
        colWidths=[520],
        hAlign="CENTER"
    )

    process_heading.setStyle(TableStyle([
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#5D3A87")),

        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 13),

        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("ALIGN", (0,0), (-1,-1), "CENTER")

    ]))

    elements.append(process_heading)

    elements.append(Spacer(1, 0.12 * inch))


    # ----------------------------------------------------------
    # Process Data
    # ----------------------------------------------------------

    process_data = [[

        "PID",
        "AT",
        "BT",
        "Priority",
        "CT",
        "TAT",
        "WT",
        "RT"

    ]]

    for p in processes:

        process_data.append([

            p.pid,
            p.arrival_time,
            p.burst_time,
            p.priority,
            p.completion_time,
            p.turnaround_time,
            p.waiting_time,
            p.response_time

        ])


    process_table = Table(

        process_data,

        repeatRows=1,

        hAlign="CENTER",

        colWidths=[60, 48, 48, 68, 58, 62, 58, 58]

    )


    process_table.setStyle(TableStyle([

        # Header
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#5D3A87")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10.5),

        # Body
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 10),

        # Alignment
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("ALIGN", (0,1), (0,-1), "LEFT"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),

        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

        # Zebra Rows
        ("ROWBACKGROUNDS",
            (0,1),
            (-1,-1),
            [
                colors.HexColor("#FCFAFE"),
                colors.HexColor("#F3ECFA")
            ]
        ),

        # Grid
        ("GRID",
            (0,0),
            (-1,-1),
            0.55,
            colors.HexColor("#C8A5E5")
        ),

        # Padding
        ("TOPPADDING",
            (0,0),
            (-1,-1),
            9
        ),

        ("BOTTOMPADDING",
            (0,0),
            (-1,-1),
            9
        ),

        ("LEFTPADDING",
            (0,0),
            (-1,-1),
            7
        ),

        ("RIGHTPADDING",
            (0,0),
            (-1,-1),
            7
        ),

    ]))

    elements.append(process_table)

    elements.append(Spacer(1, 0.30 * inch))
    
    # ==========================================================
    # PERFORMANCE METRICS
    # ==========================================================

    metric_heading = Table(
        [["Performance Metrics"]],
        colWidths=[520],
        hAlign="CENTER"
    )

    metric_heading.setStyle(TableStyle([
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#5D3A87")),

        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 13),

        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("ALIGN", (0,0), (-1,-1), "CENTER")

    ]))

    elements.append(metric_heading)

    elements.append(Spacer(1, 0.12 * inch))


    metric_data = []

    for key, value in metrics.items():

        metric_data.append([key, str(value)])


    metric_table = Table(
        metric_data,
        colWidths=[280, 180],
        hAlign="CENTER"
    )

    metric_table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F0E5FA")),
        ("BACKGROUND", (1,0), (1,-1), colors.white),

        ("GRID", (0,0), (-1,-1), 0.6, colors.HexColor("#C8A5E5")),

        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),

        ("FONTSIZE", (0,0), (-1,-1), 10.5),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),

        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),

    ]))

    elements.append(metric_table)

    elements.append(Spacer(1, 0.25 * inch))
    
    # ==========================================================
    # PERFORMANCE GRAPH
    # ==========================================================

    if graph_paths:

        graph_heading = Table(
            [["Performance Analytics Graphs"]],
            colWidths=[520],
            hAlign="CENTER"
        )

        graph_heading.setStyle(TableStyle([
            ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#5D3A87")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 13),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ]))


        elements.append(graph_heading)

        elements.append(
            Spacer(1,0.15 * inch)
        )


        for graph_path in graph_paths:

            graph = Image(
                graph_path,
                width=5.5 * inch,
                height=3.2 * inch
            )

            elements.append(graph)

            elements.append(
                Spacer(1,0.25 * inch)
            )
    # ==========================================================
    # REPORT END
    # ==========================================================

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#D8C3F0")
        )
    )

    elements.append(Spacer(1, 0.12 * inch))

    end_note = Paragraph(
        """
        <para align='center'>
        <font size='9' color='#6A4C93'>
        End of Report
        </font>
        </para>
        """,
        styles["BodyText"]
    )

    elements.append(end_note)

    doc.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )
    
    