from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


OUT = Path("Assessment/MSE806_Assessment1_Report_Template_Final.docx")


def run(text, bold=False, italic=False, size=None):
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if size:
        rpr.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    props = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
    return f'<w:r>{props}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def paragraph(text="", style=None, align=None, before=None, after=None, keep=False):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if before is not None or after is not None:
        attrs = []
        if before is not None:
            attrs.append(f'w:before="{before}"')
        if after is not None:
            attrs.append(f'w:after="{after}"')
        ppr.append(f"<w:spacing {' '.join(attrs)}/>")
    if keep:
        ppr.append("<w:keepNext/>")
    props = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{props}{run(text)}</w:p>"


def blank(count=1):
    return "".join(paragraph() for _ in range(count))


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def bullet(text):
    return (
        '<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
        f'{run(text)}</w:p>'
    )


def rich_paragraph(fragments, style=None, align=None, before=None, after=None):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if before is not None or after is not None:
        attrs = []
        if before is not None:
            attrs.append(f'w:before="{before}"')
        if after is not None:
            attrs.append(f'w:after="{after}"')
        ppr.append(f"<w:spacing {' '.join(attrs)}/>")
    props = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    runs = "".join(run(text, bold=bold, italic=italic) for text, bold, italic in fragments)
    return f"<w:p>{props}{runs}</w:p>"


def table_cell(text, width, header=False, shade=None, align="center", size=20):
    fill = shade or ("1F4E78" if header else "FFFFFF")
    color = "FFFFFF" if header else "000000"
    return (
        '<w:tc>'
        f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:vAlign w:val="center"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
        '<w:tcMar><w:top w:w="100" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar></w:tcPr>'
        '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
        f'<w:jc w:val="{align}"/></w:pPr><w:r><w:rPr>'
        f'{"<w:b/>" if header else ""}<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        f'</w:rPr><w:t>{escape(text)}</w:t></w:r></w:p></w:tc>'
    )


def table_with_data(number, title, columns, widths, data_rows, note):
    rows = []
    rows.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(
        table_cell(col, width, header=True) for col, width in zip(columns, widths)
    ) + '</w:tr>')
    for row_index, values in enumerate(data_rows):
        shade = "EDF3F8" if row_index % 2 else "FFFFFF"
        rows.append('<w:tr>' + "".join(
            table_cell(value, width, shade=shade, align="left", size=18)
            for value, width in zip(values, widths)
        ) + '</w:tr>')
    borders = "".join(
        f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>'
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    table = (
        '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>'
        f'<w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="80" w:type="dxa"/>'
        '<w:left w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/>'
        '<w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
        + "".join(rows) + '</w:tbl>'
    )
    return (
        rich_paragraph([(f"Table {number}", True, False)], style="CaptionLabel", before=220, after=0)
        + rich_paragraph([(title, False, True)], style="CaptionTitle", after=100)
        + table
        + paragraph(note, style="FigureNote", before=80, after=200)
    )


def table_placeholder(number, title, columns, widths, sample_rows=3):
    rows = []
    rows.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(
        table_cell(col, width, header=True) for col, width in zip(columns, widths)
    ) + '</w:tr>')
    for row_index in range(sample_rows):
        shade = "EDF3F8" if row_index % 2 else "FFFFFF"
        rows.append('<w:tr>' + "".join(
            table_cell("[Add content]", width, shade=shade) for width in widths
        ) + '</w:tr>')
    borders = "".join(
        f'<w:{edge} w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>'
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    table = (
        '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>'
        f'<w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="80" w:type="dxa"/>'
        '<w:left w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/>'
        '<w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
        + "".join(rows) + '</w:tbl>'
    )
    return (
        rich_paragraph([(f"Table {number}", True, False)], style="CaptionLabel", before=220, after=0)
        + rich_paragraph([(title, False, True)], style="CaptionTitle", after=100)
        + table
        + paragraph("Note. Replace placeholder rows with analysed evidence and add the source where applicable.", style="FigureNote", before=80, after=200)
    )


def figure_placeholder(number, title, description):
    return (
        rich_paragraph([(f"Figure {number}", True, False)], style="CaptionLabel", before=220, after=0)
        + rich_paragraph([(title, False, True)], style="CaptionTitle", after=80)
        + paragraph(f"[Insert figure here: {description}]", style="FigurePlaceholder", align="center", before=240, after=240)
        + paragraph("Note. Add the data source, date, scope, filters and a concise explanation of what the figure demonstrates.", style="FigureNote", after=200)
    )


def toc_field():
    return (
        '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:i/><w:t>Open in Microsoft Word and update the table to refresh page numbers.</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p>'
    )


body = []

# Cover page
body.append(blank(2))
body.append(paragraph("Evaluating and Advancing Intelligent Transport Systems for Dublin Bus", style="Title", align="center", after=240))
body.append(paragraph("Architecture  Congestion Management  Traffic Signal Priority  and AI Enabled Operations", style="Subtitle", align="center", after=720))
body.append(paragraph("MSE806 Intelligent Transportation Systems", style="CoverInfo", align="center", after=80))
body.append(paragraph("Assessment 1  Case Study Based Research Assignment", style="CoverInfo", align="center", after=360))
body.append(paragraph("Student Name  [Insert name]", style="CoverInfo", align="center", after=80))
body.append(paragraph("Student ID  [Insert ID]", style="CoverInfo", align="center", after=80))
body.append(paragraph("Tutor  [Insert tutor name]", style="CoverInfo", align="center", after=80))
body.append(paragraph("Submission Date  [Insert date]", style="CoverInfo", align="center", after=80))
body.append(paragraph("Word Count  [Insert final word count]", style="CoverInfo", align="center"))
body.append(page_break())

# TOC page
body.append(paragraph("Table of Contents", style="TOCHeading", align="center", after=360))
body.append(toc_field())
body.append(page_break())

sections = [
    ("Executive Summary", [
        (0, "Purpose  evidence base  key findings  and three priority recommendations"),
    ]),
    ("1 Introduction to ITS and Dublin Bus", [
        (2, "1.1 Operational Context and Scale"),
        (2, "1.2 ITS and Cyber Physical System Framework"),
        (2, "1.3 Aim, Research Questions, Scope, and Methodology"),
    ]),
    ("2 Literature Review and Theoretical ITS Design", [
        (2, "2.1 Evolution from AVM to Data Driven AVLC"),
        (2, "2.2 Layered ITS Architecture and Communication Services"),
        (2, "2.3 Evidence on AVL  RTPI  TSP and Predictive Operations"),
        (2, "2.4 Standards and Interoperability"),
    ]),
    ("3 Dublin Bus ITS Architecture and Implementation", [
        (2, "3.1 Historical ITS Development"),
        (2, "3.2 On Bus Hardware and Integration Architecture"),
        (3, "3.2.1 ETM Gateway and RS485 Subsystem"),
        (3, "3.2.2 AVLC On Board Unit and Vehicle Telematics"),
        (2, "3.3 Communications, Control, and Data Exchange"),
        (3, "3.3.1 Tait Radio and Broadstone Control Centre"),
        (3, "3.3.2 SIRI, RTPI, DCC, NTA, and SCATS Interfaces"),
        (2, "3.4 Effectiveness and Architectural Limitations"),
    ]),
    ("4 Future Directions for the ITS Framework", [
        (2, "4.1 Standardised Data and Cloud Edge Architecture"),
        (2, "4.2 System Observability and Predictive Maintenance"),
        (2, "4.3 Prioritised Implementation and KPI Framework"),
    ]),
    ("5 Challenges, Benefits, Congestion, and Scheduled Service Evidence", [
        (2, "5.1 Pre- and Post-ITS Challenges, Incidents, and Benefits"),
        (2, "5.2 TFI GTFS Scheduled Service Analysis"),
        (3, "5.2.1 Spatial Network and Stop Coverage"),
        (3, "5.2.2 Hourly and Weekday Weekend Service Distribution"),
        (3, "5.2.3 Route Complexity and Corridor Profiles"),
        (2, "5.3 Operational, Data, Cyber, and Organisational Risk Mitigation"),
    ]),
    ("6 International Standards and Best Practice Comparison", [
        (2, "6.1 Comparison Method and Selected Cities"),
        (2, "6.2 GTFS  SIRI  NeTEx and Transmodel Comparison"),
        (2, "6.3 International Congestion and TSP Practices"),
        (2, "6.4 Dublin Bus Capability Gap and Transferable Lessons"),
    ]),
    ("7 Traffic Signal Priority", [
        (2, "7.1 Definition and Role in Congestion Management"),
        (2, "7.2 Twenty Second Polling and SCATS Limitations"),
        (2, "7.3 Vehicle to Infrastructure and Conditional TSP Design"),
        (2, "7.4 Impacts, KPIs, and Road User Safeguards"),
    ]),
    ("8 AI and Machine Learning Integration", [
        (2, "8.1 Travel Time and Delay Prediction"),
        (2, "8.2 Predictive Conditional TSP"),
        (2, "8.3 Incident Detection and Predictive Maintenance"),
        (2, "8.4 Five-Year Roadmap, Governance, and Risk Controls"),
    ]),
    ("9 Conclusion", [
        (0, "Direct answers to the research questions and prioritised final recommendations"),
    ]),
    ("References", [
    ]),
    ("Appendices", [
        (0, "Appendix A  GTFS Static Data Schema and Aggregation Method"),
        (0, "Appendix B  Data Quality Checks and Supporting Results"),
        (0, "Appendix C  Supplementary Risk and Comparison Evidence"),
    ]),
]

figures_after = {
    "2.2 Layered ITS Architecture and Communication Services": (
        1, "Layered ITS and Cyber Physical System Architecture",
        "sensing and vehicle  communication  data integration  application and control  governance and feedback layers",
    ),
    "3.1 Historical ITS Development": (
        2, "Dublin Bus ITS Development Timeline",
        "AVM  ETM  magnetic cards  destination displays  trunked radio  smart cards  AVLC  RTPI and integrated ticketing milestones",
    ),
    "3.3.2 SIRI, RTPI, DCC, NTA, and SCATS Interfaces": (
        3, "End to End Dublin Bus ITS and Communications Architecture",
        "ETM and RS485  AVLC OBU  GPS and odometer  radio  Broadstone Control Centre  RTPI  NTA  DCC and SCATS data flows",
    ),
    "5.2.1 Spatial Network and Stop Coverage": (
        4, "Dublin Bus Scheduled Route and Stop Network",
        "Power BI map showing scheduled routes  used stops and spatial network coverage for the selected service date",
    ),
    "5.2.2 Hourly and Weekday Weekend Service Distribution": (
        5, "Hourly Distribution of Scheduled Trips",
        "Power BI chart comparing scheduled weekday and weekend trips by hour",
    ),
    "5.2.3 Route Complexity and Corridor Profiles": (
        6, "Route Distance and Scheduled Journey Duration",
        "Power BI scatter plot of route distance  scheduled duration and service volume or stops",
    ),
    "7.3 Vehicle to Infrastructure and Conditional TSP Design": (
        7, "Conditional Traffic Signal Priority Decision Process",
        "vehicle detection  arrival prediction  lateness or headway test  safety constraints  priority request  controller response and outcome monitoring",
    ),
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": (
        8, "Five-Year ITS and AI Adoption Roadmap",
        "data governance  offline validation  shadow mode  corridor pilot  controlled integration and monitored scaling",
    ),
}

