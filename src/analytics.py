import csv
from statistics import mean, median
from fpdf import FPDF #for pdf creation and handeling

ANALYTICS_FILE="analytics.csv"

def updateAnalytics(file_id, score):
    #logging students' score
    with open(ANALYTICS_FILE, 'a', newline='')as f:
        writer=csv.writer(f)
        writer.writerow([file_id, score])

def printScoreSummary():
    #outputting satistical data
    scores= []
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                scores.append(float(row[1]))
        if scores:
            print(f"[Analytics] Mean: {mean(scores):.2f}, High: {max(scores)}, Low: {min(scores)}")
    except FileNotFoundError:
        print("[Analytics] no data sourced yet!")

def generateReport(file_id=None):
    try:
        df = pd.read_csv(ANALYTICS_FILE, names=["id", "score"])
    except FileNotFoundError:
        return {"error": "no data found."}
    
    if df.empty or "score" not in df.columns: 
        #checking if the dataframe has no rows i.e no data OR if the score column exists
        #error handleing
        return{"error": "analytics file is empty/malformed"}
    
    df["score_percent"]=df["score"]/100.0*100 #creating a new column in the dataframe
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    
    report = {} #initializing the report directory
    
    #if a specific student ID is provided and exists in the dataset:
    if file_id and dile_id in df["id"].values:
        user_row = df[df["id"] == file_id] #getRow()
        rank = user_row.index[0] + 1  #determine rank
        score = user_row.iloc[0]["score"]  #getScore()
        percentile = round((1 - (rank - 1) / len(df)) * 100, 2) #calculating percentile

        #populating report with stats: 
        report["Student"] = file_id
        report["Score"] = f"{score:.2f}/100.00 ({score:.2f}%)"
        report["Rank"] = rank
        report["Percentile"] = percentile
    elif file_id: 
        #id not found
        return{"error":"id not found"}
    
    #adding stats to the report
    report["Minimum Score"] = f"{df['score'].min():.2f}/100.00"
    report["Median Score"] = f"{median(df['score']):.2f}/100.00"
    report["Maximum Score"] = f"{df['score'].max():.2f}/100.00"

    return report 

def exportReportPDF(file_id, filename="report.pdf"):
    report=generateReport(file_id)
    if "error" in report:
        return report

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student Analytics Report", ln=True)

    for key, value in report.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output(filename)
    return {"success": f"PDF report saved as {filename}"}
        