from fastapi import FastAPI, HTTPException
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = FastAPI()

# Mock data for demonstration
mock_data = {
    'Country': ['USA', 'Italy'],
    'Date': ['2020-01-01', '2020-01-01'],
    'Cases': [100, 50]
}

df = pd.DataFrame(mock_data)

def getCasesByCountry(country: str):
    return df[df['Country'] == country]

def getEconomicsDataByCountry(country: str):
    # Mock economic data
    return pd.DataFrame({
        'Year': [2020, 2021],
        'GDP': [50000, 52000],
        'Country': [country] * 2
    })

@app.get("/")
async def hello():
    return {"message": "Hello there! API is working!"}

@app.get("/author")
async def author():
    return {"message": "Marks Dvojeglazovs"}

@app.get("/help")
async def help():
    return {"message": "This is a help page. You can find all the information about this API here."}

@app.get("/data/{country}")
async def data(country: str):
    try:
        data_df = getCasesByCountry(country)
        return {"data": data_df.to_dict(orient='records')}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Data for country '{country}' not found.")

@app.get("/visual/{country}")
async def visual(country: str):
    try:
        df = getCasesByCountry(country)
        fig = px.line(df, x="Date", y="Cases", title=f"Cases per country: {country}")
        fig_json = pio.to_json(fig)
        return {"figure": fig_json}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Data for country '{country}' not found.")

@app.get("/economy/{country}")
async def economy(country: str):
    try:
        economic_data = getEconomicsDataByCountry(country)
        return {"data": economic_data.to_dict(orient='records')}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Economic data for country '{country}' not found.")