tables_after = {
    "3.4 Effectiveness and Architectural Limitations": (
        1, "Dublin Bus ITS Components and Evaluation",
        ["Component", "Function", "Reported benefit", "Limitation", "Evidence"],
        [1400, 1600, 1900, 1900, 2560], 4,
    ),
    "5.3 Operational, Data, Cyber, and Organisational Risk Mitigation": (
        2, "ITS Risk and Mitigation Matrix",
        ["Risk or incident", "Cause", "Impact", "Existing control", "Recommended mitigation", "Residual risk or KPI"],
        [1300, 1400, 1500, 1700, 1900, 1560], 5,
    ),
    "6.2 GTFS  SIRI  NeTEx and Transmodel Comparison": (
        3, "Public Transport Data Standards Comparison",
        ["Standard", "Primary purpose", "Data type", "Real time", "Strength", "Limitation", "Dublin relevance"],
        [1000, 1400, 1100, 1000, 1500, 1700, 1660], 4,
    ),
    "6.4 Dublin Bus Capability Gap and Transferable Lessons": (
        4, "International Best Practice Gap Analysis",
        ["Dimension", "Dublin Bus", "Comparator practice", "Capability gap", "Transferable lesson"],
        [1400, 1700, 2000, 1900, 2360], 4,
    ),
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": (
        5, "AI and Machine Learning Use Case Evaluation",
        ["Use case", "Required data", "Method", "Output", "Operational action", "KPI", "Risk and safeguard"],
        [1100, 1500, 1200, 1100, 1500, 1300, 1660], 4,
    ),
}

references = [
    [("Avcı, İ., & Koca, M. (2024). Intelligent transportation system technologies, challenges and security. ", False, False),
     ("Applied Sciences, 14", False, True), ("(11), 4646. https://doi.org/10.3390/app14114646", False, False)],
    [("Cordoș, N., Duma, I., Moldovanu, D., Todoruț, A., & Barabás, I. (2025). An overview of intelligent transportation systems in Europe. ", False, False),
     ("World Electric Vehicle Journal, 16", False, True), ("(7), 387. https://doi.org/10.3390/wevj16070387", False, False)],
    [("Fatorachian, H., & Kazemi, H. (2024). Integrating learning-based solutions in intelligent transportation systems: A conceptual framework and case studies validation. ", False, False),
     ("Cogent Engineering, 11", False, True), ("(1), 2427235. https://doi.org/10.1080/23311916.2024.2427235", False, False)],
    [("Smith, B. L., Hemily, B., & Ivanovic, M. (2005). ", False, False),
     ("Transit signal priority (TSP): A planning and implementation handbook", False, True),
     (". U.S. Department of Transportation, Federal Transit Administration.", False, False)],
    [("Khan, S. M., Rahman, M., Apon, A., & Chowdhury, M. (2025). Characteristics of intelligent transportation systems and its relationship with data analytics. In M. Chowdhury, A. Apon, & K. Dey (Eds.), ", False, False),
     ("Data analytics for intelligent transportation systems", False, True),
     (" (2nd ed., pp. 1-26). Elsevier. https://doi.org/10.1016/B978-0-443-13878-2.00009-6", False, False)],
    [("MobilityData. (n.d.). ", False, False), ("GTFS documentation", False, True),
     (". Retrieved September 23, 2026, from https://gtfs.org/documentation/", False, False)],
    [("Transmodel. (n.d.). ", False, False), ("Transmodel", False, True),
     (". Retrieved September 23, 2026, from https://www.transmodel-cen.eu/", False, False)],
    [("Transport for Ireland. (n.d.). ", False, False), ("Transport operator GTFS information", False, True),
     (". Retrieved September 23, 2026, from https://www.transportforireland.ie/transitData/PT_Data.html", False, False)],
    [("World Bank. (2011). ", False, False), ("Intelligent transport systems: Dublin, Ireland", False, True),
     (" [Case study].", False, False)],
]

