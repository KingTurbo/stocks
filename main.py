from threading import excepthook
from requests.models import HTTPError
from urllib.request import urlopen
import certifi
import json
import ssl
import yfinance as yf
import time
import sys

start = time.time()


Apikey = "xyz"


def get_stock_data(ticker):


  def get_ratio_data(url1):
            context = ssl.create_default_context()
            response = urlopen(url1, context=context)
            data = response.read().decode("utf-8")
            return json.loads(data)

  url1 = ("https://financialmodelingprep.com/api/v3/ratios/"+ticker+"?apikey="+Apikey)

  ##############################################################################################

  def get_financial_data(url2):

      context = ssl.create_default_context(cafile=certifi.where())
      response = urlopen(url2, context=context)
      data = response.read().decode("utf-8")
      return json.loads(data)

  url2 = ("https://financialmodelingprep.com/api/v3/income-statement/"+ticker+"?apikey="+Apikey)
  #print(get_financial_data(url2))
  #####################################################################################################################

  def get_balance_sheet(url3):
      context = ssl.create_default_context(cafile=certifi.where())
      response = urlopen(url3, context=context)
      data = response.read().decode("utf-8")
      return json.loads(data)

  url3 = ("https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+ticker+"?limit=120&apikey="+Apikey)

  #####################################################################################################################
  def get_income_growth(url4):
      context = ssl.create_default_context(cafile=certifi.where())
      response = urlopen(url4, context=context)
      data = response.read().decode("utf-8")
      return json.loads(data)
  url4 = ("https://financialmodelingprep.com/api/v3/income-statement-growth/"+ticker+"?limit=40&apikey="+Apikey) # Growth
  #####################################################################################################################

      
  try:
     output = get_ratio_data(url1)
  except:
    return
  
  output2 = get_financial_data(url2)
  output_bs = get_balance_sheet(url3)
  output_igrowth = get_income_growth(url4)

  #################################################################################  Sektor = ti['sector']  beta = ti['beta']   


  ticker_yf = yf.Ticker(ticker)
  ti = ticker_yf.info

  try:
    Sektor = ti['sector']
    beta = ti['beta']
    Land = ti['country']
    Preis = ti["currentPrice"]
  except:
       return


  Anlagevermögen = output_bs[0]["totalNonCurrentAssets"]
  Eigenkapital = output_bs[0]["totalEquity"]
  Fremdkapital = output_bs[0]["totalLiabilities"]
  Gesamtkapital = output_bs[0]["totalLiabilitiesAndTotalEquity"]
  langfristiges_Fremdkapital = output_bs[0]["longTermDebt"]


  Eigenkapitalquote = Eigenkapital / Gesamtkapital
  Fremdkapitalquote = Fremdkapital / Gesamtkapital

  #anderes
  Steuersatz = output[0]['effectiveTaxRate']
  Dividend = output[0]['dividendYield']
  fairPrice = output[0]['priceFairValue']

  #Zahlen vergleich
  LIQ1 = output[0]['cashRatio'] # Check
  LIQ2 = output[0]['quickRatio'] # Check
  LIQ3 = output[0]['currentRatio'] # Check
  DebttoEquityRatio = output[0]['debtEquityRatio'] # Check
  Zinsdeckungsgrad = output[0]['interestCoverage'] # Check
  KBV = output[0]['priceBookValueRatio'] # Check
  KUV = output[0]['priceToSalesRatio']# Check
  KGV = output[0]['priceEarningsRatio'] # Check
  KCV = output[0]['priceToOperatingCashFlowsRatio']# Check
  PEGRatio = output[0]['priceEarningsToGrowthRatio']# könnte man printen # Check
  try:
    DeckungsgradA = Eigenkapital / Anlagevermögen # Check
  except:
    return
  try:
    DeckungsgradB = (Eigenkapital + langfristiges_Fremdkapital) / Anlagevermögen # Check
  except:
    return
  
  Bruttogewinn = output[0]["grossProfitMargin"] # Check
  #Branchen
  DSO = output[0]['daysOfSalesOutstanding']# könnte man printen


  #vorjahr
  Umsatzwachstum = output_igrowth[0]["growthRevenue"] # Check
  Nettowachstum = output_igrowth[0]["growthNetIncome"] # Check
  Forschung = output_igrowth[0]["growthResearchAndDevelopmentExpenses"]# Check
  EBITDA_growth = output_igrowth[0]["growthEBITDA"]# Check

  # Vorjahr + Branche
  ROA = output[0]['returnOnAssets']# Check
  ROA_ly = output[1]['returnOnAssets']# Check

  ROE = output[0]['returnOnEquity']# Check
  ROE_ly = output[1]['returnOnEquity']# Check


  ######################################################################################

  sector_kgv_mapping = {
          "Basic Materials": 12,
          "Consumer Cyclical": 20,
          "Financial Services": 9,
          "Real Estate": 23,
          "Consumer Defensive": 24,
          "Healthcare": 28,
          "Utilities": 20,
          "Communication Services": 14,
          "Energy": 8,
          "Industrials": 24,
          "Technology": 25
      }

  if Sektor in sector_kgv_mapping:
      kgv_vg = sector_kgv_mapping[Sektor]
  else:
      kgv_vg = 21
  ######################################################################################

  sector_kuv_mapping = {
          "Basic Materials": 3,
          "Consumer Cyclical": 2,
          "Financial Services": 2.5,
          "Real Estate": 6,
          "Consumer Defensive": 2.5,
          "Healthcare": 3,
          "Utilities": 3,
          "Communication Services": 3.5,
          "Energy": 2,
          "Industrials": 3,
          "Technology": 4
      }

  if Sektor in sector_kuv_mapping:
      Kuv_vg = sector_kuv_mapping[Sektor]
  else:
      EBITDA_Marge_vg = 21
  #########################################
  sector_kcv_mapping = {
          "Basic Materials": 12,
          "Consumer Cyclical": 16,
          "Financial Services": 5,
          "Real Estate": 8,
          "Consumer Defensive": 17,
          "Healthcare": 17,
          "Utilities": 14,
          "Communication Services": 14,
          "Energy": 5,
          "Industrials": 15,
          "Technology": 9
      }

  if Sektor in sector_kcv_mapping:
      kcv_vg = sector_kcv_mapping[Sektor]


  continents = {
          "Afrika": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros", "Democratic Republic of the Congo", "Republic of the Congo", "CÃ´te d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Swaziland", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "SÃ£o TomÃ© and PrÃ­ncipe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
          "Asien": ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Burma", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Russia", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "East Timor", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"],
          "Europa": ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatikan City", "Great Britian"],
          "Nordamerika": ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", 
      "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"],
          "Südamerika": ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"],
          "Ozeanien": ["Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", 
      "Tonga", "Tuvalu", "Vanuatu"],
      }


      # Funktion zum Überprüfen, in welchem Kontinent ein Land liegt
  def get_continent(country):
          for continent, countries in continents.items():
              if country in countries:
                  return continent
          return "Unbekannter Kontinent"

      # Beispiel: Prüfen, in welchem Kontinent Frankreich liegt
  continent = get_continent(Land)

  market_risk_premiums = {
      "Nordamerika": 0.08,
      "Europa": 0.078,
      "Asien": 0.055,
      "Afrika": 0.02,
      "Südamerika": 0.04,
      "Ozeanien": 0.04
  }

  # Set default value
  market_risk_premium = 0.05

  # Overwrite default value if continent is in dictionary
  if continent in market_risk_premiums:
      market_risk_premium = market_risk_premiums[continent]

  risk_free_rate = 0.03  
  beta = ti['beta']
  cost_of_equity = risk_free_rate + (beta * market_risk_premium)

      # wacc = Eigenkapitalquote * CAPM(oben) + Fremdkapitalquote * Fremdkapitalkostensatz * (1 - Ertragssteuersatz)

  Fremdkapitalkostensatz = 0.1
  Ertragssteuersatz = Steuersatz

  wacc = Eigenkapitalquote * cost_of_equity + Fremdkapitalquote * Fremdkapitalkostensatz * (1-Ertragssteuersatz)
  ##########################################################################################################################

  score = 0

  if LIQ3 > 2:
      score = score + 2
  else:
      if LIQ3 > 1:
        score = score + 1

  if LIQ2 > 1:
      score = score + 2

  if LIQ1 < 0.3:
    score = score + 2

  if DebttoEquityRatio < 1:
    score = score + 0.5

  if Zinsdeckungsgrad is not None:
    if Zinsdeckungsgrad > 10:
      score = score + 1.5
    elif Zinsdeckungsgrad > 3:
      score = score + 0.5
  else:
    return
  if KBV > 1:
    score = score + 1

  if KUV < Kuv_vg:
    score = score + 1

  if KGV < kgv_vg:
    score = score + 1

  if KCV < kcv_vg:
    score = score + 1

  if PEGRatio < 0.5:
    score = score + 3
  elif PEGRatio < 1:
    score = score + 1

  if DeckungsgradA >= 0.7:
    score = score + 1

  if DeckungsgradB > 1:
    score = score + 1

  if Umsatzwachstum > 0.1:
    score = score + 1
  elif Umsatzwachstum >= 0.05:
    score = score + 0.5

  if Nettowachstum > 0.1:
    score = score + 1
  elif Nettowachstum >= 0.05:
    score = score + 0.5

  if Bruttogewinn >= 0.5:
    score = score + 1

  if Forschung > 0:
    score = score + 1

  if EBITDA_growth > 0:
    score = score + 1

  if ROA > wacc and ROA > ROA_ly:
    score = score + 1
  elif ROA > ROA_ly:
    score = score + 0.5

  if ROE >= ROE_ly and ROE >= 0.3:
    score = score + 1
  #24

  print(str(ticker) +";"+ str(score))
  print(str(ticker) +";"+ str(PEGRatio)+ ";" + str(DSO)+ ";"+str(KGV)+";"+str(kgv_vg)+";"+str(KCV)+";"+str(fairPrice)+";"+str(Preis)+";"+str(beta)+";"+str(DeckungsgradA)+";"+str(DeckungsgradB)+";"+str(LIQ1)+";"+str(LIQ2)+";"+str(LIQ3))


ticker_list = ["AAPL"]


for ticker in ticker_list:
  get_stock_data(ticker)


ende = time.time()
print("Die Zeitdauer beträgt: {:.0f}h {:.0f}min {:.2f}s".format((ende - start) // 3600, ((ende - start) % 3600) // 60, ((ende - start) % 3600) % 60))
