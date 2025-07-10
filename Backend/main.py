import pandas as pd
from fastapi import FastAPI, HTTPException, Header 
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from query.models import NlpRequest, Token, LoginRequest
from jwt_token.token_verification import create_access_token , verify_token
from prompt.utils import get_gemini_response, read_sql_query, generate_summary_from_gemini



load_dotenv()


app = FastAPI()


@app.post("/api/token", response_model=Token)
async def login(login_data: LoginRequest):
    if login_data.username != "user" or login_data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": login_data.username})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/api/natural_query", response_class=HTMLResponse)
async def natural_language_query(request: NlpRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required")
    
    token = authorization.strip()
    verify_token(token) 

    name = request.name
    try:
        generated_sql = get_gemini_response(request.question, name)
        rows, column_names = read_sql_query(generated_sql, request.question, name)

        print(request.question)
        print(rows, column_names)
        
        if rows and column_names:
            formatted_column_names = [" ".join(word.capitalize() for word in col.split("_")) for col in column_names]
            data = pd.DataFrame(rows, columns=formatted_column_names)
            
            # Generate table HTML
            table_html = data.to_html(index=False, classes="table table-striped", border=1)
            
            # Generate summary
            summary = generate_summary_from_gemini(request.question, data)
            
            # Return summary as plain string followed by the table HTML
            response_html = f"{summary}\n{table_html}"
            
            return response_html
        else:
            raise HTTPException(status_code=404, detail="No data found or an error occurred")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")