section_content = {
    "1.1 Operational Context and Scale": [
        "An intelligent transport system (ITS) coordinates sensing, communications, data processing and operational control to improve the safety, reliability and efficiency of transport services. It is therefore more than a collection of devices. Its value depends on whether observations from vehicles and infrastructure can be converted into timely decisions and communicated to operators, drivers and passengers. Contemporary ITS are data-intensive systems in which data producers, communications networks, storage services and decision-support applications operate as an interconnected whole (Khan et al., 2025). For an urban bus operator, this design supports vehicle location, schedule adherence, disruption management, passenger information, fare collection and performance reporting.",
        "The Dublin Bus case provides a useful historical test of that systems perspective. During the case-study period, the operator ran approximately 980 double-deck buses and about 200,000 scheduled kilometres per day. Traffic variability, limited knowledge of vehicle location and reactive dispatching contributed to early departures, unreliable timekeeping and approximately 1,700 lost kilometres per day, mainly because of traffic delay (World Bank, 2011). These figures describe the implementation context around 2011; they are not presented as current operating statistics. The case is analytically valuable because it records how ticketing, radio, vehicle location, central control and passenger-information services were assembled over two decades rather than acquired as a single platform.",
    ],
    "1.2 ITS and Cyber Physical System Framework": [
        "Dublin Bus can be interpreted as a cyber-physical service system. GPS and odometer readings represent vehicle movement digitally; the electronic ticket machine (ETM), on-board computer and radio exchange identity and status data; central software compares observed movement with schedules; and dispatchers return operational instructions to drivers. The resulting feedback loop links physical service delivery to software-mediated supervision. A useful theoretical sequence is therefore sense, communicate, integrate, analyse, decide and measure. Breaking any link weakens the entire service: accurate location data have limited value if transmission is late, while rapid communication cannot compensate for inconsistent stop identifiers or an incorrect journey pattern.",
        "This layered interpretation also exposes cross-cutting requirements. Interoperability is needed because vehicle, control-centre and authority systems have different owners and replacement cycles. Availability and resilience matter because voice communication and operational visibility support staff safety as well as punctuality. Cybersecurity must protect connected devices, interfaces and control functions without preventing legitimate information exchange (Avcı & Koca, 2024). Consequently, Dublin Bus should be evaluated not only by the presence of AVL or RTPI technology, but by the latency, data quality, interface discipline and governance that allow those components to operate as one dependable service.",
    ],
    "1.3 Aim, Research Questions, Scope, and Methodology": [
        "This report evaluates how ITS design improved Dublin Bus software services and communications, where architectural and operational limitations remained, and how standards, traffic signal priority (TSP) and governed analytics could strengthen the system. Four questions guide the analysis: how did the implemented architecture support operational control and passenger information; what benefits and residual risks followed; how does the design compare with international standards and practice; and what future TSP and AI or machine-learning capabilities are justified by the available evidence?",
        "The method combines a focused literature review, qualitative analysis of the World Bank case, standards-based comparison and descriptive analysis of the Transport for Ireland static GTFS feed. Evidence is separated by time and function. The World Bank document is treated as a historical implementation baseline; recent academic and standards sources provide the contemporary theoretical benchmark; and GTFS describes scheduled network structure rather than observed performance. Static GTFS contains no actual arrivals, vehicle positions, speed, delay or TSP requests, so it cannot substantiate claims about current congestion or punctuality (MobilityData, n.d.; Transport for Ireland, n.d.). This boundary prevents planned service data from being misrepresented as operational evidence.",
    ],
    "2.1 Evolution from AVM to Data Driven AVLC": [
        "Automatic vehicle monitoring began as a control-centre application: locate the bus, compare it with the schedule and direct intervention towards exceptions. Dublin Bus implemented an odometer-based AVM across its fleet between 1977 and 1981. Vehicles were polled over a 45-second cycle, and depot dispatchers viewed actual and scheduled positions on route schematics. The system supported anticipatory regulation but was withdrawn in 1994 when it reached the end of its viable life (World Bank, 2011). The subsequent period illustrates that voice connectivity alone is not operational intelligence. Dispatchers could contact drivers, yet without trusted vehicle position they depended on verbal reports and generally reacted after disruption had formed.",
        "Modern AVLC extends this control logic through GPS, digital reference data, central applications and reusable event histories. Its theoretical advantage lies in converting location observations into several services at once: route regulation, estimated arrival information, schedule calibration and performance analysis. This transition also changes the bottleneck. When location data become abundant, value depends on velocity, veracity and integration rather than collection alone (Khan et al., 2025). Dublin Bus therefore moved from an equipment-centred AVM problem to a data-service problem in which stop inventories, journey patterns, sectional running times and consistent system identities were prerequisites for reliable software outputs.",
    ],
    "2.2 Layered ITS Architecture and Communication Services": [
        "A layered architecture clarifies these dependencies. The sensing and vehicle layer contains GPS, odometer, ticketing devices, door sensors and driver interfaces. Above it, radio, wireless LAN, fibre and IP services transport observations and commands. A data and integration layer aligns vehicle, route, trip, stop and schedule identities before application services use them for AVLC, dispatch, RTPI, journey planning or signal priority. Governance, safety and security cut across every layer because access control, supplier change, data provenance and failure recovery cannot be confined to one component. This interpretation is consistent with the layered and interconnected views of ITS described by Khan et al. (2025) and with European emphasis on interoperable hardware, software and real-time information flows (Cordoș et al., 2025).",
        "The architecture must also match the time sensitivity of each service. Depot software updates can tolerate batch transfer, passenger predictions require frequent and reliable observations, and a signal-priority request requires low-latency communication near a specific junction. Central control provides a network-wide view and consistent operating policy, but it introduces communication and platform dependencies. Local vehicle-to-infrastructure exchange can meet a time-critical need, while the central platform retains eligibility rules, monitoring and audit. The design issue is therefore not a choice between centralised and local control; it is the deliberate allocation of decisions according to latency, safety and evidence requirements.",
    ],
    "2.3 Evidence on AVL  RTPI  TSP and Predictive Operations": [
        "AVL evidence is strongest when operational visibility leads to a defined intervention. In the Dublin case, controllers could identify vehicles ahead of or behind schedule, track individual trips and regulate headways. The same observations supported RTPI and later analysis of sectional running times (World Bank, 2011). Passenger information, however, inherits upstream errors. Incorrect sign-on, stop coordinates, journey patterns or calibration can produce a plausible but wrong prediction. RTPI quality should therefore be assessed through coverage, prediction error, update latency and availability rather than the number of installed displays.",
        "TSP adds another control loop. It modifies signal timing through measures such as green extension or early green, normally subject to eligibility and safety constraints rather than the unconditional pre-emption used for emergency vehicles (Smith et al., 2005). Benefits depend on accurate arrival prediction, communication latency and safeguards for cross traffic and pedestrians. Predictive analytics may improve arrival estimates and identify emerging disruption, but learning-based systems require reliable real-time inputs, preprocessing, interpretability and scalable infrastructure (Fatorachian & Kazemi, 2024). The literature therefore supports progressive automation, not an immediate transfer of operational authority to opaque models. Baseline rules, shadow-mode testing and human oversight remain necessary.",
    ],
    "2.4 Standards and Interoperability": [
        "Public-transport standards separate conceptual consistency from exchange format. Transmodel provides a reference model and common terminology for entities such as routes, journey patterns, stops and timetables (Transmodel, n.d.). SIRI supports the exchange of real-time public-transport information, while GTFS primarily represents scheduled agencies, routes, trips, stops, times and shapes. GTFS-Realtime is a separate extension for trip updates, vehicle positions and alerts (MobilityData, n.d.). A folder labelled realtime but containing only static text tables does not become observed operational data.",
        "Standards reduce semantic ambiguity, but their presence does not guarantee interoperability. Stable identifiers, versioned interface contracts, time synchronisation, validation rules and accountable data ownership are also required. Dublin Bus used SIRI for the AVLC-to-RTPI feed and adopted parts of Transmodel terminology, yet the case reported no formal enterprise architecture or master interface structure (World Bank, 2011). This pragmatic approach enabled delivery, but case-by-case interfaces accumulate change risk. The theoretical lesson is to use standards as governed contracts between organisations, not merely as file formats selected within individual procurements.",
    ],
    "3.1 Historical ITS Development": [
        "Dublin Bus developed its ITS incrementally around operational needs. ETMs were introduced in 1989, followed by magnetic-card readers in 1990-1991, Autofare in 1995 and electronic destination displays in 1999. A Tait trunked-radio system arrived in 2001; replacement Wayfarer ETMs in 2005 increased memory, wireless transfer and integration capacity; and smart-card readers were added in 2008. The radio upgrade, AVLC deployment and central control-centre transition occurred across 2009-2010, followed by RTPI and integrated ticketing in 2011 (World Bank, 2011). This sequence shows architectural path dependence: early investment in a vehicle network and driver sign-on later supported services that had not been part of the original ticketing business case.",
    ],
    "3.2 On Bus Hardware and Integration Architecture": [
        "The vehicle architecture contained two coordinating nodes rather than one monolithic computer. The ETM retained responsibility for fare-related peripherals and operational identity, while the AVLC on-board computer coordinated location and telematics devices. Their RS485 and radio connections allowed information to cross subsystem boundaries without discarding established equipment (World Bank, 2011).",
    ],
    "3.2.1 ETM Gateway and RS485 Subsystem": [
        "The ETM-hosted RS485 network was the durable integration backbone. Magnetic and smart-card readers, fare equipment and destination-display functions received reference or initiation data from the ETM and returned transactions or status data. Driver sign-on supplied route, duty and identity information, while a permanent identifier in the ETM tray associated exchanged equipment with the correct vehicle. This reduced duplicate entry and enabled the destination display to update from route details entered at shift or trip start. The design was effective because it reused a stable operational gateway; its limitation was that integration depended on device-specific interfaces around a legacy bus rather than a formally governed vehicle data model.",
    ],
    "3.2.2 AVLC On Board Unit and Vehicle Telematics": [
        "The AVLC kit combined the bus radio, driver console, GPS unit, on-board computer and wireless LAN router. INIT supplied the GPS, computer and router in a 19-inch rack beneath the stairwell. Location combined odometer data as the primary measure with GPS as a supplement, and buses transmitted on a synchronised 20-second cycle. The AVLC computer linked to the ETM through RS485 and coordinated the odometer, GPS, AVL console, wireless router, passenger-information display and door switch; both focal computers connected directly to the radio (World Bank, 2011). The driver display showed an ahead-of-schedule condition but deliberately withheld lateness magnitude, limiting incentives to recover time through unsafe driving. This is a clear example of safety requirements shaping interface design.",
    ],
    "3.3 Communications, Control, and Data Exchange": [
        "On-board integration became operationally useful only when communications and control-centre software turned device data into coordinated action. Dublin Bus combined private radio, depot wireless LAN and fixed links with central AVLC services, while external passenger and traffic-management functions depended on interfaces to public authorities.",
    ],
    "3.3.1 Tait Radio and Broadstone Control Centre": [
        "The Tait trunked-radio system replaced open depot channels that suffered black spots, limited capacity and poor audio. Trunking provided private individual and group calls, dispatcher-controlled access and an emergency override. Because radios were assigned logically rather than fixed to a depot channel, vehicles could move between depots and routes. Their RS485 integration with the ETM also transferred sign-on, fleet, route and duty data without a separate radio keypad (World Bank, 2011).",
        "AVLC consolidated dispatching from eight depot control arrangements into a central control centre with 16 workstations arranged in five sector pods. Controllers received a network overview using colour-coded schedule-status categories and a route view showing buses against scheduled position. This shifted attention from locating vehicles to managing exceptions and headway. Centralisation strengthened shared situational awareness, but its success still depended on dispatcher training, safe layover locations and consistent driver procedures. Technology changed the information available; organisational preparation determined whether it produced proactive control.",
    ],
    "3.3.2 SIRI, RTPI, DCC, NTA, and SCATS Interfaces": [
        "Institutional boundaries shaped the data architecture. Dublin Bus generated AVLC observations, the National Transport Authority held responsibility for RTPI, and Dublin City Council hosted the RTPI server and managed at-stop displays. SIRI carried data from AVLC to the passenger-information environment, while scheduling and bus-stop databases supplied reference data. Each bus had a unique IP address, depots used wireless LAN, and AVLC communicated with the DCC RTPI system over a high-speed fibre link (World Bank, 2011). The arrangement enabled a multi-operator public platform, but the case initially relied on agreed specifications and working relationships rather than a formal service agreement.",
        "The SCATS interface exposed a more consequential limitation. DCC received AVLC data and used buses as probes to review travel times and rebalance signal settings, but it could not provide direct TSP. Twenty-second, one-way, slot-synchronised polling was too coarse for a bus approaching a junction, and the central system could not request an additional transmission. A trial near St James's Hospital therefore used a low-power, one-way vehicle-to-roadside message carrying vehicle, route and direction identifiers (World Bank, 2011). The distinction is important: feeding bus data into adaptive traffic management is not equivalent to operating a closed-loop priority service with eligibility logic, acknowledgement and outcome monitoring.",
    ],
    "3.4 Effectiveness and Architectural Limitations": [
        "The implementation produced credible operational benefits. The case reported improved reliability, virtual elimination of early departures from termini, better service-performance data, more appropriate sectional running times and evidence for traffic-management or bus-priority proposals. Controllers could see schedule deviation and intervene before disruption propagated, while the same data supported RTPI. These are material service improvements, yet causal strength is limited. The AVLC was still in its first full year, benefits had not been quantified, and no reduction in fleet requirement or measured productivity improvement had been attributed to it (World Bank, 2011). Reported success should therefore be treated as operational evidence, not a completed benefit-cost evaluation.",
        "Architecturally, incremental integration was both the principal strength and the residual risk. Reusing ETM, RS485 and radio assets lowered disruption and preserved organisational knowledge. Conversely, Dublin Bus had no formal overall system architecture or comprehensive data model; interfaces were specified case by case, detailed knowledge remained partly with suppliers, and external services required DCC, NTA and other organisations to coordinate. Data cleaning, equipment calibration, correct driver initiation and analytical skills were continuing concerns. Table 1 consequently evaluates each component against both its reported benefit and the constraint that a future architecture must address.",
    ],
    "4.1 Standardised Data and Cloud Edge Architecture": [
        "The next architectural step should formalise relationships that the historical system handled through project-specific interfaces. Dublin Bus needs an enterprise ITS model linking vehicle, operator, route, trip, stop, journey pattern, signal request and incident identifiers. Transmodel can supply the conceptual vocabulary, while SIRI and GTFS-family interfaces can serve defined exchange purposes (MobilityData, n.d.; Transmodel, n.d.). A versioned interface catalogue should record the owner, schema, latency target, validation rules and fallback for each data flow. This would reduce the risk that an ETM, AVLC, RTPI or ticketing change silently breaks another service.",
        "A hybrid cloud-edge design is preferable to centralising every decision. The governed platform should hold reference data, historical events, APIs and analytical services. On-board or roadside components should retain safety-critical and low-latency functions, including message validation and junction-level TSP exchange. This allocation preserves network-wide visibility without making a central round trip a prerequisite for every time-sensitive action. It also creates a controlled path from the legacy RS485 and radio environment towards IP-based services rather than requiring disruptive fleet-wide replacement.",
    ],
    "4.2 System Observability and Predictive Maintenance": [
        "Operational monitoring should cover the data service, not only whether hardware is powered. Relevant measures include vehicle-message age, missed polls, GPS-odometer disagreement, invalid sign-on, stop and trip identity failures, SIRI delivery latency, RTPI prediction error and roadside acknowledgement rate. These indicators would distinguish a communications fault from poor reference data or an incorrect driver process. The same telemetry can support condition-based maintenance by identifying repeated radio loss, sensor drift or on-board computer resets before a device fails in service.",
        "Observability also strengthens accountability across suppliers and agencies. Service-level objectives should define availability and latency at each interface, with traceable incident records and named owners. Security monitoring must accompany connectivity because vehicle, roadside and central interfaces enlarge the attack surface (Avcı & Koca, 2024). A safe design therefore combines access control, signed or authenticated messages, network segmentation, patch governance and tested degraded modes with the operational dashboard.",
    ],
    "4.3 Prioritised Implementation and KPI Framework": [
        "Implementation should proceed in dependency order. First, Dublin Bus, NTA and DCC should agree common identifiers, data ownership, interface contracts and baseline KPIs. Second, automated quality and latency monitoring should run against existing AVLC, SIRI and scheduling flows. Third, predictive ETA and disruption models can operate in shadow mode, where their outputs are compared with current practice but do not control service. A conditional TSP pilot should follow on a limited corridor only after vehicle-to-roadside messages and SCATS responses can be observed end to end. Wider deployment should depend on measured benefit and safe fallback.",
        "The evaluation set should connect technology to service outcomes: RTPI error, headway variation, early-departure rate, lost kilometres, message latency, equipment availability, TSP success rate and delay imposed on cross traffic or pedestrians. A before-and-after design with matched time periods is stronger than reporting system usage alone. This staged approach also constrains model and integration risk, consistent with evidence that learning-based ITS requires reliable data, preprocessing, interpretability and scalable infrastructure before operational use (Fatorachian & Kazemi, 2024).",
    ],
    "5.1 Pre- and Post-ITS Challenges, Incidents, and Benefits": [
        "Before the modern AVLC, Dublin Bus lacked a reliable network-wide view of vehicle position. Dispatchers depended on driver reports, roadside surveys and street supervisors, so intervention often began after lateness or bunching was visible. The case recorded approximately 1,700 lost kilometres per day, largely because of traffic delay, together with early departures, weak performance evidence and radio limitations affecting staff security (World Bank, 2011). AVLC, trunked radio and central control addressed several causal mechanisms: controllers could identify schedule deviation, regulate headways and support drivers through private and emergency communication.",
        "The post-implementation risk profile changed rather than disappeared. Operations now depended on accurate stop coordinates, journey patterns, sectional times, driver sign-on and equipment calibration. Deployment required approximately 1,000 vehicles and 2,500 drivers to adopt consistent procedures, while dispatcher effectiveness depended on PC skills and mentoring (World Bank, 2011). Integration also increased exposure to communications outages, supplier coordination and cyber threats. Reported benefits - including fewer early departures, improved scheduling evidence and RTPI support - should therefore be assessed beside residual data, organisational and cross-agency risks rather than treated as automatic consequences of installing AVL.",
    ],
    "5.2 TFI GTFS Scheduled Service Analysis": [
        "The Transport for Ireland feed was analysed as a planned-service dataset. Dublin Bus records were selected with agency_id = 1 and joined through routes, trips, stop_times, stops, calendar, calendar_dates and shapes. The feed version E220AAFE-A29E-4C78-896A-4507E0F5612A is valid from 6 August 2026 to 6 August 2027 and contains 114 Dublin Bus routes, 27,926 trip records, 4,335 used stops and 607 shapes (Transport for Ireland, n.d.). Service-date calculations below apply calendar exceptions and interpret GTFS times beyond 24:00 as post-midnight continuation of the operating day.",
    ],
    "5.2.1 Spatial Network and Stop Coverage": [
        "Figure 4 should map the 4,335 stops actually referenced by Dublin Bus trips together with their route shapes. This distinguishes operationally used stops from every stop in the multi-operator feed. The map can demonstrate geographic reach, corridor overlap and potential transfer concentrations, but not demand, accessibility quality or congestion. Those questions require passenger counts, observed vehicle movement or street-network evidence that static GTFS does not provide.",
    ],
    "5.2.2 Hourly and Weekday Weekend Service Distribution": [
        "On Wednesday 23 September 2026, 8,048 scheduled Dublin Bus trips operated across all 114 routes. Saturday 26 September contained 6,648 trips across 80 routes, 17.4% fewer trips than the selected weekday. Weekday departures peaked between 07:00 and 07:59 with 623 trips, whereas the Saturday maximum occurred between 16:00 and 16:59 with 408. Trips with times from 24:00 to 29:59 were retained as late-night service belonging to the original service day. Figure 5 should present the complete hourly distributions rather than only these peaks, since the flatter Saturday profile is operationally as important as the lower total.",
    ],
    "5.2.3 Route Complexity and Corridor Profiles": [
        "Scheduled geometry and stop sequences reveal substantial operating diversity. On the selected weekday, route E1 had 264 trips, a median scheduled duration of 111.6 minutes, a median of 87 stops and a longest shape of approximately 31.2 km. Route 41X operated only ten trips but included a shape of approximately 56.5 km. Figure 6 should therefore plot distance, duration and service volume together. A long route is not necessarily frequent, and scheduled duration is not actual travel time. The scatter plot can identify corridors for further investigation, but observed AVL is required before attributing long schedules to congestion.",
    ],
    "5.3 Operational, Data, Cyber, and Organisational Risk Mitigation": [
        "Risk controls should follow the full sensing-to-action chain. A missed poll can degrade RTPI; an incorrect trip identity can direct a valid observation to the wrong service; and a compromised interface can affect both information and control. Data validation, redundancy and degraded operating procedures are therefore as important as perimeter security. Table 2 separates the initiating condition, operational impact, existing control and measurable mitigation. Residual risk should be monitored through error, latency and recovery KPIs rather than closed after installation.",
    ],
    "6.1 Comparison Method and Selected Cities": [
        "The comparison uses common capabilities rather than ranking cities by technology count. Dublin Bus is assessed against European interoperability practice described by Cordoș et al. (2025) and the learning-based traffic-management cases from Singapore, Los Angeles and Rio de Janeiro reviewed by Fatorachian and Kazemi (2024). The dimensions are architecture, data standards, operational monitoring, adaptive control, institutional governance and evidence of benefit. This method limits false equivalence: a city-wide traffic platform and a bus AVLC have different scopes, but their approaches to data quality, integration and staged decision support remain transferable.",
    ],
    "6.2 GTFS  SIRI  NeTEx and Transmodel Comparison": [
        "Interoperability requires several complementary standards. Transmodel defines shared public-transport concepts; NeTEx exchanges detailed planned networks and timetables; SIRI supports real-time operational information; GTFS provides a widely adopted scheduled-service format; and GTFS-Realtime carries trip updates, vehicle positions and alerts (MobilityData, n.d.; Transmodel, n.d.). Table 3 shows why no single format should be labelled the complete architecture. Dublin's SIRI and GTFS use supports exchange, but consistent identifiers, governance and observable interface performance remain necessary.",
    ],
    "6.3 International Congestion and TSP Practices": [
        "International practice combines network observation with conditional intervention. European ITS programmes increasingly emphasise interoperable data flows between vehicles, infrastructure and management platforms (Cordoș et al., 2025). The TSP handbook similarly frames priority as a coordinated operational strategy, using measures such as green extension or early green while monitoring effects on other road users (Smith et al., 2005). Learning-based cases add prediction and adaptive signal control, but also expose requirements for data quality, interpretability and scalable processing (Fatorachian & Kazemi, 2024).",
        "Against this benchmark, the historical Dublin design had strong fleet visibility but an incomplete congestion-control loop. Twenty-second one-way AVLC updates could support retrospective travel-time analysis and SCATS retiming, not junction-level priority. A transferable design would combine low-latency vehicle-to-infrastructure messages with central eligibility rules based on lateness or headway, signal-controller acknowledgement and outcome logging. Priority must remain bounded by pedestrian clearance, cross-street delay and corridor coordination.",
    ],
    "6.4 Dublin Bus Capability Gap and Transferable Lessons": [
        "Dublin Bus's principal gap was not the absence of useful components; it was the lack of a formal architecture connecting them to measurable service outcomes. The ETM and RS485 network demonstrated effective reuse, AVLC created operational visibility, and SIRI enabled passenger-information exchange. Yet interfaces were governed case by case, TSP was not operational, and benefits were not quantified (World Bank, 2011). International evidence supports a sequence of formalising the data foundation, instrumenting service quality, piloting conditional control and then introducing prediction. Table 4 converts that comparison into capabilities Dublin Bus can adopt without assuming that another city's platform can be copied unchanged.",
    ],
    "7.1 Definition and Role in Congestion Management": [
        "Traffic signal priority adjusts normal signal operation to reduce delay for eligible public-transport vehicles. Typical treatments include green extension, early green, phase insertion and phase rotation. TSP differs from emergency pre-emption: it remains conditional and should preserve pedestrian clearance, junction safety and network coordination (Smith et al., 2005). For Dublin Bus, its purpose is not to remove congestion. It should reduce avoidable signal delay, limit delay propagation and improve headway or schedule reliability on selected corridors.",
        "Priority also depends on the operating objective. Giving every detected bus the same treatment may transfer excessive delay to cross traffic and provide little value to an early-running vehicle. Eligibility should therefore reflect lateness, headway imbalance, passenger impact where reliable loading data exist, junction state and recent priority activity. This links the signal decision to service regulation rather than vehicle presence alone.",
    ],
    "7.2 Twenty Second Polling and SCATS Limitations": [
        "The historical AVLC-to-DCC feed could not support junction-level TSP. Buses transmitted in synchronised slots every 20 seconds, the exchange was one way, and the central system could not request an additional update as a vehicle approached a signal. At urban speeds, a bus can travel a material distance between observations; processing and transfer delay add further uncertainty. DCC could use buses as probes for travel-time analysis and SCATS retiming, but this was not a closed priority loop (World Bank, 2011).",
        "The limitation is architectural rather than a flaw in SCATS itself. A functioning service needs timely detection, a validated request, controller response or rejection, and an outcome record. Without acknowledgement, Dublin Bus cannot distinguish a failed communication from a denied request, evaluate priority success or relate a treatment to bus and cross-street delay.",
    ],
    "7.3 Vehicle to Infrastructure and Conditional TSP Design": [
        "A target design should combine local vehicle-to-infrastructure communication with centrally governed rules. The on-board unit would transmit vehicle, route, direction, trip identity, estimated arrival and schedule or headway status to a roadside unit. The roadside service would validate the message, apply safety and cooldown constraints, and pass an eligible request to SCATS or the junction controller. The response would return through the roadside unit and be logged centrally with the signal phase, treatment and subsequent bus passage.",
        "Local exchange removes the 20-second central polling constraint, while the control platform retains consistent policy and audit. Green extension or early green should be the default treatments; stronger changes require corridor-specific modelling. If communications, identity validation or signal state is unavailable, the controller should revert to its normal plan. Figure 7 represents this request, constraint, response and measurement sequence.",
    ],
    "7.4 Impacts, KPIs, and Road User Safeguards": [
        "A corridor pilot should measure median and 95th-percentile bus travel time, headway variation, on-time performance, priority request success, request-to-controller latency and the proportion of late requests. Safeguards require parallel measures for cross-street delay, queue growth, pedestrian delay and emergency access. Results should be compared with matched periods or untreated junctions, not inferred from request counts. Limits on green extension, consecutive priority calls and recovery time protect general traffic, while an auditable rejection reason supports operational learning. TSP should scale only when reliability improves without breaching agreed safety and network-impact thresholds.",
    ],
    "8.1 Travel Time and Delay Prediction": [
        "Predictive ETA and delay support should begin with a labelled operational dataset: historical AVL or actual arrival and departure events joined to scheduled GTFS, stop and route characteristics, time of day, weather, incidents and road conditions. The downloaded static GTFS cannot supply the target variable. A simple historical or schedule-based baseline should be compared with gradient-boosted trees before considering deeper models. Outputs should include predicted sectional travel time, ETA and uncertainty, allowing RTPI to display more stable information and dispatchers to identify emerging disruption.",
        "Validation must separate training and testing by time and preferably by route or disruption period to avoid leakage. Mean absolute error alone is insufficient; error by route, time band and disruption state is needed because an apparently accurate network average can conceal poor service on difficult corridors. Predictions should first operate in shadow mode, with dispatchers able to inspect inputs and override recommendations.",
    ],
    "8.2 Predictive Conditional TSP": [
        "Predictive TSP would estimate arrival at the stop line and the operational value of priority before submitting a request. Inputs include recent vehicle trajectory, lateness or headway, dwell-state information, signal phase and queue conditions. A constrained optimiser can select no priority, early green or a bounded extension. Reinforcement learning may be tested in simulation, but direct live control is premature because reward design can conceal pedestrian or cross-street costs and policies may fail when traffic patterns change (Fatorachian & Kazemi, 2024).",
        "The safe deployment sequence is offline replay, digital or microscopic simulation, shadow decisions, a supervised corridor pilot and controlled expansion. The controller must enforce hard safety constraints independently of the prediction model. Every request should retain its input version, decision, response and outcome so that performance and bias can be audited.",
    ],
    "8.3 Incident Detection and Predictive Maintenance": [
        "The same data platform can detect operational and equipment anomalies. Missed polls, implausible GPS-odometer divergence, repeated sign-on failures, excessive dwell, route deviation, door-sensor faults and on-board computer resets can be compared with route- and device-specific baselines. Initial rules are preferable where failure signatures are known; unsupervised anomaly detection can identify unfamiliar patterns but requires human review because rare service conditions may resemble faults.",
        "Alerts should identify the affected vehicle, evidence, severity and recommended check rather than provide an unexplained score. Useful KPIs include detection lead time, false-alert rate, mean time to repair, repeat failure rate and service kilometres affected. This supports maintenance prioritisation without allowing an opaque model to remove a vehicle from service automatically.",
    ],
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": [
        "Years one and two should establish common identifiers, data ownership, retention rules, quality monitoring and baseline KPIs, followed by offline ETA and anomaly models. Years two and three should introduce shadow-mode prediction and a low-latency conditional TSP pilot. Years three and four can expand proven corridors and integrate dispatcher workflows. Year five should focus on monitored scaling, model refresh and independent evaluation rather than adding algorithms by default.",
        "Governance applies across the roadmap. Connected ITS requires access control, authentication, segmentation, patch management and incident response (Avcı & Koca, 2024). Models add drift, bias, privacy and explainability risks. Named owners, versioned data and models, approval gates, override mechanisms and rollback plans are therefore deployment requirements. Table 5 ties each use case to required data, operational action, KPI and safeguard; Figure 8 should show that later phases depend on evidence from earlier ones.",
    ],
    "9 Conclusion": [
        "Dublin Bus demonstrates how incremental ITS investment can create a coherent operational capability. ETM-hosted RS485 integration, trunked radio, GPS and odometer-based AVLC, central dispatch and SIRI-enabled RTPI improved visibility, communication and service regulation. The reported reduction in early departures and improved scheduling evidence are credible, but the historical case did not quantify AVLC productivity benefits and documented no formal overall architecture or operational TSP (World Bank, 2011).",
        "The assessment also identifies a clear boundary in the current evidence. Static TFI GTFS describes a large and varied scheduled network, including 8,048 trips on the selected weekday and 6,648 on the selected Saturday, but cannot establish actual delay, speed, congestion or punctuality. Those outcomes require archived AVL or GTFS-Realtime observations and traffic data.",
        "The recommended sequence is consequently disciplined: formalise the data and interface architecture, make quality and latency observable, pilot acknowledged conditional TSP, and introduce predictive services through baseline comparison, shadow mode and controlled evaluation. Dublin Bus should scale each capability only when passenger benefit, operational reliability, cybersecurity and effects on other road users are measurable and acceptable.",
    ],
}

