from io import BytesIO
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

templates = Environment(loader=FileSystemLoader("app/reports/templates"))

def generate_pdf_response(template_name:str, data:dict, filename:str):
    
    template = templates.get_template(template_name)
    html_content = template.render(**data)
    pdf_buffer = BytesIO()
    
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }        
)