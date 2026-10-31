"""
Generates multi-sheet Excel Workbook (SpreadsheetML) compatible with Microsoft Excel
Contains Raw Data, Cleaned Data, Pivot KPI Summary, and Excel Formulas Guide.
"""

import csv
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_DIR, "data")

def build_excel_workbook():
    clean_csv = os.path.join(DATA_DIR, "cleaned_students_data.csv")
    raw_csv = os.path.join(DATA_DIR, "raw_students_data.csv")

    with open(clean_csv, "r", encoding="utf-8") as f:
        clean_rows = list(csv.reader(f))

    with open(raw_csv, "r", encoding="utf-8") as f:
        raw_rows = list(csv.reader(f))

    xml_header = """<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
 <Styles>
  <Style ss:ID="Default" ss:Name="Normal">
   <Alignment ss:Vertical="Bottom"/>
   <Borders/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#000000"/>
   <Interior/>
   <NumberFormat/>
   <Protection/>
  </Style>
  <Style ss:ID="Header">
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#FFFFFF" ss:Bold="1"/>
   <Interior ss:Color="#1F4E78" ss:Pattern="Solid"/>
   <Alignment ss:Horizontal="Center" ss:Vertical="Center"/>
  </Style>
  <Style ss:ID="SubHeader">
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#FFFFFF" ss:Bold="1"/>
   <Interior ss:Color="#2F5597" ss:Pattern="Solid"/>
   <Alignment ss:Horizontal="Left" ss:Vertical="Center"/>
  </Style>
  <Style ss:ID="HighlightRed">
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#9C0006" ss:Bold="1"/>
   <Interior ss:Color="#FFC7CE" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="HighlightGreen">
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#006100" ss:Bold="1"/>
   <Interior ss:Color="#C6EFCE" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="BoldText">
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Bold="1"/>
  </Style>
 </Styles>
"""

    def generate_sheet(name, rows, is_clean=False):
        out = f' <Worksheet ss:Name="{name}">\n  <Table>\n'
        for r_idx, row in enumerate(rows):
            out += '   <Row>\n'
            for c_idx, cell in enumerate(row):
                style_attr = ''
                cell_type = "String"
                clean_cell = cell.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

                if r_idx == 0:
                    style_attr = ' ss:StyleID="Header"'
                elif is_clean:
                    if clean_cell == "High Risk" or clean_cell == "Fail":
                        style_attr = ' ss:StyleID="HighlightRed"'
                    elif clean_cell == "Pass" or clean_cell == "Low Risk":
                        style_attr = ' ss:StyleID="HighlightGreen"'

                try:
                    float(cell)
                    cell_type = "Number"
                except ValueError:
                    pass

                out += f'    <Cell{style_attr}><Data ss:Type="{cell_type}">{clean_cell}</Data></Cell>\n'
            out += '   </Row>\n'
        out += '  </Table>\n </Worksheet>\n'
        return out

    # Pivot Summary Sheet
    pivot_sheet = """ <Worksheet ss:Name="Pivot_Summary">
  <Table>
   <Row>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Metric / Dimension</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Enrolled Students</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Avg Attendance %</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Pass Count</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Pass Rate %</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">Computer Science &amp; Business Systems (CSBS)</Data></Cell>
    <Cell><Data ss:Type="Number">68</Data></Cell>
    <Cell><Data ss:Type="Number">82.4</Data></Cell>
    <Cell><Data ss:Type="Number">52</Data></Cell>
    <Cell><Data ss:Type="Number">76.5</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">Computer Engineering (CE)</Data></Cell>
    <Cell><Data ss:Type="Number">64</Data></Cell>
    <Cell><Data ss:Type="Number">82.1</Data></Cell>
    <Cell><Data ss:Type="Number">48</Data></Cell>
    <Cell><Data ss:Type="Number">75.0</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">Information Technology (IT)</Data></Cell>
    <Cell><Data ss:Type="Number">58</Data></Cell>
    <Cell><Data ss:Type="Number">81.3</Data></Cell>
    <Cell><Data ss:Type="Number">42</Data></Cell>
    <Cell><Data ss:Type="Number">72.4</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">Artificial Intelligence &amp; Data Science (AIDS)</Data></Cell>
    <Cell><Data ss:Type="Number">60</Data></Cell>
    <Cell><Data ss:Type="Number">81.5</Data></Cell>
    <Cell><Data ss:Type="Number">42</Data></Cell>
    <Cell><Data ss:Type="Number">70.0</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="Header"><Data ss:Type="String">TOTAL / COHORT AVERAGE</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="Number">250</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="Number">81.9</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="Number">184</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="Number">73.6</Data></Cell>
   </Row>
   <Row></Row>
   <Row>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Attendance Cohort Group</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Count</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Avg Academic Score %</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Failed Students</Data></Cell>
    <Cell ss:StyleID="SubHeader"><Data ss:Type="String">Failure Rate %</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="HighlightRed"><Data ss:Type="String">Defaulters (&lt; 75% Attendance)</Data></Cell>
    <Cell ss:StyleID="HighlightRed"><Data ss:Type="Number">49</Data></Cell>
    <Cell ss:StyleID="HighlightRed"><Data ss:Type="Number">47.18</Data></Cell>
    <Cell ss:StyleID="HighlightRed"><Data ss:Type="Number">42</Data></Cell>
    <Cell ss:StyleID="HighlightRed"><Data ss:Type="Number">85.71</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="HighlightGreen"><Data ss:Type="String">Regular (&gt;= 75% Attendance)</Data></Cell>
    <Cell ss:StyleID="HighlightGreen"><Data ss:Type="Number">201</Data></Cell>
    <Cell ss:StyleID="HighlightGreen"><Data ss:Type="Number">67.71</Data></Cell>
    <Cell ss:StyleID="HighlightGreen"><Data ss:Type="Number">24</Data></Cell>
    <Cell ss:StyleID="HighlightGreen"><Data ss:Type="Number">11.94</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
"""

    # Excel Formulas Guide Sheet
    formulas_guide = """ <Worksheet ss:Name="Excel_Formulas_Guide">
  <Table>
   <Row>
    <Cell ss:StyleID="Header"><Data ss:Type="String">Formula Name</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="String">Formula Implementation</Data></Cell>
    <Cell ss:StyleID="Header"><Data ss:Type="String">Purpose in Project</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">VLOOKUP</Data></Cell>
    <Cell><Data ss:Type="String">=VLOOKUP(A2, Cleaned_Data!A:T, 16, FALSE)</Data></Cell>
    <Cell><Data ss:Type="String">Fetch Overall % or Grade based on Student ID</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">IF + COUNTIF</Data></Cell>
    <Cell><Data ss:Type="String">=IF(COUNTIF(I2:M2, "&lt;40")&gt;0, "Fail", "Pass")</Data></Cell>
    <Cell><Data ss:Type="String">Determine pass/fail based on 40 passing cutoff</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">AVERAGE</Data></Cell>
    <Cell><Data ss:Type="String">=AVERAGE(Cleaned_Data!H2:H251)</Data></Cell>
    <Cell><Data ss:Type="String">Calculate cohort mean attendance</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">COUNTIF</Data></Cell>
    <Cell><Data ss:Type="String">=COUNTIF(Cleaned_Data!H2:H251, "&lt;75")</Data></Cell>
    <Cell><Data ss:Type="String">Count attendance defaulters</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldText"><Data ss:Type="String">PIVOT TABLE</Data></Cell>
    <Cell><Data ss:Type="String">Insert &gt; PivotTable (Rows: Department, Values: Average of overall_pct)</Data></Cell>
    <Cell><Data ss:Type="String">Departmental performance ranking and summary</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
"""

    content = xml_header
    content += generate_sheet("Cleaned_Data", clean_rows, is_clean=True)
    content += generate_sheet("Raw_Data", raw_rows, is_clean=False)
    content += pivot_sheet
    content += formulas_guide
    content += "</Workbook>"

    out_file = os.path.join(DATA_DIR, "student_performance_workbook.xls")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated Excel Workbook: {out_file}")

if __name__ == "__main__":
    build_excel_workbook()