# Concise final-pass versions preserve evidence while keeping the report within its word budget.
section_content.update({
    "1.1 Operational Context and Scale": [
        "An intelligent transport system (ITS) links sensing, communications, data processing and operational control to improve safety, reliability and efficiency. For a bus operator, that chain supports vehicle location, schedule adherence, disruption management, passenger information, fare collection and performance reporting (Khan et al., 2025). During the 2011 case period, Dublin Bus operated about 980 buses and 200,000 scheduled kilometres per day; traffic delay, reactive dispatch and limited location visibility contributed to early departures and approximately 1,700 lost kilometres per day (World Bank, 2011). These are historical baseline figures, not current operating statistics.",
    ],
    "1.2 ITS and Cyber Physical System Framework": [
        "Dublin Bus can be treated as a cyber-physical service system. GPS and odometer readings represent vehicle movement; ETM, on-board computer and radio services exchange identity and status; central software compares observations with schedules; and dispatchers return instructions. The resulting loop is sense, communicate, integrate, analyse, decide and measure. Its quality depends on latency, data accuracy, interoperability, resilience and cybersecurity across vehicle, operator and authority boundaries (Avcı & Koca, 2024). AVL or RTPI technology alone is insufficient if an identifier is wrong, a message is late or responsibility for an interface is unclear.",
    ],
    "1.3 Aim, Research Questions, Scope, and Methodology": [
        "This report asks how ITS improved Dublin Bus services and communications, which benefits and risks remained, how the design compares with international practice, and how TSP and governed AI or machine learning could extend it. The method combines a focused literature review, qualitative case analysis, standards comparison and descriptive TFI GTFS analysis. The World Bank case is a historical implementation baseline; recent sources provide the contemporary benchmark; and static GTFS describes scheduled service only. It contains no actual arrivals, vehicle positions, speed, delay or TSP requests and therefore cannot substantiate current congestion or punctuality (MobilityData, n.d.; Transport for Ireland, n.d.).",
    ],
    "2.1 Evolution from AVM to Data Driven AVLC": [
        "Dublin Bus deployed an odometer-based AVM fleetwide between 1977 and 1981. Vehicles were polled over 45 seconds and depot screens compared actual with scheduled position, enabling anticipatory regulation. After withdrawal in 1994, radio contact remained but dispatch became reactive because controllers relied on driver reports (World Bank, 2011). Modern AVLC restores location visibility through GPS, odometer, digital reference data and reusable histories. The bottleneck then shifts from collection to the velocity, veracity and integration of data (Khan et al., 2025): accurate stops, journey patterns, sectional times and identities become prerequisites for dispatch, ETA and performance services.",
    ],
    "2.2 Layered ITS Architecture and Communication Services": [
        "A layered model separates sensing and vehicle devices; radio, wireless, fibre and IP communications; data and identity integration; and applications such as AVLC, RTPI, scheduling and TSP. Governance, safety and security cross every layer (Khan et al., 2025). The architecture must also reflect time sensitivity. Depot updates may be batch-based, passenger predictions require frequent observations, and a junction priority request requires low latency. Central control provides network context and audit, while local vehicle-to-infrastructure exchange can handle the time-critical signal interaction. The relevant design choice is where each decision belongs, not whether all control should be central or local.",
        "This division also supports graceful degradation. A loss of central analytics should not disable normal signal control or driver safety communication, while a failed roadside exchange should leave the scheduled service and central dispatch functions available. Architecture quality is therefore reflected in bounded failure, observable interfaces and recoverable state as well as nominal functionality.",
    ],
    "2.3 Evidence on AVL  RTPI  TSP and Predictive Operations": [
        "AVL creates value when visibility triggers a defined action. Dublin controllers could identify schedule deviation, track trips, regulate headways and reuse observations for RTPI and sectional running-time review (World Bank, 2011). RTPI nevertheless inherits upstream sign-on, mapping and calibration errors. TSP adds a stricter loop: green extension or early green should serve eligible buses while retaining safety and network constraints, rather than operate as emergency pre-emption (Smith et al., 2005). Prediction can improve ETA and disruption response, but reliable inputs, preprocessing, interpretability and scalable infrastructure are prerequisites (Fatorachian & Kazemi, 2024). Baselines, shadow testing and human oversight should precede automation.",
        "Reported benefits must also be matched to evidence quality. Operational observations can show that controllers gained visibility, but they do not isolate the effect of AVLC from training, timetable changes or bus-priority infrastructure. Strong evaluation requires explicit service KPIs, a baseline and, where possible, matched corridors or periods.",
    ],
    "2.4 Standards and Interoperability": [
        "Transmodel supplies common public-transport concepts; SIRI exchanges operational information; GTFS represents scheduled agencies, routes, trips, stops and times; and GTFS-Realtime separately carries trip updates, vehicle positions and alerts (MobilityData, n.d.; Transmodel, n.d.). Dublin Bus used SIRI for AVLC-to-RTPI transfer and parts of Transmodel terminology, but the case reported no formal enterprise architecture or master interface structure (World Bank, 2011). Standards therefore need stable identifiers, versioned contracts, validation, time synchronisation and accountable owners. A folder named realtime that contains only static GTFS tables is not observed operational data.",
        "Interoperability is consequently organisational as well as syntactic. Two systems can exchange valid messages yet disagree about a trip identity, effective date or responsibility for correction. Shared profiles, conformance testing and change control convert a standard into a dependable service contract.",
    ],
    "3.1 Historical ITS Development": [
        "Dublin Bus introduced ETMs in 1989, magnetic-card readers in 1990-1991, destination displays in 1999, trunked radio in 2001, replacement Wayfarer ETMs in 2005, smart-card readers in 2008, AVLC and central control during 2009-2010, and RTPI and integrated ticketing in 2011 (World Bank, 2011). The sequence shows path dependence: the early vehicle network and driver sign-on later supported services outside the original ticketing case.",
    ],
    "3.2 On Bus Hardware and Integration Architecture": [
        "The vehicle contained two coordinating nodes: the ETM managed fare peripherals and operational identity, while the AVLC computer managed location and telematics. RS485 and radio linked the subsystems without replacing established equipment (World Bank, 2011).",
    ],
    "3.2.1 ETM Gateway and RS485 Subsystem": [
        "The ETM-hosted RS485 network connected magnetic and smart-card readers, fare equipment and destination functions. Driver sign-on supplied route, duty and identity data, while an identifier in the ETM tray tied exchanged equipment to the vehicle. This reduced duplicate entry and automated destination updates. The reuse was efficient, but integration remained device-specific rather than governed by a common vehicle data model.",
    ],
    "3.2.2 AVLC On Board Unit and Vehicle Telematics": [
        "The AVLC kit combined radio, driver console, GPS, on-board computer and wireless LAN router; INIT housed the GPS, computer and router in a 19-inch rack beneath the stairwell. Odometer data provided primary location with GPS supplementation, and buses transmitted in synchronised 20-second slots. The computer linked through RS485 and coordinated location, passenger-display and door-sensor functions (World Bank, 2011). The console showed early running but withheld lateness magnitude to discourage unsafe recovery driving.",
    ],
    "3.3 Communications, Control, and Data Exchange": [
        "Radio, depot wireless LAN and fixed links turned on-board observations into control-centre and external information services.",
    ],
    "3.3.1 Tait Radio and Broadstone Control Centre": [
        "Tait trunked radio replaced open depot channels with private calls, dispatcher control, group communication and emergency override. ETM integration transferred sign-on, route and duty data without another keypad. AVLC then consolidated dispatching into 16 workstations across five sector pods. Colour-coded network and route views shifted attention from locating vehicles to managing schedule and headway exceptions. Training, safe holding locations and driver procedures remained necessary; better information did not by itself produce proactive control (World Bank, 2011).",
    ],
    "3.3.2 SIRI, RTPI, DCC, NTA, and SCATS Interfaces": [
        "Dublin Bus generated AVLC observations, NTA held RTPI responsibility, and DCC hosted the server and at-stop displays. SIRI transferred information over a high-speed link, with scheduling and stop databases supplying reference data. The arrangement supported a multi-operator platform but initially relied on specifications and working relationships rather than a formal service agreement. DCC also received AVLC data as SCATS probes, yet 20-second one-way polling was too coarse for direct TSP and could not request an extra approach update. A roadside trial near St James's Hospital instead used a low-power vehicle message carrying vehicle, route and direction identifiers (World Bank, 2011).",
    ],
    "3.4 Effectiveness and Architectural Limitations": [
        "The case reported improved reliability, virtual elimination of early terminal departures, better running-time evidence and support for RTPI and traffic-management proposals. However, AVLC was in its first full year, benefits were not quantified, and no fleet or productivity reduction had been attributed to it (World Bank, 2011). Incremental reuse of ETM, RS485 and radio assets reduced disruption, but no formal overall architecture or comprehensive data model existed; interfaces were specified case by case and depended on suppliers and cross-agency coordination. Table 1 therefore treats effectiveness and architectural debt together.",
    ],
    "4.1 Standardised Data and Cloud Edge Architecture": [
        "Dublin Bus should formalise vehicle, route, trip, stop, journey-pattern, incident and signal-request identities in an enterprise ITS model. Transmodel can supply common concepts, while SIRI and GTFS-family interfaces retain defined exchange roles (MobilityData, n.d.; Transmodel, n.d.). Each versioned interface needs an owner, schema, latency target, validation rule and fallback. A hybrid design should keep governed reference, history and analytics centrally, while on-board or roadside components validate and exchange time-critical TSP messages. This provides a controlled migration from RS485 and private radio without requiring immediate fleet replacement.",
    ],
    "4.2 System Observability and Predictive Maintenance": [
        "Monitoring should distinguish hardware, communications, reference-data and process faults. Measures include message age, missed polls, GPS-odometer disagreement, invalid sign-on, identity failures, SIRI latency, RTPI error and roadside acknowledgement. Repeated radio loss, sensor drift or computer resets can then trigger condition-based maintenance. Cross-agency service objectives should name owners and recovery targets. Because added connectivity expands the attack surface, observability must be paired with authentication, segmentation, patch governance, logging and tested degraded modes (Avcı & Koca, 2024).",
    ],
    "4.3 Prioritised Implementation and KPI Framework": [
        "Implementation should follow its dependencies: agree identifiers, ownership and baseline KPIs; automate quality and latency monitoring; test ETA and disruption models in shadow mode; then pilot conditional TSP on a limited corridor with observable vehicle, roadside and SCATS responses. Scaling should depend on RTPI error, headway variation, early departures, lost kilometres, availability, TSP success and effects on cross traffic and pedestrians. Matched before-and-after evaluation is stronger than usage counts. This sequence constrains integration and model risk while addressing the data-quality and interpretability conditions identified by Fatorachian and Kazemi (2024).",
    ],
    "7.1 Definition and Role in Congestion Management": [
        "TSP adjusts normal signals through measures such as green extension, early green or phase changes for eligible buses. Unlike emergency pre-emption, it remains conditional and preserves pedestrian clearance, safety and coordination (Smith et al., 2005). Dublin should prioritise late or headway-disrupted services, subject to signal state and recent priority activity, rather than every detected bus. The objective is to reduce avoidable signal delay and delay propagation, not to claim that TSP removes congestion.",
    ],
    "7.2 Twenty Second Polling and SCATS Limitations": [
        "The historical AVLC feed transmitted one way in synchronised 20-second slots and could not request an extra update near a junction. Location age, processing and transfer delay made it unsuitable for direct priority, although DCC could use buses as probes for SCATS retiming (World Bank, 2011). An operational loop needs timely detection, a validated request, controller acceptance or rejection and an outcome record. Acknowledgement is essential for distinguishing communications failure from a denied request and for measuring success.",
    ],
    "7.3 Vehicle to Infrastructure and Conditional TSP Design": [
        "The on-board unit should send vehicle, route, trip, direction, estimated arrival and schedule or headway status to a roadside unit. Local services validate identity and apply safety, cooldown and corridor constraints before passing an eligible request to SCATS. The response and subsequent bus passage return to the central log. Local exchange removes the polling delay; central policy retains consistency and audit. Green extension or early green should be default treatments, with normal signal operation as the fallback when communications or validation fails. Figure 7 depicts this closed request-response-measurement loop.",
    ],
    "7.4 Impacts, KPIs, and Road User Safeguards": [
        "A corridor pilot should compare bus travel time, headway variation, punctuality, request success and latency against matched periods or untreated junctions. Cross-street queues, pedestrian delay and emergency access must be measured in parallel. Maximum extension, consecutive-call and recovery limits protect other users, while logged rejection reasons support learning. Expansion is justified only when reliability improves without breaching agreed safety and network-impact thresholds.",
    ],
    "8.1 Travel Time and Delay Prediction": [
        "ETA models require historical AVL or actual arrival events joined to GTFS schedules, route and stop attributes, weather and incidents; static GTFS alone has no delay label. A historical baseline and gradient-boosted trees should precede deeper models. Outputs should include sectional time, ETA and uncertainty for RTPI and dispatcher alerts. Testing must be separated by time and report error by route, period and disruption state, since a network average can conceal weak corridors. Shadow mode and dispatcher override should precede operational use.",
    ],
    "8.2 Predictive Conditional TSP": [
        "Predictive TSP estimates stop-line arrival and priority value from trajectory, lateness or headway, dwell state, signal phase and queues. A constrained optimiser selects no treatment, early green or bounded extension. Reinforcement learning belongs first in simulation because reward design can hide pedestrian or cross-street costs and policies may fail under changed traffic (Fatorachian & Kazemi, 2024). Deployment should progress through replay, simulation, shadow decisions and a supervised corridor pilot, while the controller enforces hard safety constraints independently of the model.",
    ],
    "8.3 Incident Detection and Predictive Maintenance": [
        "Missed polls, GPS-odometer divergence, sign-on failures, excessive dwell, route deviation, sensor faults and computer resets can be compared with device and route baselines. Known signatures should use transparent rules; anomaly detection can identify unfamiliar patterns but requires human review. Alerts should state the vehicle, evidence, severity and recommended check rather than an unexplained score. Detection lead time, false-alert rate, repair time and repeat failure are suitable KPIs, and no opaque model should remove a vehicle from service automatically.",
    ],
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": [
        "Years one and two establish identifiers, ownership, retention, quality monitoring and KPI baselines, then test ETA and anomaly models offline. Years two and three introduce shadow prediction and a conditional TSP pilot; years three and four integrate proven services into dispatcher workflows; year five scales only demonstrated benefits. Security controls include authentication, segmentation, patching and incident response (Avcı & Koca, 2024). Model controls add versioning, drift and bias monitoring, approval gates, override and rollback. Table 5 links each use case to its data, action, KPI and safeguard; Figure 8 makes later phases conditional on earlier evidence.",
    ],
})

