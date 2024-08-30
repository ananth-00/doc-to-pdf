from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from docx2pdf import convert
import os

app = FastAPI()

def convert_docx_to_pdf(input_path, output_path):

    try:
        convert(input_path,output_path)
        print(f"Conversion completed.PDF file saved as {output_path}")
    except Exception as e:
        print(f"An error occured: {str(e)}")
        
        
@app.post("/convert/")
async def convert_endpoint(file: UploadFile = File(...)):
    
        try:
            
            input_path = f"temp_{file.filename}"
            with open(input_path, "wb") as buffer:
                buffer.write(await file.read())
                
            output_path = input_path.replace('.docx', '.pdf')
            
            convert_docx_to_pdf(input_path, output_path)
            
            os.remove(input_path)
            
            return FileResponse(output_path, media_type='application/pdf', filename = os.path.basename(output_path))
        
        except Exception as e:
            
            return {"error": str(e)}
        
        
if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)