from fpdf import FPDF

def generate_pdf(data, prediction):
    fields = [
        'Age_band_of_driver', 'Sex_of_driver', 'Educational_level',
        'Vehicle_driver_relation', 'Driving_experience', 'Lanes_or_Medians',
        'Types_of_Junction', 'Road_surface_type', 'Light_conditions',
        'Weather_conditions', 'Type_of_collision', 'Vehicle_movement',
        'Pedestrian_movement', 'Cause_of_accident'
    ]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Traffic Accident Severity Report", ln=True, align='C')
    pdf.ln(10)

    for field, value in zip(fields, data):
        pdf.cell(200, 10, txt=f"{field.replace('_', ' ')}: {value}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Predicted Severity: {prediction}", ln=True)

    pdf.output("report.pdf")
    return "report.pdf"