table_1_rows = [
    ["ETM and RS485", "Vehicle identity, ticketing and peripheral integration", "Reused sign-on and route data; automated destination and fare-device exchanges", "Legacy, device-specific interfaces; no common vehicle data model", "World Bank (2011)"],
    ["Tait trunked radio", "Private voice, emergency and AVLC data communication", "Improved coverage, call control, security and cross-depot flexibility", "Private network and supplier dependency; finite polling capacity", "World Bank (2011)"],
    ["AVLC and control centre", "Location, schedule comparison, dispatch and reporting", "Proactive route regulation; fewer early departures; performance evidence", "Benefits not quantified; data quality and training remained material", "World Bank (2011)"],
    ["SIRI and RTPI", "Transfer predictions to DCC-managed passenger information", "Shared real-time information beyond the operator", "Cross-agency service dependency; initial coverage and governance gaps", "World Bank (2011)"],
    ["SCATS and TSP interface", "Use buses as probes and potentially request signal priority", "Supported review of travel times and signal settings", "No operational TSP; 20-second one-way polling was too coarse", "World Bank (2011)"],
]

table_2_rows = [
    ["Wrong trip or stop identity", "Sign-on, reference-data or mapping error", "Incorrect control view or RTPI", "Driver procedures and data cleaning", "Automated referential checks; quarantine invalid events", "Invalid-event rate; RTPI error"],
    ["Vehicle communication loss", "Radio, base station or on-board fault", "Loss of visibility and delayed intervention", "Trunked radio; supplier maintenance", "Link-health alerts; redundant channel; degraded procedure", "Missed-poll rate; recovery time"],
    ["Cyber compromise", "Connected devices, credentials or unpatched interface", "False data, outage or control disruption", "Access and supplier controls", "Segmentation, authentication, logging and patch governance", "Critical findings; containment time"],
    ["Cross-agency interface failure", "Unclear ownership or incompatible change", "RTPI or TSP service degradation", "Agreed specifications and relationships", "Versioned contracts, service objectives and joint incident process", "Availability; breach count"],
    ["Predictive model error", "Poor data, drift or opaque decision logic", "Misleading ETA or priority decision", "Human dispatch oversight", "Shadow mode, baseline comparison, monitoring and rollback", "Prediction error; override rate"],
]

table_3_rows = [
    ["Transmodel", "Conceptual public-transport model", "Shared entities and relationships", "No", "Semantic consistency", "Complex to implement fully", "Common vocabulary and identity model"],
    ["NeTEx", "Detailed planned-network exchange", "Network, timetable and fare XML", "No", "Rich European scope", "Greater implementation complexity", "Authority and operator planned-data exchange"],
    ["SIRI", "Operational information exchange", "Estimated, vehicle and service messages", "Yes", "European real-time interoperability", "Depends on profiles and data quality", "AVLC-to-RTPI and operational feeds"],
    ["GTFS", "Widely used scheduled-service publication", "CSV routes, trips, stops and times", "No", "Simple and broadly supported", "Limited operational semantics", "Open-data and planned-service analysis"],
    ["GTFS-Realtime", "Live service updates", "Protocol-buffer trip, vehicle and alert entities", "Yes", "Broad consumer ecosystem", "Requires a genuine live feed and stable IDs", "Future open vehicle and disruption services"],
]

table_4_rows = [
    ["Architecture", "Useful components; no formal overall model in the case", "Documented layers, interfaces and owners", "Change risk across project-specific links", "Create an enterprise ITS architecture and interface catalogue"],
    ["Data quality", "Cleaning and calibration continued after deployment", "Automated validation and observability", "Errors can propagate into RTPI and control", "Monitor identity, completeness, latency and sensor agreement"],
    ["Congestion control", "AVLC probes informed SCATS; no operational TSP", "Conditional, acknowledged priority requests", "Twenty-second one-way polling was inadequate", "Pilot low-latency vehicle-to-infrastructure TSP"],
    ["Analytics", "Reporting and running-time review", "Predictive support with staged validation", "Limited quantified benefits and predictive capability", "Use shadow mode and compare against simple baselines"],
    ["Governance", "Strong working relationships; interfaces handled case by case", "Formal multi-agency service objectives", "Accountability and change coordination risk", "Joint ownership, incident process and measurable KPIs"],
]

table_5_rows = [
    ["ETA and delay prediction", "Actual AVL events, GTFS, weather and incidents", "Baseline plus gradient boosting", "ETA, delay and uncertainty", "Update RTPI and flag emerging delay", "MAE by route and period", "Drift or missing data; shadow mode and fallback"],
    ["Headway and bunching risk", "AVL trajectories, headways, dwell and schedule", "Time-series or boosted model", "Bunching probability", "Hold, regulate or short-turn review", "Headway variation; intervention benefit", "Unequal service impact; dispatcher approval"],
    ["Conditional TSP", "Trajectory, lateness, headway and signal state", "Arrival prediction plus constrained optimisation", "Treatment and request timing", "Submit bounded priority request", "Bus saving; cross-street and pedestrian delay", "Unsafe or unfair priority; hard controller constraints"],
    ["Incident and maintenance alert", "Telemetry, missed polls, sensors and fault history", "Rules plus anomaly detection", "Evidence-based alert", "Inspect vehicle or communications asset", "Lead time; false alerts; repair time", "False positives; human verification and rollback"],
]

completed_table_rows = {
    "3.4 Effectiveness and Architectural Limitations": table_1_rows,
    "5.3 Operational, Data, Cyber, and Organisational Risk Mitigation": table_2_rows,
    "6.2 GTFS  SIRI  NeTEx and Transmodel Comparison": table_3_rows,
    "6.4 Dublin Bus Capability Gap and Transferable Lessons": table_4_rows,
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": table_5_rows,
}

completed_table_notes = {
    "3.4 Effectiveness and Architectural Limitations": "Note. Benefits and limitations describe the historical case-study period. Source: World Bank (2011).",
    "5.3 Operational, Data, Cyber, and Organisational Risk Mitigation": "Note. Controls synthesise the Dublin Bus case with security and learning-system risks identified by Avcı and Koca (2024) and Fatorachian and Kazemi (2024).",
    "6.2 GTFS  SIRI  NeTEx and Transmodel Comparison": "Note. The standards are complementary rather than substitutes. Sources: MobilityData (n.d.) and Transmodel (n.d.).",
    "6.4 Dublin Bus Capability Gap and Transferable Lessons": "Note. Dublin Bus refers to the historical case baseline; comparator practice is synthesised from the cited literature and standards.",
    "8.4 Five-Year Roadmap, Governance, and Risk Controls": "Note. Models require archived operational data and controlled validation; the supplied static GTFS is insufficient for training delay or TSP models.",
}

for title, subsections in sections:
    body.append(paragraph(title, style="Heading1", before=240, after=180, keep=True))
    if title == "References":
        for reference in references:
            body.append(rich_paragraph(reference, style="Reference", after=120))
        continue
    if title in section_content:
        for text in section_content[title]:
            body.append(paragraph(text))
        continue
    for index, (level, item) in enumerate(subsections):
        if level in (2, 3):
            style = "Heading2" if level == 2 else "Heading3"
            body.append(paragraph(item, style=style, before=180 if level == 2 else 100, after=90, keep=True))
            next_level = subsections[index + 1][0] if index + 1 < len(subsections) else 0
            if item in section_content:
                for text in section_content[item]:
                    body.append(paragraph(text))
            elif next_level <= level:
                body.append(paragraph("[Draft content to be added]"))
        else:
            body.append(bullet(item))
        if item in tables_after:
            number, table_title, columns, widths, rows = tables_after[item]
            if item in completed_table_rows:
                body.append(table_with_data(
                    number,
                    table_title,
                    columns,
                    widths,
                    completed_table_rows[item],
                    completed_table_notes[item],
                ))
            else:
                body.append(table_placeholder(number, table_title, columns, widths, rows))
        if item in figures_after:
            number, figure_title, description = figures_after[item]
            body.append(figure_placeholder(number, figure_title, description))

sect = (
    '<w:sectPr>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
    '</w:sectPr>'
)

document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <w:body>{''.join(body)}{sect}</w:body>
</w:document>'''

styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
 <w:docDefaults>
  <w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault>
 </w:docDefaults>
 <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
 <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/><w:szCs w:val="40"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:rPr><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="CoverInfo"><w:name w:val="Cover Information"/><w:basedOn w:val="Normal"/><w:next w:val="CoverInfo"/><w:pPr><w:spacing w:line="300" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="CaptionLabel"><w:name w:val="Caption Label"/><w:basedOn w:val="Normal"/><w:next w:val="CaptionTitle"/><w:pPr><w:keepNext/><w:spacing w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="CaptionTitle"><w:name w:val="Caption Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="FigurePlaceholder"><w:name w:val="Figure Placeholder"/><w:basedOn w:val="Normal"/><w:next w:val="FigureNote"/><w:pPr><w:keepNext/><w:spacing w:line="300" w:lineRule="auto"/></w:pPr><w:rPr><w:i/><w:color w:val="666666"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="FigureNote"><w:name w:val="Figure Note"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="333333"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Reference"><w:name w:val="Reference"/><w:basedOn w:val="Normal"/><w:next w:val="Reference"/><w:pPr><w:ind w:left="720" w:hanging="720"/><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="TOCHeading"><w:name w:val="TOC Heading"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:semiHidden/><w:unhideWhenUsed/><w:pPr><w:spacing w:before="0" w:after="30" w:line="220" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="21"/><w:szCs w:val="21"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:semiHidden/><w:unhideWhenUsed/><w:pPr><w:spacing w:before="0" w:after="10" w:line="210" w:lineRule="auto"/><w:ind w:left="360"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="TOC3"><w:name w:val="toc 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:semiHidden/><w:unhideWhenUsed/><w:pPr><w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="auto"/><w:ind w:left="720"/></w:pPr><w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/><w:color w:val="000000"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:style>
</w:styles>'''

settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
 <w:updateFields w:val="true"/>
 <w:compat/>
</w:settings>'''

content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="xml" ContentType="application/xml"/>
 <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
 <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
 <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
 <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
 <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
 <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
 <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
 <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>'''

core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <dc:title>MSE806 Assessment 1 Report Template</dc:title>
 <dc:subject>Dublin Bus Intelligent Transport Systems</dc:subject>
 <dc:creator>Student</dc:creator>
</cp:coreProperties>'''

app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
 <Application>Microsoft Office Word</Application>
</Properties>'''

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("docProps/core.xml", core)
    z.writestr("docProps/app.xml", app)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/settings.xml", settings)
    z.writestr("word/_rels/document.xml.rels", doc_rels)

print(OUT.resolve())
